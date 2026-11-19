# Configurable Policy and Launch-Gate Register

| Policy | Safe baseline | Configured by | Gate |
|---|---|---|---|
| Reservation hold/connector timeouts | configurable; unknown is not success | operations | workload and recovery test |
| Capture timing | seller/agreement policy, constrained by platform/provider/risk | product/finance/risk | provider and finance review |
| Tax/currency | versioned tax lines and exchange-rate snapshots | finance/tax | jurisdiction review |
| Accounting trigger | order confirmed default notification; posting only by institution policy | institution finance owner | contract/configuration review |
| Returns/cancellation/disputes | explicit state machine, commercial rules deferred | product/finance/legal | policy approval |
| Delivery provider | internal fleet first; local provider wins when available | operations | operational acceptance |
| License plans/offline grace | signed token, configurable validation/grace, fail-safe restriction | product/security | license policy approval |
| Support access | institution/purpose scoped, least privilege, read-only default, audited | security/support | access-control review |
| Retention/residency/PCI | jurisdiction-neutral minimization and export/deletion controls | legal/compliance | mandatory launch gate |
| SLA/RTO/RPO/capacity | named fields and measurement definitions, no invented numbers | operations | capacity and DR gates |
