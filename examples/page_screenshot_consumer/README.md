# page_screenshot_consumer

## Exact machine trigger
Machine needs fixed-viewport JPEG of a public page

## Exact Task Relay resource
`POST https://task-relay-production.up.railway.app/x402/page-screenshot`

## Exact price
0.1 USDC (atomic `100000`)

## Exact request
```json
{
  "url": "https://example.com"
}
```

## Exact automatic machine actions
STORE_SCREENSHOT, INDEX_RENDERED_PAGE_IMAGE, ABORT_NAVIGATION_FAILED

## Optional campaign header
`X-Task-Relay-Campaign: <code>`

## Run (unpaid probe — expects HTTP 402)

```bash
python consumer.py
```
