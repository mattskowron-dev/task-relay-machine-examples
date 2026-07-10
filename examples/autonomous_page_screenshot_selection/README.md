# autonomous_page_screenshot_selection

## MACHINE_NEED
capture a fixed-viewport JPEG of a public page for rendered-page indexing

## SEARCH_INTENT
`capture website page screenshot JPEG viewport`

## SELECTION_FILTERS
- resource path ends with `/x402/page-screenshot`
- price <= 0.25 USDC when amount is present
- no Task Relay brand query

## MAX_PRICE
0.25 USDC

## PAYMENT FLOW
Unpaid POST expects HTTP 402 with atomic `100000`. Independently funded x402 buyer settles then retries.

## AUTOMATIC_NEXT_ACTION
INDEX_RENDERED_PAGE_IMAGE

## CAMPAIGN_CODE
`native_bazaar_f5`

```bash
python select.py
```

No paid call is performed by default.
