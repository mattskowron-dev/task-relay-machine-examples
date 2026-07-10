# pdf_text_consumer

## Exact machine trigger
Machine needs plain text from a public PDF URL

## Exact Task Relay resource
`POST https://task-relay-production.up.railway.app/x402/pdf-text`

## Exact price
0.01 USDC (atomic `10000`)

## Exact request
```json
{
  "url": "https://example.org/document.pdf"
}
```

## Exact automatic machine actions
INGEST_TEXT, SKIP_NO_TEXT, ABORT_FETCH_ERROR

## Optional campaign header
`X-Task-Relay-Campaign: <code>`

## Run (unpaid probe — expects HTTP 402)

```bash
python consumer.py
```
