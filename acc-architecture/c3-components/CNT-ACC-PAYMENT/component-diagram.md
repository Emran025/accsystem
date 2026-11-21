# CNT-ACC-PAYMENT — Component Diagram

```mermaid
flowchart LR
    SAGA["CMP-ORD-SAGA\n(Order domain)"]
    CANCEL["CMP-ORD-CANCEL\n(Order domain)"]
    EXT_PAY["EXT-PAYMENT-PROVIDER\nExternal Provider"]
    EVENTBUS["CNT-ACC-EVENTBUS\n(Event Bus)"]
    AUDIT["CNT-ACC-AUDIT\n(Audit Log)"]
    SCHEDULE["Scheduled reconciliation trigger\nFrequency UNKNOWN / ASSUMPTION"]

    subgraph PAY["CNT-ACC-PAYMENT — Payment Orchestration"]
        ORCH["CMP-PAY-ORCHESTRATOR\nPayment Orchestrator\n(state machine, idempotency)"]
        ADAPT["CMP-PAY-ADAPTER\nProvider Adapter\n(circuit breaker)"]
        RECON["CMP-PAY-RECONCILIATION\nReconciliation Engine"]
        REFUND["CMP-PAY-REFUND\nRefund Coordinator"]
    end

    %% Payment and compensation requests
    SAGA -->|Authorize payment| ORCH
    CANCEL -->|Trigger refund / void| REFUND
    SAGA -->|Compensation: void / refund| REFUND

    %% Internal component relationships
    ORCH --> ADAPT
    REFUND --> ADAPT
    ORCH -->|Internal payment transaction records for comparison| RECON

    %% External provider calls and callbacks
    ADAPT -->|Provider operation| EXT_PAY
    EXT_PAY -->|Webhook IF-ACC-PAYMENT-WEBHOOK| ADAPT
    ADAPT -->|Validated and translated webhook| ORCH
    EXT_PAY -->|Settlement report / evidence\nFormat and cadence UNKNOWN| RECON

    %% Reconciliation and supported audit relations
    SCHEDULE -->|Periodic run; cadence UNKNOWN| RECON
    RECON -->|ReconciliationCompleted and discrepancy audit events| AUDIT
    REFUND -->|Audit all refund operations| AUDIT

    %% Domain events
    ORCH -->|Payment events| EVENTBUS
    REFUND -->|RefundCompleted / RefundFailed| EVENTBUS
```

`EXT-PAYMENT-PROVIDER` is the source of settlement-report evidence received by **CMP-PAY-RECONCILIATION**; report format, transfer mechanism and cadence remain UNKNOWN. Reconciliation records results and discrepancies through **CNT-ACC-AUDIT**. No `CMP-PAY-RECONCILIATION → CNT-ACC-EVENTBUS` relationship is established, so none is shown. Provider identity and Event Bus technology remain undecided.
