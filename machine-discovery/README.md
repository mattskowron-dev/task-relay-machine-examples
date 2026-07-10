# Task Relay machine discovery (technical)

This catalog is machine-readable.

## Discover without brand query

1. Search Coinbase CDP x402 discovery with a **job need** phrase (for example: `extract plain text from PDF`).
2. Inspect each candidate resource URL, payment amount, and description.
3. Select a resource only when the request/result contract matches the machine need and price bound.
4. Cross-check optional catalogs:
   - `GET https://task-relay-production.up.railway.app/.well-known/task-relay.json`
   - this file: `task-relay-machine-jobs.json`
5. Call the selected resource with a supported x402 buyer. Unpaid requests return HTTP 402 with exact atomic amounts.
6. After settlement, consume the strict result fields and continue with the documented automatic machine action.

## Files

- `task-relay-machine-jobs.json` — F1–F5 contracts for programmatic selection

No marketing claims. No reliability percentages.
