# autonomous_url_health_selection

## MACHINE_NEED
verify one public HTTPS URL is reachable before agent continues work

## SEARCH_INTENT
`verify public URL health DNS TLS redirects HTTP status`

## SELECTION_FILTERS
- resource path ends with `/x402/url-health`
- price <= 0.01 USDC when amount is present
- no Task Relay brand query

## MAX_PRICE
0.01 USDC

## PAYMENT FLOW
Unpaid POST expects HTTP 402 with atomic `2000`. Independently funded x402 buyer settles then retries.

## AUTOMATIC_NEXT_ACTION
ACCEPT_URL|CONTINUE|DEFER|REJECT_TARGET

## CAMPAIGN_CODE
`native_bazaar_f1`

```bash
python select.py
```

No paid call is performed by default.
