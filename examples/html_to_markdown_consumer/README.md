# html_to_markdown_consumer

## Exact machine trigger
Machine already holds HTML and needs deterministic Markdown

## Exact Task Relay resource
`POST https://task-relay-production.up.railway.app/x402/html-to-markdown`

## Exact price
0.002 USDC (atomic `2000`)

## Exact request
```json
{
  "html": "<h1>Example</h1><p>Hello</p>"
}
```

## Exact automatic machine actions
PIPE_MARKDOWN, ABORT_EMPTY, HANDLE_TRUNCATION

## Optional campaign header
`X-Task-Relay-Campaign: <code>`

## Run (unpaid probe — expects HTTP 402)

```bash
python consumer.py
```
