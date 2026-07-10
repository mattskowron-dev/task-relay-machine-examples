# autonomous_csv_structure_selection

## MACHINE_NEED
parse a public CSV URL into ordered rows for a load step

## SEARCH_INTENT
`convert CSV URL to JSON rows`

## SELECTION_FILTERS
- resource path ends with `/x402/csv-structure`
- price <= 0.01 USDC when amount is present
- no Task Relay brand query

## MAX_PRICE
0.01 USDC

## PAYMENT FLOW
Unpaid POST expects HTTP 402 with atomic `2000`. Independently funded x402 buyer settles then retries.

## AUTOMATIC_NEXT_ACTION
LOAD_ROWS

## CAMPAIGN_CODE
`native_bazaar_f3`

```bash
python select.py
```

No paid call is performed by default.
