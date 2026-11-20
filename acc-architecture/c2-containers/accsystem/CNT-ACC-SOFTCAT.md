# CNT-ACC-SOFTCAT — Software Catalog & Release Distribution

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Exception (Conditional)

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-SOFTCAT |
| **Purpose** | Manages the catalog of ACC software products, their versions, release channels, platform requirements, release notes, and package download links. Provides public HTTPS links, including policy-permitted anonymous signed links, or authorized signed, time-limited links for restricted installation packages stored in EXT-PACKAGE-CDN, according to asset access policy. |
| **Scope Boundary** | Owns release metadata, version catalog, and download link generation. Does NOT store binary files (EXT-PACKAGE-CDN). |

CONFIRMED (idea.md §3.1): "Software Catalog & Release Distribution — إدارة كتالوج منتجات ACC وإصداراتها ومتطلبات التشغيل وملاحظات الإصدار، وإتاحة تنزيل الحزم عبر روابط عامة أو موقعة ومحددة الصلاحية."

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACM-PUBLIC | Inbound | Public catalog browsing and download link requests (IF-ACC-SOFTDL) |
| CNT-ACM-ADMIN | Inbound | Admin console for publishing new releases and managing versions |
| EXT-PACKAGE-CDN | Outbound | Provides public HTTPS or authorized signed, time-limited URLs to CDN-hosted packages as appropriate |
| CNT-ACC-EVENTBUS | Outbound | Publishes SoftwareReleasePublished/Withdrawn events |
| CNT-ACC-AUDIT | Outbound | Logs all release publish/withdraw and download events |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Package storage | CONFIRMED (idea.md §3.1) | Object Storage/CDN (EXT-PACKAGE-CDN) |
| Signed URLs | CONFIRMED (idea.md §3.1) | Time-limited signed download URLs |
| Package integrity | CONFIRMED (idea.md §7.7) | SHA-256 checksum and digital signature per package |

---

## 4. Data Owned

- Product/system catalog records: `{product_code, name, description, current_version, release_channels}`
- Release records: `{release_id, product_code, version, channel, platform_targets, requirements, release_notes, sha256, signature, cdn_object_key, published_at}`
- Download link generation logs

CONFIRMED (idea.md §3.1): "بيانات الأنظمة والإصدارات وقنوات الإصدار والملفات الوصفية وبصمات التحقق."
CONFIRMED (idea.md §3.1): "أما ملفات الحزم فتخزن في Object Storage/CDN."

---

## 5. Interfaces

- **IF-ACC-SOFTDL** (provider): Download URL generation and product catalog query. Consumers: CNT-ACM-PUBLIC, ACT-VISITOR, ACT-INST-ADMIN
- Publishes: SoftwareReleasePublished/Withdrawn events

---

## 6. Failure Modes

| Failure | Response |
|---|---|
| CDN unavailable | Affected public or signed package download unavailable; alert operations |
| Package integrity check fails | Do not publish release; log error; alert platform team |
| Signed download link expired | Authorized requester obtains a fresh signed URL under policy |

---

## 7. Security

- CONFIRMED (idea.md §7.7): "التحقق من سلامة الحزمة وتوقيعها قبل التثبيت أو التحديث"
- CONFIRMED (idea.md §9): Digital signature per package, SHA-256 published per release, HTTPS download links
- CONFIRMED (idea.md §3.1): "لا ينبغي أن تكون ملفات التثبيت منطقاً مخزناً داخل واجهة ACManagement نفسها"

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | CONFIRMED (idea.md §11): "عدد التنزيلات، نجاح/فشل التنزيل، الإصدارات النشطة والمسحوبة، سلامة الحزم" |

---

## 9. C3 Disposition

**EXCEPTION (Conditional):** Key workflows documented in `supporting-views/dynamic-license-flow.md` and `supporting-views/dynamic-publication-flow.md`. C3 conditional — revisit when release-signing pipeline design is planned (Phase 1 of implementation).
