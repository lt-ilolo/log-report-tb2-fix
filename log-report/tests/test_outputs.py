"""Honest verifier for the log-report task.

Checks the *real outcome*: the report must contain the correct computed values,
not merely exist. Expected values are the known-correct answer for
/app/access.log:

    192.168.0.1  GET  /index.html
    192.168.0.2  GET  /about.html
    192.168.0.1  GET  /index.html
    10.0.0.5     POST /api/login
    192.168.0.2  GET  /index.html
    10.0.0.5     GET  /about.html

  total_requests = 6   (6 request lines)
  unique_ips     = 3   ({192.168.0.1, 192.168.0.2, 10.0.0.5})
  top_path       = "/index.html"   (3 hits vs /about.html 2, /api/login 1)
"""

import json
from pathlib import Path

REPORT = Path("/app/report.json")

EXPECTED_TOTAL_REQUESTS = 6
EXPECTED_UNIQUE_IPS = 3
EXPECTED_TOP_PATH = "/index.html"


def _load_report():
    assert REPORT.exists(), "no /app/report.json found"
    assert REPORT.stat().st_size > 0, "report.json is empty"
    text = REPORT.read_text()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:  # pragma: no cover - message is the point
        raise AssertionError(f"report.json is not valid JSON: {exc}") from exc
    assert isinstance(data, dict), "report.json must be a single JSON object"
    return data


def test_total_requests():
    data = _load_report()
    assert data.get("total_requests") == EXPECTED_TOTAL_REQUESTS, (
        f"total_requests: expected {EXPECTED_TOTAL_REQUESTS}, got {data.get('total_requests')!r}"
    )


def test_unique_ips():
    data = _load_report()
    assert data.get("unique_ips") == EXPECTED_UNIQUE_IPS, (
        f"unique_ips: expected {EXPECTED_UNIQUE_IPS}, got {data.get('unique_ips')!r}"
    )


def test_top_path():
    data = _load_report()
    assert data.get("top_path") == EXPECTED_TOP_PATH, (
        f"top_path: expected {EXPECTED_TOP_PATH!r}, got {data.get('top_path')!r}"
    )
