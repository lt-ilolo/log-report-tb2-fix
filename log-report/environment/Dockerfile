# Base image pinned by digest for a reproducible build (python:3.12-slim).
FROM python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de

# Verifier dependencies are baked in so grading needs no network at runtime.
RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

WORKDIR /app

# Only the task input is placed in the agent environment.
# NOTE: no solution/reference file is copied here — the agent must not see the answer.
COPY access.log /app/access.log
