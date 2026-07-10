"""Autonomous need-first selection example — F3

MACHINE_NEED: parse a public CSV URL into ordered rows for a load step
SEARCH_INTENT: convert CSV URL to JSON rows
SELECTION_FILTERS: exact resource path match preferred; price <= MAX_PRICE; required request/result facts
MAX_PRICE: 0.01
REQUIRED_REQUEST_FACTS: ['url']
REQUIRED_RESULT_FACTS: ['status', 'rows', 'dialect']
PAYMENT FLOW: unpaid probe expects HTTP 402; independently funded buyer settles x402 then retries
AUTOMATIC_NEXT_ACTION: LOAD_ROWS
CAMPAIGN_CODE: native_bazaar_f3

Does NOT search Task Relay brand / merchant / franchise names.
No paid call in this example.
"""
from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request

SEARCH = "https://api.cdp.coinbase.com/platform/v2/x402/discovery/search"
MANIFEST = "https://task-relay-production.up.railway.app/.well-known/task-relay.json"
CATALOG = (
    "https://raw.githubusercontent.com/mattskowron-dev/task-relay-machine-examples/"
    "main/machine-discovery/task-relay-machine-jobs.json"
)
MACHINE_NEED = 'parse a public CSV URL into ordered rows for a load step'
SEARCH_INTENT = 'convert CSV URL to JSON rows'
MAX_PRICE = 0.01
PATH_HINT = '/x402/csv-structure'  # structural filter only — not a brand query
CAMPAIGN = os.environ.get("TASK_RELAY_CAMPAIGN", 'native_bazaar_f3')
REQUEST_BODY = {"url": "https://example.org/data.csv"}
ATOMIC = '2000'


def bazaar_search(intent: str) -> list[dict]:
    params = urllib.parse.urlencode(
        {"query": intent, "network": "eip155:8453", "scheme": "exact", "limit": 20}
    )
    req = urllib.request.Request(f"{SEARCH}?{params}", headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    return list(data.get("resources") or [])


def mechanical_select(candidates: list[dict]) -> dict | None:
    qualified = []
    for c in candidates:
        res = c.get("resource") or ""
        # accept only exact path suffix match for this job class
        if not res.endswith(PATH_HINT):
            continue
        # price from metadata when present
        price = None
        accepts = c.get("accepts") or c.get("payment") or []
        if isinstance(accepts, list) and accepts:
            amt = accepts[0].get("amount") if isinstance(accepts[0], dict) else None
            if amt and str(amt).isdigit():
                price = int(amt) / 1_000_000
        if price is not None and price > MAX_PRICE:
            continue
        qualified.append(c)
    return qualified[0] if qualified else None


def unpaid_probe(resource_url: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Task-Relay-Campaign": CAMPAIGN,
    }
    req = urllib.request.Request(
        resource_url, data=json.dumps(REQUEST_BODY).encode(), headers=headers, method="POST"
    )
    try:
        urllib.request.urlopen(req, timeout=30)
        return {"http": "unexpected_success"}
    except urllib.error.HTTPError as e:
        pr = e.headers.get("payment-required")
        amt = None
        if pr:
            try:
                j = json.loads(base64.b64decode(pr + "=="))
                amt = j.get("accepts", [{}])[0].get("amount")
            except Exception:
                pass
        return {"http": e.code, "amount": amt, "expected_atomic": ATOMIC}


def main() -> int:
    print("MACHINE_NEED", MACHINE_NEED)
    print("SEARCH_INTENT", SEARCH_INTENT)
    candidates = bazaar_search(SEARCH_INTENT)
    print("CANDIDATE_COUNT", len(candidates))
    selected = mechanical_select(candidates)
    if not selected:
        # fallback: public machine catalog (still not a brand search string)
        try:
            with urllib.request.urlopen(CATALOG, timeout=20) as resp:
                cat = json.loads(resp.read().decode())
            for f in cat.get("franchises") or []:
                if (f.get("resource_path") or "").endswith(PATH_HINT):
                    selected = {"resource": f.get("resource"), "from": "github_job_catalog"}
                    break
        except Exception as ex:
            print("catalog_fallback_error", type(ex).__name__)
    print("SELECTED", selected)
    if not selected:
        print("NO_MATCH — independently funded buyer would not pay")
        return 2
    resource = selected.get("resource")
    print("PAYMENT_FLOW", "x402 exact scheme on Base; unpaid probe next")
    print("probe", unpaid_probe(resource))
    print("AUTOMATIC_NEXT_ACTION_AFTER_PAID_RESULT", 'LOAD_ROWS')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
