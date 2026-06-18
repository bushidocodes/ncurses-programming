#!/usr/bin/env bash
# Build the examples and run the TUI test suite.
#
# Must run where tmux and the ncurses runtime exist. On Windows, invoke from
# WSL, e.g.:  wsl -e bash tests/run.sh
set -euo pipefail

for tool in tmux python3 make gcc; do
    command -v "$tool" >/dev/null 2>&1 || {
        echo "error: '$tool' not found on PATH" >&2
        exit 1
    }
done

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

exec python3 -m unittest discover -s tests -p 'test_*.py' -v "$@"
