#!/bin/bash
# Oracle entrypoint. Runs the reference implementation, which reads /app/access.log
# and writes the summary to /app/report.json.
set -euo pipefail

python3 /solution/solve.py
