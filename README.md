# task-relay-machine-examples

Runnable machine-buyer examples for Task Relay F1–F5 x402 jobs.

## Machine consumption model

A machine sends a bounded request, Task Relay performs the bounded job, a strict result returns, and the machine programmatically consumes the result.

## Franchises

| ID | Job | Path | Price USDC | Atomic |
|----|-----|------|------------|--------|
| F1 | URL Health | `/x402/url-health` | 0.002 | 2000 |
| F2 | PDF Text | `/x402/pdf-text` | 0.01 | 10000 |
| F3 | CSV Structure | `/x402/csv-structure` | 0.002 | 2000 |
| F4 | HTML→Markdown | `/x402/html-to-markdown` | 0.002 | 2000 |
| F5 | Page Screenshot | `/x402/page-screenshot` | 0.10 | 100000 |

Public manifest: `GET https://task-relay-production.up.railway.app/.well-known/task-relay.json`

No private keys embedded. No organic-demand claims.
