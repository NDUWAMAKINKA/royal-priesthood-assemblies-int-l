#!/usr/bin/env python3
"""One-command deploy for the RPAI church site and giving API.

The website (Render static site `rpai-church-site`) and the giving API
(Render web service `rpai-give-api`) are built from the same repository, so a
single push to the deploy branch rebuilds both. This script makes that one
step explicit and then *proves* that both services actually shipped the new
commit:

    1. commit any pending changes (only when -m is given)
    2. push the deploy branch
    3. poll the static site's /deploy-info.json and the API's /api/health
       until both report the pushed commit

Run it with no arguments:

    python scripts/deploy.py
    python scripts/deploy.py -m "content: Sunday bulletin"

On a normal machine the helpers are:

    deploy.bat          (Windows)
    ./deploy.sh         (Linux/macOS)

Configuration is optional and read from environment variables or a
`.env.deploy` file in the repository root:

    SITE_URL=https://rpai-church-site.onrender.com
    API_HEALTH_URL=https://rpai-give-api.onrender.com/api/health
    RENDER_DEPLOY_HOOK_FRONTEND=https://api.render.com/deploy/srv-...?key=...
    RENDER_DEPLOY_HOOK_BACKEND=https://api.render.com/deploy/srv-...?key=...

The deploy hooks are only needed for `--redeploy`, which rebuilds the
services without a new commit. Normal deploys rely on Render's automatic
deploy on push, which render.yaml enables for both services.

Exit codes: 0 success, 1 the deploy did not become healthy, 2 preflight error.
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
DEFAULT_SITE_URL = "https://rpai-church-site.onrender.com"
DEFAULT_API_HEALTH_URL = "https://rpai-give-api.onrender.com/api/health"
DEFAULT_TIMEOUT = 15 * 60
POLL_INTERVAL = 10

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT

# Populated from .env.deploy in main(); the real environment always wins.
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


def http_get_json(url: str, timeout: int = 25) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "rpai-deploy/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
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
# Preflight
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

    # Refresh the tracking ref so the ahead/behind counts are honest. A
    # branch that does not exist on origin yet is fine - the push creates it.
    fetch = run_git("fetch", "--quiet", "origin", branch, check=False)
    if fetch.returncode != 0:
        exists = run_git(
            "ls-remote", "--exit-code", "--heads", "origin", branch, check=False
        )
        if exists.returncode not in (0, 2):
            log("[warn] could not reach origin - using the last known state")

    return current


def commit_if_needed(
    message: str | None, interactive: bool, dry_run: bool
) -> bool:
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
    """Push, returning True when the remote actually moved."""
    tracking = "origin/%s" % branch
    known = run_git("rev-parse", "--verify", "--quiet", tracking, check=False)
    if known.returncode != 0:
        log("[git] %s does not exist on origin yet - the push will create it"
            % branch)
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

    if ahead == "0":
        log("[git] nothing to push - origin/%s is already at %s"
            % (branch, short(git_output("rev-parse", "HEAD"))))
        return False

    if dry_run:
        log("[git] would push %s commit(s) to origin/%s" % (ahead, branch))
        return True

    log("[git] pushing %s commit(s) to origin/%s" % (ahead, branch))
    run_git("push", "origin", branch)
    return True


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def check_site(site_url: str, target: str) -> tuple:
    url = "%s/deploy-info.json?t=%d" % (
        site_url.rstrip("/"),
        int(time.time() * 1000),
    )
    try:
        data = http_get_json(url)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return False, "deploy-info.json not found (old build still live)"
        return False, "HTTP %s" % err.code
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        return False, "unreachable (%s)" % getattr(err, "reason", err)
    except json.JSONDecodeError:
        return False, "invalid JSON"

    live = str(data.get("commit", "")).strip()
    if not live:
        return False, "no commit in deploy-info.json"
    if target != "unknown" and live != target:
        return False, "live %s, want %s" % (short(live), short(target))
    return True, "commit %s" % short(live)


def check_api(health_url: str, target: str) -> tuple:
    url = "%s?t=%d" % (health_url, int(time.time() * 1000))
    try:
        data = http_get_json(url)
    except urllib.error.HTTPError as err:
        try:
            payload = json.loads(err.read().decode("utf-8", "replace"))
            reason = payload.get("db")
            if reason in (None, "", "ok"):
                reason = "ok=false"
        except Exception:  # noqa: BLE001 - diagnostic only
            reason = "HTTP %s" % err.code
        return False, "not healthy (%s)" % reason
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        return False, "unreachable (%s)" % getattr(err, "reason", err)
    except json.JSONDecodeError:
        return False, "invalid JSON"

    if not data.get("ok"):
        return False, "health check reported ok=false"
    live = str(data.get("commit", "unknown")).strip()
    if target != "unknown" and live not in ("", "unknown") and live != target:
        return False, "live %s, want %s" % (short(live), short(target))
    return True, "commit %s, db %s" % (short(live), data.get("db", "?"))


def wait_for_deploy(site_url: str, health_url: str, target: str, timeout: int) -> bool:
    log("")
    log("[check] waiting for both services to serve %s" % short(target))
    log("        site: %s" % site_url)
    log("        api:  %s" % health_url)
    log("")

    deadline = time.time() + timeout
    last_site = last_api = None
    site_ok = api_ok = False

    while True:
        with ThreadPoolExecutor(max_workers=2) as pool:
            site_future = pool.submit(check_site, site_url, target)
            api_future = pool.submit(check_api, health_url, target)
            site_ok, site_state = site_future.result()
            api_ok, api_state = api_future.result()

        if site_state != last_site:
            log("        frontend: %s" % site_state)
            last_site = site_state
        if api_state != last_api:
            log("        backend:  %s" % api_state)
            last_api = api_state

        if site_ok and api_ok:
            log("")
            log("[ok] frontend and backend both serve %s" % short(target))
            return True

        if time.time() >= deadline:
            waited = (
                "%d min" % (timeout // 60) if timeout >= 60 else "%d s" % timeout
            )
            log("")
            log("[fail] timed out after %s" % waited)
            log("        frontend: %s" % site_state)
            log("        backend:  %s" % api_state)
            log("        Open the Render dashboard and check both service logs.")
            return False

        time.sleep(POLL_INTERVAL)


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
        "  python scripts/deploy.py --redeploy frontend\n",
    )
    parser.add_argument("-m", "--message", help="commit pending changes with this message")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help="deploy branch (default: main)")
    parser.add_argument(
        "--redeploy",
        choices=["all", "frontend", "backend"],
        help="rebuild with Render deploy hooks instead of pushing a new commit",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="seconds to wait for both services (default: 900)",
    )
    parser.add_argument("--no-wait", action="store_true", help="push but skip verification")
    parser.add_argument("--dry-run", action="store_true", help="show what would happen")
    args = parser.parse_args(argv)

    site_url = setting("SITE_URL", DEFAULT_SITE_URL)
    health_url = setting("API_HEALTH_URL", DEFAULT_API_HEALTH_URL)
    hook_frontend = setting("RENDER_DEPLOY_HOOK_FRONTEND")
    hook_backend = setting("RENDER_DEPLOY_HOOK_BACKEND")

    try:
        preflight(args.branch)

        if args.redeploy:
            wanted = (
                ["frontend", "backend"]
                if args.redeploy == "all"
                else [args.redeploy]
            )
            hooks = {"frontend": hook_frontend, "backend": hook_backend}
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

            target = git_output("rev-parse", "HEAD")
        else:
            interactive = sys.stdin.isatty()
            commit_if_needed(args.message, interactive, args.dry_run)
            pushed = push_branch(args.branch, args.dry_run)
            target = git_output("rev-parse", "HEAD")

            if pushed:
                log("[render] push triggers both services (autoDeployTrigger: commit)")
                log("         rpai-give-api   (backend)")
                log("         rpai-church-site (frontend)")
            elif not args.no_wait and not args.dry_run:
                log("[render] no new commit - verifying what is already live")

        if args.dry_run:
            log("")
            log("[dry-run] no changes were pushed and no hooks were called")
            return 0

        if args.no_wait:
            log("")
            log("[ok] deploy triggered. Verification skipped (--no-wait).")
            return 0

        return 0 if wait_for_deploy(site_url, health_url, target, args.timeout) else 1

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
