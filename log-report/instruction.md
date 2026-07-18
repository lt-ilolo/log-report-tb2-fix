# Access log report

A web-server access log is at `/app/access.log`. Each non-blank line is one request in
Apache "common/combined" format: the client IP address is the first whitespace-separated
field, and the request line is quoted, e.g. `"GET /index.html HTTP/1.1"`.

Analyze the log and write a JSON summary to **`/app/report.json`**. The file must contain
a single JSON object with exactly these three keys:

- `total_requests` (integer) — the number of request lines in the log (ignore blank lines).
- `unique_ips` (integer) — the number of distinct client IP addresses (the first field on each line).
- `top_path` (string) — the request path that appears most often (the path taken from the
  request line, e.g. `/index.html`).

Example shape (values are illustrative, not the answer):

```json
{"total_requests": 42, "unique_ips": 7, "top_path": "/index.html"}
```

## Success criteria

1. `/app/report.json` exists and is a single valid JSON object.
2. `total_requests` equals the number of request lines in `/app/access.log`.
3. `unique_ips` equals the number of distinct client IP addresses in the log.
4. `top_path` equals the most frequently requested path in the log.
