#!/usr/bin/env sh
# One-command deploy: pushes the site and API, then waits until both are live.
# Usage:  ./deploy.sh
#         ./deploy.sh -m "content: new devotional"
set -e
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$here/scripts/deploy.py" "$@"
fi

if command -v python >/dev/null 2>&1; then
  exec python "$here/scripts/deploy.py" "$@"
fi

echo "Python 3 is required to deploy. Install it from https://python.org" >&2
exit 2
