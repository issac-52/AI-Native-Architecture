# Identical agent task prompts (A and B)

Give the **same text** to the agent for each variant. Do not include directory hints.

## T01 — validation
"Reject order quantities larger than 100 with HTTP 400 and show a helpful UI error. Keep 1–100 valid."
Oracle: 0 -> 400, 1/100 -> 201, 101 -> 400, UI error visible.

## T02 — search
"Add case-insensitive product-name order search; empty search returns all orders. Do not break create/cancel."
Oracle: filtered/unfiltered responses and UI checks.

## T03 — API contract evolution
"Include a stable ISO-8601 createdAt timestamp with every order response and display it in the UI."
Oracle: same timestamp for same order across endpoints.

## T04 — cancellation error
"Reject cancellation of shipped orders with HTTP 409, while keeping cancelled-order requests idempotent."
Oracle requires a shipped-state fixture.

## T05 — cross-domain (future)
"On cancellation, request refund and inventory restoration exactly once."
**Blocked:** first introduce real payment and inventory domains with failure injection.
