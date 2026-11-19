#!/usr/bin/env python3
"""Check release-gate status consistency across manifest and validation reports.

This is a structural status audit. It does not assess architectural truth or quality.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import tempfile
from pathlib import Path

GATES = {"NOT_STARTED", "IN_PROGRESS", "BLOCKED", "PASSED", "WAIVED"}
REPORTS = (
    "validation/traceability-report.md",
    "validation/coverage-report.md",
    "validation/depth-review-report.md",
    "validation/consistency-artifact-validation.md",
    "validation/consistency-review-report.md",
)
REQUIRED_FOR_PASS = (
    "validation/architecture-consistency-ledger.md",
    "validation/diagram-coverage-matrix.md",
    "validation/consistency-review-report.md",
)
OUTPUT = "validation/release-status-audit.md"


def safe_read(root: Path, rel: str) -> tuple[str | None, str | None]:
    candidate = root / rel
    if candidate.is_symlink():
        return None, f"symlink is not allowed: {rel}"
    try:
        resolved = candidate.resolve()
        resolved.relative_to(root)
    except (OSError, ValueError):
        return None, f"missing or escapes project root: {rel}"
    if not resolved.is_file():
        return None, f"required file is missing: {rel}"
    try:
        return resolved.read_text(encoding="utf-8", errors="replace"), None
    except OSError as exc:
        return None, f"cannot read {rel}: {exc}"


def open_findings(text: str) -> list[str]:
    findings=[]
    for line_no, line in enumerate(text.splitlines(), 1):
        stripped=line.strip()
        if re.match(r"[-*]\s*(?:\*\*)?(?:BLOCKER|MAJOR)(?:\*\*)?\s*:", stripped, re.I):
            findings.append(f"line {line_no}: {stripped}")
        elif stripped.startswith("|") and re.search(r"\b(?:BLOCKER|MAJOR)\b", stripped, re.I) and re.search(r"\b(?:OPEN|UNRESOLVED|BLOCKED)\b", stripped, re.I):
            findings.append(f"line {line_no}: {stripped}")
    return findings


def audit(architecture_dir: str | Path) -> dict:
    root=Path(architecture_dir).resolve()
    errors=[]
    manifest_text, err=safe_read(root, "registry/architecture-manifest.json")
    if err: errors.append(err); manifest={}
    else:
        try: manifest=json.loads(manifest_text)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid architecture manifest JSON: {exc}"); manifest={}
    stages=manifest.get("stages", {}) if isinstance(manifest, dict) else {}
    if not isinstance(stages, dict):
        errors.append("manifest stages must be an object"); stages={}
    for name, status in stages.items():
        if status not in GATES: errors.append(f"manifest stage {name} has invalid status {status!r}")

    status_text, err=safe_read(root, "validation/validation-status.md")
    gate_status=None
    if err: errors.append(err)
    else:
        match=re.search(r"^\|\s*Gate\s*7\s*\|[^\n]*?\|\s*\*\*(NOT_STARTED|IN_PROGRESS|BLOCKED|PASSED|WAIVED)\*\*\s*\|", status_text, re.M)
        if match: gate_status=match.group(1)
        else: errors.append("validation-status.md has no parseable Gate 7 status")

    manifest_status=stages.get("validation")
    if gate_status and manifest_status and gate_status != manifest_status:
        errors.append(f"Gate 7 is {gate_status} but manifest validation stage is {manifest_status}")

    findings_by_file={}
    for rel in REPORTS:
        text, read_error=safe_read(root, rel)
        if read_error:
            if rel.endswith("consistency-review-report.md") and gate_status != "PASSED":
                continue
            if rel.endswith("consistency-review-report.md") and gate_status == "PASSED":
                errors.append(read_error)
            continue
        findings=open_findings(text)
        if findings: findings_by_file[rel]=findings
        status_match=re.search(r"\*\*Status:\*\*\s*(PASSED|PARTIAL|BLOCKED)\b", text, re.I)
        if status_match and status_match.group(1).upper()=="PASSED" and findings:
            errors.append(f"{rel} claims PASSED while containing an open BLOCKER/MAJOR finding")
        if rel.endswith("depth-review-report.md") and re.search(r"Overall:\s*\*\*BLOCKED", text, re.I) and gate_status=="PASSED":
            errors.append("Gate 7 is PASSED while depth-review-report is BLOCKED")
        if rel.endswith("consistency-artifact-validation.md") and re.search(r"Status:\s*\*\*BLOCKED\*\*", text, re.I) and gate_status=="PASSED":
            errors.append("Gate 7 is PASSED while consistency-artifact-validation is BLOCKED")

    if gate_status=="PASSED" or manifest_status=="PASSED":
        for rel in REQUIRED_FOR_PASS:
            if not (root/rel).is_file(): errors.append(f"release PASS requires {rel}")
        all_findings=sum(findings_by_file.values(), [])
        if all_findings:
            errors.append("release is marked PASSED despite open BLOCKER/MAJOR findings in validation reports")
        blocked_stages=[name for name,value in stages.items() if name!="validation" and value in {"BLOCKED","IN_PROGRESS","NOT_STARTED"}]
        if blocked_stages:
            errors.append("validation is PASSED while manifest stages remain incomplete: "+", ".join(sorted(blocked_stages)))

    audit_status="BLOCKED" if errors else "CONSISTENT"
    report_lines=["# Release status consistency audit","",f"Audit result: **{audit_status}**",f"Gate 7 report status: **{gate_status or 'UNKNOWN'}**",f"Manifest validation status: **{manifest_status or 'UNKNOWN'}**","",
      "This audit checks only consistency between release status records, selected validation reports and required release artifacts. It does not certify domain correctness, semantic consistency, security, diagram rendering, visual quality or stakeholder acceptance.","", "## Open findings observed",""]
    for rel, items in sorted(findings_by_file.items()):
        report_lines.append(f"### {rel}")
        report_lines.extend(f"- {item}" for item in items)
        report_lines.append("")
    if not findings_by_file: report_lines.append("No explicit open BLOCKER/MAJOR rows found in scanned reports.\n")
    report_lines += ["## Audit findings",""]
    report_lines += [f"- BLOCKER: {item}" for item in errors] if errors else ["- Status records are internally consistent under this audit's limited rules."]
    out=root/OUTPUT
    try:
        if (root/"validation").is_symlink(): raise OSError("validation directory must not be a symlink")
        (root/"validation").mkdir(exist_ok=True)
        if out.is_symlink() or (out.exists() and out.stat().st_nlink > 1):
            raise OSError(f"audit output must not be a symlink or hard-linked file: {OUTPUT}")
        temp_name=None
        try:
            with tempfile.NamedTemporaryFile("w",encoding="utf-8",dir=root/"validation",prefix=".release-audit-",delete=False) as tmp:
                temp_name=tmp.name
                tmp.write("\n".join(report_lines)+"\n")
                tmp.flush()
                os.fsync(tmp.fileno())
            os.replace(temp_name,out)
        except OSError:
            if temp_name:
                try: Path(temp_name).unlink(missing_ok=True)
                except OSError: pass
            raise
    except OSError as exc:
        errors.append(str(exc)); audit_status="BLOCKED"
    return {"status":audit_status,"gate_status":gate_status,"manifest_status":manifest_status,"errors":errors,"report":OUTPUT,"open_findings":sum(map(len,findings_by_file.values()))}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("architecture_dir")
    args=parser.parse_args()
    result=audit(args.architecture_dir)
    print(f"{result['status']}: Gate7={result['gate_status']}; manifest={result['manifest_status']}; open_findings={result['open_findings']}; report={result['report']}")
    for error in result["errors"]: print("- "+error)
    return 1 if result["status"]=="BLOCKED" else 0

if __name__=="__main__":
    raise SystemExit(main())
