# CNT-ACC-CART — Cart & Checkout

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Exception

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-CART |
| **Purpose** | Manages shopping carts and checkout sessions for buyers. Validates cart items (prices, availability), calculates totals, and initiates the order creation and saga flow on checkout completion. |
| **Scope Boundary** | Owns cart and checkout session data (temporary). Does NOT own orders (CNT-ACC-ORDERS) or payment logic. |

CONFIRMED (idea.md §8.1): "السلة مساحة مؤقتة قابلة للتعديل، وCheckout جلسة تحقق وحساب وحجز ودفع."
CONFIRMED (idea.md §3.1): "Cart & Checkout — السلة، التحقق من عناصرها، حساب الإجماليات، إنشاء جلسة Checkout."

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-APIGATEWAY | Inbound | Receives add-to-cart, update-cart, initiate-checkout requests |
| CNT-ACC-OFFER | Outbound | Validates current prices and availability for cart items |
| CNT-ACC-IDENTITY | Outbound | Validates buyer identity and session |
| CNT-ACC-ORDERS | Outbound | Creates order on checkout completion |
| CNT-ACC-EVENTBUS | Outbound | Publishes checkout session events |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Session storage | ASSUMPTION | Short-lived sessions suggest Redis or similar ephemeral store |
| Multi-seller support | ACCEPTED-OWNER | Cart groups lines by seller and creates ParentOrder + SellerOrders in MVP; no single-seller restriction |

---

## 4. Data Owned

- Cart records: `{cart_id, buyer_id, items:[{listing_id, quantity, price_snapshot}], created_at, expires_at}`
- Checkout sessions: `{session_id, cart_id, validated_total, shipping_info, reservation_id, expires_at}`

CONFIRMED (idea.md §3.1): "السلال وجلسات الدفع/إتمام الشراء المؤقتة."
CONFIRMED (idea.md §8.3): At order confirmation, an immutable commercial snapshot is written — this is handed off to CNT-ACC-ORDERS, not stored in Cart.

---

## 5. Interfaces

- Provides: Cart management REST API (POST /v1/carts, POST /v1/checkouts) — CONFIRMED (idea.md §6.2)
- Function: FN-ORD-CHECKOUT (`functions/specs/FN-ORD-CHECKOUT.md`)

---

## 6. Failure Modes and Resilience

| Failure | Response |
|---|---|
| Checkout session expires | Cart cleared; buyer must re-initiate (session TTL to be defined — UNKNOWN) |
| Offer validation fails | Checkout blocked; buyer shown updated price/availability |
| Order creation fails after checkout | If no external payment request was dispatched, mark the session failed and allow a safe retry. If authorization/capture may have been dispatched, do not promise “no charge”: persist recovery, reconcile the provider and reservation states, and use only an evidence-backed void/refund or resume path under the selected capture policy. |

---

## 7. Security

- Cart scoped to authenticated buyer only; no cross-buyer cart access — CONFIRMED (idea.md §9)
- Price always read from CNT-ACC-OFFER; client-submitted prices rejected — CONFIRMED (idea.md §9)

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Checkout success rate. CONFIRMED (idea.md §11): "معدل نجاح Checkout" is a monitored business metric |
| Risk | Cart expiry without user awareness is a poor UX; notification strategy needed (PROPOSAL) |

---

## 9. C3 Disposition

**EXCEPTION:** Stateful session service; key behavior documented in `functions/specs/FN-ORD-CHECKOUT.md`. C3 deferred to implementation planning phase. Revisit trigger: when promotions, coupon logic, or multi-seller cart splitting is implemented.
