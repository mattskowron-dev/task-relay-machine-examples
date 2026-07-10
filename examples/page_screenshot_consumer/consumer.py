"""Task Relay machine-buyer example — page_screenshot_consumer

EXACT MACHINE TRIGGER: Machine needs fixed-viewport JPEG of a public page
EXACT TASK RELAY RESOURCE: https://task-relay-production.up.railway.app/x402/page-screenshot
EXACT PRICE: 0.1 USDC (atomic 100000)
EXACT REQUEST: see REQUEST_BODY
EXACT STRICT RESULT CONSUMPTION: see consume_result()
EXACT AUTOMATIC MACHINE ACTION: ['STORE_SCREENSHOT', 'INDEX_RENDERED_PAGE_IMAGE', 'ABORT_NAVIGATION_FAILED']
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
RESOURCE = "/x402/page-screenshot"
PRICE_USDC = 0.1
ATOMIC = "100000"
CAMPAIGN = os.environ.get("TASK_RELAY_CAMPAIGN", "example_page_screenshot_consumer_f5")
REQUEST_BODY = {"url": "https://example.com"}


def consume_result(payload: dict) -> str:
    status = (payload.get("result") or {}).get("status") if isinstance(payload.get("result"), dict) else None
    task_status = payload.get("task_status")
    if task_status != "succeeded":
        action = "ABORT_NAVIGATION_FAILED"
    elif status == "captured":
        action = "STORE_SCREENSHOT"
    else:
        action = "ABORT_NAVIGATION_FAILED"
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
            print("automatic_actions_after_paid_result", ['STORE_SCREENSHOT', 'INDEX_RENDERED_PAGE_IMAGE', 'ABORT_NAVIGATION_FAILED'])
            return 0
        print(e.read()[:300])
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
