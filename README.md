# log-report — fixed Terminal-Bench 2 (Harbor) task

Repaired version of the broken `log-report` task. The underlying task is simple
(parse an Apache-style access log into a small JSON report); the work was fixing
the broken task *authoring* so the task is correct, reproducible, and graded honestly.

## Verified

```
harbor run -p log-report -a oracle     # reward 1.0  (reference solution PASSES)
harbor run -p log-report --agent nop   # reward 0.0  (no-op agent FAILS)
```

Verifier writes `/logs/verifier/reward.txt` and `/logs/verifier/ctrf.json`
(ctrf: 3 tests, 3 passed).

## Defects found and fixed

| # | Defect | Fix |
|---|--------|-----|
| 1 | `task.toml` `artifacts` was a **string** and pointed at the wrong file (`/app/out.json`) | `artifacts = ["/app/report.json"]` (array, correct file); added `schema_version = "1.3"` |
| 2 | `environment/Dockerfile` used **unpinned** `python:latest` | Pinned by digest: `python:3.12-slim@sha256:57cd7c3a…` |
| 3 | Agent image **leaked the reference solution** (`COPY solution_hint.py`) | Removed the file and the `COPY`; agent gets only `access.log` |
| 4 | Verifier was **gameable** — only checked that `report.json` exists / is non-empty | Verifier now asserts the real values (`total_requests=6`, `unique_ips=3`, `top_path=/index.html`) and JSON-object shape |
| 5 | `tests/test.sh` wrote reward to `/app/reward.txt` and produced **no ctrf.json** | Writes `/logs/verifier/reward.txt` and emits `/logs/verifier/ctrf.json` via `pytest --ctrf` |
| 6 | `instruction.md` was **ambiguous** and inconsistent with the verifier | Rewritten with the exact output path, JSON schema, and numbered success criteria matching the verifier |

Not defects (distractors): the access log is clean; the task needs no runtime
network; the oracle already computed the correct answer; `memory_mb = 2048` is ample.

## Note on `network_mode`

The task needs no internet (verifier deps are baked into the image). Ideally this
would be `no-network`, but the local Docker environment provider cannot enforce a
no-network policy and rejects such tasks, so the task uses the provider-supported
`network_mode = "public"`. Reproducibility is guaranteed by the digest-pinned base
image, not by the network policy.
