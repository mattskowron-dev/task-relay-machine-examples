# csv_structure_consumer

## Exact machine trigger
Machine must ingest public CSV into structured rows

## Exact Task Relay resource
`POST https://task-relay-production.up.railway.app/x402/csv-structure`

## Exact price
0.002 USDC (atomic `2000`)

## Exact request
```json
{
  "url": "https://example.org/data.csv"
}
```

## Exact automatic machine actions
LOAD_ROWS, ABORT_INVALID_CSV, TRUNCATE_AWARE_CONTINUE

## Optional campaign header
`X-Task-Relay-Campaign: <code>`

## Run (unpaid probe — expects HTTP 402)

```bash
python consumer.py
```
