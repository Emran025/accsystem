# FN-ORDER-001 — validate shipment request

## Ownership and purpose

- System/container/component/module: `SYS-PARCELFLOW` / `CNT-API` / `CMP-API-VALIDATION` / `CODE-API-VALIDATOR`.
- Parent operation: `OP-SHIPMENT-BOOKING`; related decision: `ADR-002` (technology proposal, not acceptance).
- Purpose: determine whether a submitted shipment request satisfies the sample's minimum required fields and dimensions before booking-related side effects.
- Evidence/status: `ASSUMPTION` for the teaching fixture; no production schema or carrier contract is supplied.
- Language/signature: implementation-neutral. Illustrative contract: `validate(request) -> Result<NormalizedShipment, FieldErrors>`; do not treat this as a committed programming-language signature.

## Preconditions and contract

The request object must be present and parseable by the caller's transport layer. The sample does not define exact JSON field names, address formats, dimension units, maximum values, package types, locale normalization, or whether weights are required. These are unresolved input-contract decisions.

Sample validation rules:

1. Origin is present and contains enough information for the eventual booking contract.
2. Destination is present and contains enough information for the eventual booking contract.
3. Each required parcel dimension is numeric and greater than zero.
4. If any rule fails, return a field-specific error identifying the invalid/missing field; do not invoke a carrier or write a booking record.
5. If all known rules pass, return a normalized request value. Exact normalization rules must be specified before implementation; normalization must not silently change user intent.

## Outputs and postconditions

| Outcome | Result semantics | Side effects |
|---|---|---|
| Valid request | Success includes a normalized shipment object suitable for the next orchestration step | None; validation reads the request only |
| Invalid/missing fields | Failure includes one or more stable field-level errors suitable for a client response | None; must not call `EXT-CARRIER` or mutate `CNT-DB` |
| Unparseable/unsupported input | A transport/domain validation error; exact public error code remains unresolved | None |

The function is pure with respect to external systems in the sample: no network call, database write, event publication or booking-state transition is allowed. It has no idempotency or transaction requirement because it performs no side effects. The API's authentication/authorization must occur at an identified boundary; this function does not itself establish the caller's identity.

## Failure and security behavior

- Error messages should identify fields and constraints without echoing sensitive full addresses or exposing internal implementation details.
- Maximum request size, numeric overflow, unsupported character/locale handling, malformed encoding and unknown fields need an explicit API contract; currently `UNKNOWN`.
- Authorization belongs to the API/request boundary, but the identity, role model, tenancy and enforcement mechanism are unresolved.
- Logging must avoid raw addresses and other personal data. Correlation and audit requirements need the security/data policy.

## Verification cases

| Case | Input condition | Expected result | Side-effect assertion |
|---|---|---|---|
| Valid minimum request | Origin, destination and all defined dimensions supplied and positive | Success with normalized value | No carrier/database call |
| Missing origin | Origin absent | Field error for origin | No side effect |
| Missing destination | Destination absent | Field error for destination | No side effect |
| Zero dimension | Any required dimension equals zero | Field error for that dimension | No side effect |
| Negative dimension | Any required dimension is negative | Field error for that dimension | No side effect |
| Non-numeric dimension | Dimension cannot be parsed as a supported number | Stable validation error; public code to be defined | No side effect |
| Boundary/unit cases | Values at supported min/max and each supported unit | Result follows a product-approved constraint | No side effect |
| Multiple invalid fields | More than one rule fails | Deterministic collection/order of field errors | No side effect |
| Sensitive invalid input | Invalid address includes private details | Error identifies field without reflecting sensitive value | No sensitive value in logs |

## Open matters and readiness

| Open item | Impact | Required evidence | Owner/action | Revisit trigger |
|---|---|---|---|---|
| Address schema and normalization | Validation correctness and carrier mapping | Product and provider schema | `OWNER_UNASSIGNED` — appoint API/product owner | Before contract freeze |
| Dimension units/ranges and package types | Acceptance/rejection correctness | Carrier/product limits | `OWNER_UNASSIGNED` — appoint domain owner | Before implementation |
| Public error envelope and compatibility | Client behavior and versioning | API style/version policy | `OWNER_UNASSIGNED` — appoint API owner | Before client integration |
| Identity/tenant and data logging rules | Privacy and access safety | Security/data policy | `OWNER_UNASSIGNED` — appoint security owner | Before pilot |

Implementation readiness: `PARTIAL`. The example establishes a side-effect-free minimum validation intent, not a production-complete contract; the unknown schema/ranges and security boundary must be resolved before claiming implementation readiness.
