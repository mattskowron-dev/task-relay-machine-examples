"""Task Relay machine-buyer example — html_to_markdown_consumer

EXACT MACHINE TRIGGER: Machine already holds HTML and needs deterministic Markdown
EXACT TASK RELAY RESOURCE: https://task-relay-production.up.railway.app/x402/html-to-markdown
EXACT PRICE: 0.002 USDC (atomic 2000)
EXACT REQUEST: see REQUEST_BODY
EXACT STRICT RESULT CONSUMPTION: see consume_result()
EXACT AUTOMATIC MACHINE ACTION: ['PIPE_MARKDOWN', 'ABORT_EMPTY', 'HANDLE_TRUNCATION']
OPTIONAL HEADER: X-Task-Relay-Campaign

Secrets via environment only. Unpaid POST expects HTTP 402.
No embedded private keys. No organic-demand claims.
"""
from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request

BASE = os.environ.get("TASK_RELAY_BASE_URL", "https://task-relay-production.up.railway.app").rstrip("/")
RESOURCE = "/x402/html-to-markdown"
PRICE_USDC = 0.002
ATOMIC = "2000"
CAMPAIGN = os.environ.get("TASK_RELAY_CAMPAIGN", "example_html_to_markdown_consumer_f4")
REQUEST_BODY = {"html": "<h1>Example</h1><p>Hello</p>"}


def consume_result(payload: dict) -> str:
    status = (payload.get("result") or {}).get("status") if isinstance(payload.get("result"), dict) else None
    task_status = payload.get("task_status")
    if task_status != "succeeded":
        action = "ABORT_EMPTY"
    elif status == "converted":
        action = "PIPE_MARKDOWN"
    elif status == "partial":
        action = "HANDLE_TRUNCATION"
    else:
        action = "ABORT_EMPTY"
    return action


def main() -> int:
    url = BASE + RESOURCE
    data = json.dumps(REQUEST_BODY).encode("utf-8")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if CAMPAIGN:
        headers["X-Task-Relay-Campaign"] = CAMPAIGN
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            print("UNEXPECTED_SUCCESS_STATUS", resp.status)
            print(resp.read()[:500])
            return 2
    except urllib.error.HTTPError as e:
        print("HTTP", e.code)
        print("resource", url)
        print("price_usdc", PRICE_USDC, "atomic", ATOMIC)
        print("campaign", CAMPAIGN or None)
        pr = e.headers.get("payment-required") or e.headers.get("Payment-Required")
        if pr:
            try:
                j = json.loads(base64.b64decode(pr + "=="))
                amt = j.get("accepts", [{}])[0].get("amount")
                print("payment_required_amount", amt, "expected", ATOMIC, "ok", str(amt) == ATOMIC)
            except Exception as ex:
                print("payment_required_decode_note", type(ex).__name__)
        if e.code == 402:
            print("EXPECTED_UNPAID_402")
            print("automatic_actions_after_paid_result", ['PIPE_MARKDOWN', 'ABORT_EMPTY', 'HANDLE_TRUNCATION'])
            return 0
        print(e.read()[:300])
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
