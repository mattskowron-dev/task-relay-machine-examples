# autonomous_html_markdown_selection

## MACHINE_NEED
convert HTML already held by the machine into deterministic Markdown

## SEARCH_INTENT
`convert HTML to Markdown`

## SELECTION_FILTERS
- resource path ends with `/x402/html-to-markdown`
- price <= 0.01 USDC when amount is present
- no Task Relay brand query

## MAX_PRICE
0.01 USDC

## PAYMENT FLOW
Unpaid POST expects HTTP 402 with atomic `2000`. Independently funded x402 buyer settles then retries.

## AUTOMATIC_NEXT_ACTION
ACCEPT_MARKDOWN|INDEX_MARKDOWN

## CAMPAIGN_CODE
`native_bazaar_f4`

```bash
python select.py
```

No paid call is performed by default.
