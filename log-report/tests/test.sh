#!/bin/bash
# Verifier entrypoint. Copied to /tests/test.sh and run in the environment container
# after the agent finishes.
#
# pytest + pytest-json-ctrf are baked into the environment image
# (environment/Dockerfile), so grading requires no network access.
#
# Reports results the way Harbor expects:
#   - a CTRF report at /logs/verifier/ctrf.json
#   - the reward (1 pass / 0 fail) at /logs/verifier/reward.txt

mkdir -p /logs/verifier

pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA
status=$?

if [ "$status" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi

exit "$status"
