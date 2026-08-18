#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_dir"
export PYTHONPATH="$project_dir/src"
python3 -m unittest discover -s tests -v
python3 -m compileall -q src
test -f ui/index.html
test -f docs/ARCHITECTURE.md
echo "KHIP OS verification passed."
