"""Discover Task Relay on CDP x402 Bazaar, then unpaid-call for 402 shape.

Does not build a Task Relay MCP server.
"""
from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request

SEARCH = "https://api.cdp.coinbase.com/platform/v2/x402/discovery/search"
BASE = os.environ.get("TASK_RELAY_BASE_URL", "https://task-relay-production.up.railway.app").rstrip("/")
QUERIES = [
    "verify public URL health DNS TLS redirects HTTP status",
    "extract plain text from PDF",
    "convert CSV URL to JSON rows",
    "convert HTML to Markdown",
    "capture website page screenshot JPEG viewport",
]


def search(q: str):
    params = urllib.parse.urlencode({"query": q, "network": "eip155:8453", "scheme": "exact", "limit": 10})
    req = urllib.request.Request(f"{SEARCH}?{params}", headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def unpaid_probe(resource_url: str, body: dict, campaign: str | None = None):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if campaign:
        headers["X-Task-Relay-Campaign"] = campaign
    req = urllib.request.Request(resource_url, data=json.dumps(body).encode(), headers=headers, method="POST")
    try:
        urllib.request.urlopen(req, timeout=30)
        return {"http": "200_unexpected"}
    except urllib.error.HTTPError as e:
        pr = e.headers.get("payment-required")
        amt = None
        if pr:
            try:
                j = json.loads(base64.b64decode(pr + "=="))
                amt = j.get("accepts", [{}])[0].get("amount")
            except Exception:
                pass
        return {"http": e.code, "amount": amt}


def main():
    found = []
    for q in QUERIES:
        try:
            data = search(q)
        except Exception as ex:
            print("search_fail", q, type(ex).__name__)
            continue
        for r in data.get("resources") or []:
            res = r.get("resource") or ""
            if "task-relay-production.up.railway.app" in res:
                found.append({"query": q, "resource": res})
    print(json.dumps({"task_relay_hits": found}, indent=2))
    target = found[0]["resource"] if found else BASE + "/x402/url-health"
    print("unpaid_probe", unpaid_probe(target, {"url": "https://example.com"}, "bazaar_discovery_example_f1"))


if __name__ == "__main__":
    main()
