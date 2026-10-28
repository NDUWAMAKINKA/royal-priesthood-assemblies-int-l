#!/usr/bin/env python3
"""One-command deploy for the RPAI church site and giving API.

The website and the giving API live in the same repository and deploy from the
same branch, so a single push ships both. This script wraps that push and then
*proves* the deploy actually landed instead of assuming it did.

    1. commit pending changes (only when -m is given)
    2. push the deploy branch
    3. wait until the frontend build for that exact commit succeeds, and until
       the API reports the same commit from /api/health

The live website is served by GitHub Pages, whose build is checked through the
GitHub Actions API. If the site is later served by the Render static site, the
build writes /deploy-info.json and that stamp is checked instead.

Run it with no arguments:

    python scripts/deploy.py
    python scripts/deploy.py -m "content: Sunday bulletin"

On a normal machine the helpers are:

    deploy.bat          (Windows)
    ./deploy.sh         (Linux/macOS)

Optional configuration, as environment variables or in `.env.deploy`:

    GITHUB_REPO=NDUWAMAKINKA/royal-priesthood-assemblies-int-l
    GITHUB_TOKEN=ghp_...                 (avoids anonymous API rate limits)
    SITE_URL=https://royal-priesthood-assemblies-int-l-1.onrender.com
    API_HEALTH_URL=https://royal-priesthood-assemblies-int-l.onrender.com/api/health
    RENDER_DEPLOY_HOOK_FRONTEND=https://api.render.com/deploy/srv-...?key=...
    RENDER_DEPLOY_HOOK_BACKEND=https://api.render.com/deploy/srv-...?key=...

The deploy hooks are only used by `--redeploy`, which rebuilds a service
without a new commit.

Exit codes: 0 success, 1 the deploy did not land, 2 preflight problem.
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DEFAULT_BRANCH = "main"
DEFAULT_SITE_URL = "https://royal-priesthood-assemblies-int-l-1.onrender.com"
DEFAULT_API_HEALTH_URL = (
    "https://royal-priesthood-assemblies-int-l.onrender.com/api/health"
)
DEFAULT_TIMEOUT = 15 * 60
DEFAULT_POLL = 20

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT

# Populated from .env.deploy in __main__; the real environment always wins.
FILE_ENV: dict = {}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

class DeployError(RuntimeError):
    """A preflight problem the user has to fix."""


def log(message: str) -> None:
    print(message, flush=True)


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git", *args],
        cwd=str(REPO),
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise DeployError("git %s failed: %s" % (" ".join(args), detail))
    return result


def git_output(*args: str) -> str:
    return run_git(*args).stdout.strip()


def load_env_file(path: Path) -> dict:
    """Read simple KEY=VALUE lines. Never overrides the real environment."""
    values = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def setting(name: str, default: str = "") -> str:
    value = os.environ.get(name)
    if value:
        return value.strip()
    return FILE_ENV.get(name, default).strip()


def http_get_json(url: str, headers: dict | None = None, timeout: int = 25) -> dict:
    request_headers = {
        "User-Agent": "rpai-deploy/1.0",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }
    if headers:
        request_headers.update(headers)
    request = urllib.request.Request(url, headers=request_headers)
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
        body = response.read().decode("utf-8", "replace")
    return json.loads(body)


def trigger_hook(name: str, hook: str, branch: str) -> str:
    separator = "&" if "?" in hook else "?"
    url = "%s%sref=%s" % (hook, separator, urllib.parse.quote(branch, safe=""))
    request = urllib.request.Request(
        url,
        method="POST",
        headers={"User-Agent": "rpai-deploy/1.0", "Content-Length": "0"},
    )
    context = ssl.create_default_context()
    try:
        with urllib.request.urlopen(request, timeout=30, context=context) as response:
            return "%s: HTTP %s" % (name, response.status)
    except urllib.error.HTTPError as err:
        raise DeployError(
            "%s deploy hook rejected the request (HTTP %s). "
            "Regenerate the hook URL in Render -> Settings -> Deploy Hook."
            % (name, err.code)
        ) from err


def short(commit: str) -> str:
    return commit[:7] if commit and commit != "unknown" else commit or "?"


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def github_repo() -> str:
    """owner/repo for the origin remote, or "" when it is not GitHub."""
    configured = setting("GITHUB_REPO")
    if configured:
        return configured.strip("/")

    remote = run_git("remote", "get-url", "origin", check=False)
    if remote.returncode != 0:
        return ""
    url = remote.stdout.strip()
    if url.endswith(".git"):
        url = url[: -len(".git")]
    if "github.com/" in url:
        return url.split("github.com/", 1)[1].strip("/")
    if "github.com:" in url:
        return url.split("github.com:", 1)[1].strip("/")
    return ""


def check_pages(repo: str, sha: str) -> tuple:
    """Did GitHub Pages publish this exact commit?"""
    if not repo:
        return "error", "no GitHub repository detected"

    url = (
        "https://api.github.com/repos/%s/actions/runs"
        "?head_sha=%s&per_page=50" % (repo, sha)
    )
    headers = {"Accept": "application/vnd.github+json"}
    token = setting("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer %s" % token

    try:
        data = http_get_json(url, headers=headers)
    except urllib.error.HTTPError as err:
        if err.code in (403, 429):
            return "error", "GitHub API rate limit (set GITHUB_TOKEN)"
        if err.code == 404:
            return "error", "GitHub Actions API not available for %s" % repo
        return "error", "GitHub API HTTP %s" % err.code
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        return "error", "GitHub unreachable (%s)" % getattr(err, "reason", err)
    except json.JSONDecodeError:
        return "error", "GitHub API returned invalid JSON"

    runs = [r for r in data.get("workflow_runs") or [] if r.get("head_sha") == sha]
    pages_runs = [r for r in runs if "pages" in (r.get("name") or "").lower()]
    if not pages_runs:
        return "pending", "no Pages build for %s yet" % short(sha)

    run = max(pages_runs, key=lambda r: r.get("created_at") or "")
    if run.get("status") != "completed":
        return "pending", "Pages build %s" % (run.get("status") or "running")
    if run.get("conclusion") == "success":
        return "ok", "GitHub Pages published %s" % short(sha)
    return "failed", "Pages build %s" % (run.get("conclusion") or "failed")


def check_stamp(site_url: str, sha: str) -> tuple:
    """Render static site: /deploy-info.json names the commit it built."""
    url = "%s/deploy-info.json?t=%d" % (
        site_url.rstrip("/"),
        int(time.time() * 1000),
    )
    try:
        data = http_get_json(url)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return "missing", "no deploy stamp at %s" % site_url
        return "error", "HTTP %s" % err.code
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        return "error", "unreachable (%s)" % getattr(err, "reason", err)
    except json.JSONDecodeError:
        return "error", "invalid JSON"

    live = str(data.get("commit", "")).strip()
    if not live or live == "unknown":
        return "error", "build ran without RENDER_GIT_COMMIT"
    if live != sha:
        return "pending", "live %s, want %s" % (short(live), short(sha))
    return "ok", "static build %s" % short(live)


def check_api(health_url: str, sha: str) -> tuple:
    """Is the API serving this commit and connected to the database?"""
    url = "%s?t=%d" % (health_url, int(time.time() * 1000))
    try:
        data = http_get_json(url)
    except urllib.error.HTTPError as err:
        routing = (err.headers or {}).get("x-render-routing", "")
        if err.code == 404 and routing == "no-server":
            return "down", "Render has no live server for this service"
        try:
            payload = json.loads(err.read().decode("utf-8", "replace"))
            reason = payload.get("db")
            if reason in (None, "", "ok"):
                reason = "ok=false"
        except Exception:  # noqa: BLE001 - diagnostic only
            reason = "HTTP %s" % err.code
        return "failed", "not healthy (%s)" % reason
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        return "error", "unreachable (%s)" % getattr(err, "reason", err)
    except json.JSONDecodeError:
        return "error", "invalid JSON"

    if not data.get("ok"):
        return "failed", "health check reported ok=false"

    live = str(data.get("commit", "unknown")).strip()
    if live not in ("", "unknown") and live != sha:
        return "pending", "live %s, want %s" % (short(live), short(sha))
    return "ok", "API %s, db %s" % (short(live), data.get("db", "?"))


# ---------------------------------------------------------------------------
# Waiting
# ---------------------------------------------------------------------------

BACKEND_FATAL = {"failed"}


def wait_for_deploy(
    frontend,
    backend,
    target: str,
    timeout: int,
    poll: int,
    require_backend: bool,
) -> bool:
    log("")
    log("[check] waiting for commit %s to be live" % short(target))
    log("")

    deadline = time.time() + timeout
    last = {}
    state = {}
    checked = {"frontend": 0, "backend": 0}

    while True:
        with ThreadPoolExecutor(max_workers=2) as pool:
            frontend_result = pool.submit(frontend, target)
            backend_result = pool.submit(backend, target)
            state["frontend"] = frontend_result.result()
            state["backend"] = backend_result.result()

        for name in ("frontend", "backend"):
            status, message = state[name]
            if last.get(name) != (status, message):
                log("        %-8s %s" % (name + ":", message))
                last[name] = (status, message)
            checked[name] += 1

        frontend_ok = state["frontend"][0] == "ok"
        backend_status = state["backend"][0]
        if require_backend:
            backend_ok = backend_status == "ok"
        else:
            # "down" means the Render service has no live server. That is a
            # configuration gap worth reporting, not a failed site deploy.
            backend_ok = backend_status in ("ok", "down")

        if frontend_ok and backend_ok:
            log("")
            if backend_status == "down" and not require_backend:
                log("[warn] frontend is live, but the API has no live server.")
                log("       Finish the Render setup in DEPLOY-RENDER.md, then run:")
                log("       python scripts/deploy.py --redeploy backend")
            else:
                log("[ok] frontend and backend are serving %s" % short(target))
            return True

        if state["frontend"][0] == "failed" or backend_status in BACKEND_FATAL:
            log("")
            log("[fail] a deploy finished unsuccessfully")
            log("        frontend: %s" % state["frontend"][1])
            log("        backend:  %s" % state["backend"][1])
            return False

        if time.time() >= deadline:
            waited = "%d min" % (timeout // 60) if timeout >= 60 else "%d s" % timeout
            log("")
            log("[fail] timed out after %s" % waited)
            log("        frontend: %s" % state["frontend"][1])
            log("        backend:  %s" % state["backend"][1])
            log("        Open the GitHub Actions or Render dashboard for details.")
            return False

        time.sleep(poll)


# ---------------------------------------------------------------------------
# Git
# ---------------------------------------------------------------------------

def preflight(branch: str) -> str:
    if not (REPO / ".git").exists():
        raise DeployError("%s is not a git repository" % REPO)

    current = git_output("rev-parse", "--abbrev-ref", "HEAD")
    if current != branch:
        raise DeployError(
            "You are on branch '%s' but this deploys '%s'. "
            "Switch with: git switch %s" % (current, branch, branch)
        )

    if run_git("remote", "get-url", "origin", check=False).returncode != 0:
        raise DeployError("No 'origin' remote is configured")

    # Refresh the tracking ref so the ahead/behind counts are honest. A branch
    # that does not exist on origin yet is fine - the push creates it.
    fetch = run_git("fetch", "--quiet", "origin", branch, check=False)
    if fetch.returncode != 0:
        exists = run_git(
            "ls-remote", "--exit-code", "--heads", "origin", branch, check=False
        )
        if exists.returncode not in (0, 2):
            log("[warn] could not reach origin - using the last known state")

    return current


def commit_if_needed(message: str | None, interactive: bool, dry_run: bool) -> bool:
    status = git_output("status", "--porcelain")
    if not status:
        return False

    changed = len([line for line in status.splitlines() if line.strip()])
    if not message:
        raise DeployError(
            "%d uncommitted change(s). Either commit them first or pass a "
            "message:\n    python scripts/deploy.py -m \"what changed\""
            % changed
        )

    if dry_run:
        log("[git] would commit %d file(s): %s" % (changed, message))
        return True

    if not interactive:
        raise DeployError("Refusing to commit in non-interactive mode without review")

    run_git("add", "-A")
    run_git("commit", "-m", message)
    log("[git] committed %d file(s): %s" % (changed, message))
    return True


def push_branch(branch: str, dry_run: bool) -> bool:
    """Push, returning True when the remote actually moves."""
    tracking = "origin/%s" % branch
    known = run_git("rev-parse", "--verify", "--quiet", tracking, check=False)
    if known.returncode != 0:
        log("[git] %s does not exist on origin yet - the push will create it" % branch)
        ahead = git_output("rev-list", "--count", "HEAD")
        behind = 0
    else:
        ahead = git_output("rev-list", "--count", "%s..HEAD" % tracking)
        behind = int(git_output("rev-list", "--count", "HEAD..%s" % tracking))

    if behind:
        raise DeployError(
            "origin/%s has commits you do not have. Run 'git pull --rebase' first."
            % branch
        )

    head = short(git_output("rev-parse", "HEAD"))
    if ahead == "0":
        log("[git] nothing to push - origin/%s is already at %s" % (branch, head))
        return False

    if dry_run:
        log("[git] would push %s commit(s) to origin/%s" % (ahead, branch))
        return True

    log("[git] pushing %s commit(s) to origin/%s" % (ahead, branch))
    run_git("push", "origin", branch)
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list) -> int:
    parser = argparse.ArgumentParser(
        description="Deploy the church site and giving API with one command.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
        "  python scripts/deploy.py\n"
        "  python scripts/deploy.py -m \"content: new devotional\"\n"
        "  python scripts/deploy.py --redeploy backend\n",
    )
    parser.add_argument("-m", "--message", help="commit pending changes with this message")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help="deploy branch (default: main)")
    parser.add_argument(
        "--redeploy",
        choices=["all", "frontend", "backend"],
        help="rebuild with Render deploy hooks instead of pushing a new commit",
    )
    parser.add_argument(
        "--frontend",
        choices=["auto", "pages", "stamp"],
        default="auto",
        help="how to verify the site (default: auto)",
    )
    parser.add_argument(
        "--require-backend",
        action="store_true",
        help="fail unless the API is also live and healthy",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="seconds to wait for the deploy (default: 900)",
    )
    parser.add_argument(
        "--poll",
        type=int,
        default=DEFAULT_POLL,
        help="seconds between checks (default: 20)",
    )
    parser.add_argument("--no-wait", action="store_true", help="push but skip verification")
    parser.add_argument("--dry-run", action="store_true", help="show what would happen")
    args = parser.parse_args(argv)

    site_url = setting("SITE_URL", DEFAULT_SITE_URL)
    health_url = setting("API_HEALTH_URL", DEFAULT_API_HEALTH_URL)
    repo = github_repo()

    try:
        preflight(args.branch)

        head = git_output("rev-parse", "HEAD")

        if args.frontend == "pages":
            use_pages = True
        elif args.frontend == "stamp":
            use_pages = False
        else:
            # Prefer the stamped Render build when that site exists; otherwise
            # fall back to the GitHub Pages build for the same commit.
            use_pages = bool(repo) and check_stamp(site_url, head)[0] == "missing"

        if use_pages:
            frontend = lambda sha: check_pages(repo, sha)  # noqa: E731
            frontend_label = "GitHub Pages (%s)" % repo
        else:
            frontend = lambda sha: check_stamp(site_url, sha)  # noqa: E731
            frontend_label = "Render static site (%s)" % site_url
        backend = lambda sha: check_api(health_url, sha)  # noqa: E731

        if args.redeploy:
            wanted = (
                ["frontend", "backend"] if args.redeploy == "all" else [args.redeploy]
            )
            hooks = {
                "frontend": setting("RENDER_DEPLOY_HOOK_FRONTEND"),
                "backend": setting("RENDER_DEPLOY_HOOK_BACKEND"),
            }
            missing = [name for name in wanted if not hooks[name]]
            if missing:
                raise DeployError(
                    "No deploy hook configured for: %s. Add it to .env.deploy "
                    "(see .env.deploy.example) or deploy with a push instead."
                    % ", ".join(missing)
                )

            if args.dry_run:
                log("[render] would trigger: %s" % ", ".join(wanted))
            else:
                with ThreadPoolExecutor(max_workers=len(wanted)) as pool:
                    for result in pool.map(
                        lambda name: trigger_hook(name, hooks[name], args.branch),
                        wanted,
                    ):
                        log("[render] %s" % result)
        else:
            commit_if_needed(args.message, sys.stdin.isatty(), args.dry_run)
            pushed = push_branch(args.branch, args.dry_run)
            if pushed:
                log("[deploy] one push ships both:")
                log("         frontend -> %s" % frontend_label)
                log("         backend  -> rpai-give-api (%s)" % health_url)
            elif not args.no_wait and not args.dry_run:
                log("[deploy] no new commit - verifying what is already live")

        target = head

        if args.dry_run:
            log("")
            log("[dry-run] nothing was pushed and no hooks were called")
            return 0

        if args.no_wait:
            log("")
            log("[ok] deploy triggered. Verification skipped (--no-wait).")
            return 0

        return (
            0
            if wait_for_deploy(
                frontend,
                backend,
                target,
                args.timeout,
                args.poll,
                args.require_backend,
            )
            else 1
        )

    except DeployError as err:
        log("")
        log("[error] %s" % err)
        return 2
    except KeyboardInterrupt:
        log("")
        log("[stopped] interrupted - the push (if any) already happened")
        return 1


if __name__ == "__main__":
    FILE_ENV.update(load_env_file(REPO / ".env.deploy"))
    sys.exit(main(sys.argv[1:]))
