# url_health_consumer

## Exact machine trigger
Machine must gate work on one public URL reachability

## Exact Task Relay resource
`POST https://task-relay-production.up.railway.app/x402/url-health`

## Exact price
0.002 USDC (atomic `2000`)

## Exact request
```json
{
  "url": "https://example.com"
}
```

## Exact automatic machine actions
CONTINUE, DEFER, REJECT_TARGET

## Optional campaign header
`X-Task-Relay-Campaign: <code>`

## Run (unpaid probe — expects HTTP 402)

```bash
python consumer.py
```
