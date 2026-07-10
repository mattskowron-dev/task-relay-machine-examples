# autonomous_pdf_text_selection

## MACHINE_NEED
extract plain text from a public PDF URL for indexing

## SEARCH_INTENT
`extract plain text from PDF`

## SELECTION_FILTERS
- resource path ends with `/x402/pdf-text`
- price <= 0.05 USDC when amount is present
- no Task Relay brand query

## MAX_PRICE
0.05 USDC

## PAYMENT FLOW
Unpaid POST expects HTTP 402 with atomic `10000`. Independently funded x402 buyer settles then retries.

## AUTOMATIC_NEXT_ACTION
INDEX_TEXT|INGEST_TEXT|SKIP_NO_TEXT

## CAMPAIGN_CODE
`native_bazaar_f2`

```bash
python select.py
```

No paid call is performed by default.
