#!/usr/bin/env python3
"""Validate and query the ACC execution-phase requirement registry.

The checker proves structural/reference integrity only. It does not prove that a
requirement is semantically correct, implemented, secure, approved, or ready for
production. ``--strict-ready`` is a fail-closed gate over visible placeholders,
owner decisions, draft statuses, and planned-only verification; passing it still
requires human review of the readiness dimensions this script cannot prove.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PHASE_ROOT = ROOT / "acc-architecture" / "execution-phases"
REGISTRY = PHASE_ROOT / "requirements-registry.csv"
ELEMENTS = ROOT / "acc-architecture" / "registry" / "elements.json"
FUNCTIONS = ROOT / "acc-architecture" / "registry" / "functions.json"

EXPECTED_COLUMNS = [
    "requirement_id", "level", "document_id", "document_path",
    "parent_requirement_id", "phase_id", "title", "status", "statement",
    "locations", "c4_containers", "actor_ids", "use_case_id",
    "acceptance_criteria", "verification_refs", "evidence_refs",
    "open_decisions",
]
PHASES = {
    "PH-01": "phase-01-platform-foundation",
    "PH-02": "phase-02-catalog-discovery-reservation",
    "PH-03": "phase-03-inventory-order-payment-delivery-events",
    "PH-04": "phase-04-accmared-internal-delivery",
    "PH-05": "phase-05-intelligence-personalization",
}
STATUSES = {"DRAFT", "PROPOSED", "OWNER_REVIEW", "ACCEPTED", "RETIRED"}
MAIN_RE = re.compile(r"^REQ-PH0[1-5]-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
SUB_RE = re.compile(r"^SREQ-PH0[1-5]-[A-Z0-9]+-[0-9]{3}$")
REF_RE = re.compile(r"^[A-Z][A-Z0-9-]+$")
FN_RE = re.compile(r"\bFN-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")
GAP_RE = re.compile(r"\bRGAP-PH0[1-4]-[0-9]{3}\b")
AC_RE = re.compile(r"^AC-PH0[1-4]-[A-Z0-9]+-[0-9]{3}-[0-9]{2}$")


def split_values(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[,;]", value or "") if part.strip()]


def _normal(value: str) -> str:
    value = " ".join((value or "").split())
    return "" if value.lower() in {"none recorded", "n/a", "—", "-"} else value


def load_elements() -> tuple[dict[str, dict], dict[str, dict]]:
    with ELEMENTS.open(encoding="utf-8-sig") as handle:
        data = json.load(handle)["elements"]
    c1 = {item["id"]: item for item in data if item.get("level") == "C1"}
    c2 = {item["id"]: item for item in data if item.get("level") == "C2"}
    return c1, c2


def load_function_ids() -> set[str]:
    with FUNCTIONS.open(encoding="utf-8-sig") as handle:
        data = json.load(handle)
    return {item["id"] for item in data.get("functions", []) if item.get("id")}


def load_rows() -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    if not REGISTRY.exists():
        return [], [f"missing registry: {REGISTRY}"]
    with REGISTRY.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        actual = reader.fieldnames or []
        missing = [column for column in EXPECTED_COLUMNS if column not in actual]
        extra = [column for column in actual if column not in EXPECTED_COLUMNS]
        if missing:
            errors.append("missing CSV columns: " + ", ".join(missing))
        if extra:
            errors.append("unexpected CSV columns: " + ", ".join(extra))
        rows = list(reader)
    return rows, errors


def _split_markdown_row(line: str) -> list[str]:
    """Split one Markdown table row while honoring escaped pipe characters."""
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|") and not text.endswith("\\|"):
        text = text[:-1]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in text:
        if char == "|" and not escaped:
            cells.append("".join(current).replace("\\|", "|").strip())
            current = []
        else:
            current.append(char)
        if char == "\\" and not escaped:
            escaped = True
        else:
            escaped = False
    cells.append("".join(current).replace("\\|", "|").strip())
    return cells


def _is_markdown_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def _tables_in_section(text: str, heading: str) -> list[list[list[str]]]:
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == heading), None)
    if start is None:
        return []
    section: list[str] = []
    for line in lines[start + 1:]:
        if re.match(r"^##\s+", line):
            break
        section.append(line)
    tables: list[list[list[str]]] = []
    current: list[list[str]] = []
    for line in section + [""]:
        if line.strip().startswith("|"):
            cells = _split_markdown_row(line)
            if not _is_markdown_separator(cells):
                current.append(cells)
        elif current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    return tables


def _table_by_header(tables: list[list[list[str]]], first_cells: tuple[str, ...]) -> list[list[str]] | None:
    for table in tables:
        if table and tuple(table[0][:len(first_cells)]) == first_cells:
            return table
    return None


def _document_header(text: str, rid: str, expected_phase: str, errors: list[str]) -> None:
    fields = {
        name: re.search(pattern, text, re.MULTILINE)
        for name, pattern in {
            "Document ID": r"^\*\*Document ID:\*\*\s*(.*?)\s*$",
            "Phase": r"^\*\*Phase:\*\*\s*(PH-0[1-5])\b.*$",
            "Status": r"^\*\*Status:\*\*\s*([A-Z_]+)\b.*$",
        }.items()
    }
    for name, match in fields.items():
        if not match:
            errors.append(f"{rid}: document is missing **{name}:** metadata")
    doc_match = fields["Document ID"]
    if doc_match and doc_match.group(1).strip() != rid:
        errors.append(f"{rid}: document Document ID is {doc_match.group(1).strip()!r}")
    phase_match = fields["Phase"]
    if phase_match and phase_match.group(1) != expected_phase:
        errors.append(f"{rid}: document Phase is {phase_match.group(1)!r}, expected {expected_phase}")
    first_heading = next((line.strip() for line in text.splitlines() if line.startswith("# ")), "")
    if rid not in first_heading:
        errors.append(f"{rid}: document title heading does not contain its Document ID")


def _field_map(table: list[list[str]], rid: str, errors: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for cells in table[1:]:
        if len(cells) != 2:
            errors.append(f"{rid}: malformed main-requirement metadata row")
            continue
        key, value = cells
        if key in result:
            errors.append(f"{rid}: duplicate main-requirement field {key!r}")
        result[key] = value
    return result


def validate_documents(rows: list[dict[str, str]], errors: list[str]) -> None:
    """Compare registry rows to their exact Markdown table rows and AC ownership."""
    known = {row.get("requirement_id", "").strip(): row for row in rows if row.get("requirement_id", "").strip()}
    ac_owners: dict[str, str] = {}
    for row in rows:
        rid = row.get("requirement_id", "").strip()
        if row.get("level", "").strip().lower() != "sub":
            continue
        for ac_id in split_values(row.get("acceptance_criteria", "")):
            if ac_id in ac_owners:
                errors.append(f"{rid}: duplicate acceptance criterion reference {ac_id} (already assigned to {ac_owners[ac_id]})")
            ac_owners[ac_id] = rid

    docs: dict[Path, list[dict[str, str]]] = {}
    for row in rows:
        rel = row.get("document_path", "").strip()
        if not rel:
            continue
        path = (ROOT / rel).resolve() if not Path(rel).is_absolute() else Path(rel).resolve()
        docs.setdefault(path, []).append(row)

    doc_ac_ids: dict[Path, dict[str, str]] = {}
    for path, doc_rows in docs.items():
        doc_id = doc_rows[0].get("document_id", "").strip()
        expected_phase = doc_rows[0].get("phase_id", "").strip()
        if any(r.get("document_id", "").strip() != doc_id for r in doc_rows):
            errors.append(f"{path}: rows sharing one document_path have different document_id values")
        if any(r.get("phase_id", "").strip() != expected_phase for r in doc_rows):
            errors.append(f"{path}: rows sharing one document_path have different phase_id values")
        if expected_phase not in PHASES or expected_phase == "PH-05":
            continue
        expected_root = (PHASE_ROOT / PHASES[expected_phase]).resolve()
        try:
            path.relative_to(expected_root)
        except ValueError:
            errors.append(f"{doc_id or path}: document_path must be under {expected_root.relative_to(ROOT)}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{doc_id or path}: cannot read requirement document: {exc}")
            continue
        if doc_id:
            _document_header(text, doc_id, expected_phase, errors)

        main_rows = [r for r in doc_rows if r.get("level", "").strip().lower() == "main"]
        sub_rows = [r for r in doc_rows if r.get("level", "").strip().lower() == "sub"]
        if len(main_rows) != 1:
            errors.append(f"{doc_id or path}: document_path must have exactly one main requirement row; found {len(main_rows)}")
            main = main_rows[0] if main_rows else None
        else:
            main = main_rows[0]

        main_tables = _tables_in_section(text, "## 1. Main requirement")
        main_table = _table_by_header(main_tables, ("Field", "Value"))
        if main is None:
            pass
        elif not main_table:
            errors.append(f"{main['requirement_id']}: missing ## 1. Main requirement Field/Value table")
        else:
            fields = _field_map(main_table, main["requirement_id"], errors)
            checks = {
                "Requirement ID": "requirement_id", "Phase ID": "phase_id", "Title": "title",
                "Statement": "statement", "Actors": "actor_ids", "Locations": "locations",
                "Primary C4 containers": "c4_containers", "Related function/use case": "use_case_id",
                "Status": "status", "Evidence": "evidence_refs",
            }
            for label, key in checks.items():
                if label not in fields:
                    errors.append(f"{main['requirement_id']}: main document table is missing {label!r}")
                elif _normal(fields[label]) != _normal(main.get(key, "")):
                    errors.append(f"{main['requirement_id']}: registry/document mismatch for main field {label!r}")
            if main.get("document_id", "").strip() != main.get("requirement_id", "").strip():
                errors.append(f"{main['requirement_id']}: main document_id must equal requirement_id")
            doc_status = re.search(r"^\*\*Status:\*\*\s*([A-Z_]+)\b", text, re.MULTILINE)
            if doc_status and doc_status.group(1) != main.get("status", "").strip():
                errors.append(f"{main['requirement_id']}: document-level Status does not match the registry")

        sub_tables = _tables_in_section(text, "## 3. Sub-requirement register")
        sub_table = _table_by_header(sub_tables, ("Sub-requirement ID", "Parent requirement ID"))
        related_table = _table_by_header(sub_tables, ("Sub-requirement ID", "Title", "Actors"))
        if sub_rows and not sub_table:
            errors.append(f"{doc_id}: missing sub-requirement register table")
        if sub_rows and not related_table:
            errors.append(f"{doc_id}: missing related function/use case, actors and evidence table")

        sub_data: dict[str, dict[str, str]] = {}
        if sub_table:
            header = sub_table[0]
            if len(set(header)) != len(header):
                errors.append(f"{doc_id}: duplicate columns in sub-requirement table")
            for cells in sub_table[1:]:
                if len(cells) != len(header):
                    errors.append(f"{doc_id}: malformed sub-requirement table row")
                    continue
                record = dict(zip(header, cells))
                rid = record.get("Sub-requirement ID", "").strip()
                if rid in sub_data:
                    errors.append(f"{doc_id}: duplicate sub-requirement table row {rid}")
                sub_data[rid] = record
        related_data: dict[str, dict[str, str]] = {}
        if related_table:
            header = related_table[0]
            for cells in related_table[1:]:
                if len(cells) != len(header):
                    errors.append(f"{doc_id}: malformed related-metadata table row")
                    continue
                record = dict(zip(header, cells))
                rid = record.get("Sub-requirement ID", "").strip()
                if rid in related_data:
                    errors.append(f"{doc_id}: duplicate related-metadata row {rid}")
                related_data[rid] = record

        sub_checks = {
            "Parent requirement ID": "parent_requirement_id", "Statement": "statement",
            "Locations": "locations", "C4 containers": "c4_containers",
            "Acceptance criteria": "acceptance_criteria", "Verification": "verification_refs",
            "Status": "status", "Open decisions": "open_decisions",
        }
        for row in sub_rows:
            rid = row.get("requirement_id", "").strip()
            if row.get("document_id", "").strip() != row.get("parent_requirement_id", "").strip():
                errors.append(f"{rid}: sub-requirement document_id must equal parent_requirement_id")
            record = sub_data.get(rid)
            if not record:
                errors.append(f"{rid}: no exact row in the document sub-requirement table")
            else:
                for label, key in sub_checks.items():
                    if label not in record:
                        errors.append(f"{rid}: sub-requirement table is missing {label!r}")
                    elif _normal(record[label]) != _normal(row.get(key, "")):
                        errors.append(f"{rid}: registry/document mismatch for sub field {label!r}")
            related = related_data.get(rid)
            if not related:
                errors.append(f"{rid}: no exact row in the related function/use case, actors and evidence table")
            else:
                for label, key in (("Actors", "actor_ids"), ("Related function/use case", "use_case_id"), ("Evidence", "evidence_refs")):
                    if label not in related:
                        errors.append(f"{rid}: related-metadata table is missing {label!r}")
                    elif _normal(related[label]) != _normal(row.get(key, "")):
                        errors.append(f"{rid}: registry/document mismatch for related field {label!r}")

        ac_tables = _tables_in_section(text, "## 4. Acceptance criteria")
        ac_table = _table_by_header(ac_tables, ("Acceptance criterion", "Proves", "Criterion"))
        if sub_rows and not ac_table:
            errors.append(f"{doc_id}: missing acceptance-criteria table")
        local_ac: dict[str, str] = {}
        if ac_table:
            header = ac_table[0]
            ai, pi = header.index("Acceptance criterion"), header.index("Proves")
            for cells in ac_table[1:]:
                if len(cells) != len(header):
                    errors.append(f"{doc_id}: malformed acceptance-criteria table row")
                    continue
                ac_id, proves = cells[ai].strip(), cells[pi].strip()
                if not AC_RE.fullmatch(ac_id):
                    errors.append(f"{doc_id}: invalid acceptance criterion ID {ac_id!r}")
                if ac_id in local_ac:
                    errors.append(f"{doc_id}: duplicate acceptance criterion row {ac_id}")
                local_ac[ac_id] = proves
                if ac_id not in ac_owners:
                    errors.append(f"{doc_id}: acceptance criterion {ac_id} is not referenced by the CSV registry")
                elif ac_owners[ac_id] != proves:
                    errors.append(f"{doc_id}: acceptance criterion {ac_id} proves {proves}, expected {ac_owners[ac_id]}")
                if proves not in known or known[proves].get("level", "").strip().lower() != "sub":
                    errors.append(f"{doc_id}: acceptance criterion {ac_id} proves unknown/non-sub requirement {proves}")
        doc_ac_ids[path] = local_ac
        for row in sub_rows:
            rid = row.get("requirement_id", "").strip()
            ac_ids = split_values(row.get("acceptance_criteria", ""))
            if not ac_ids:
                errors.append(f"{rid}: at least one acceptance criterion is required")
            for ac_id in ac_ids:
                if not AC_RE.fullmatch(ac_id):
                    errors.append(f"{rid}: invalid acceptance criterion reference {ac_id!r}")
                if ac_id not in local_ac:
                    errors.append(f"{rid}: acceptance criterion {ac_id} is missing from its document")
                elif local_ac[ac_id] != rid:
                    errors.append(f"{rid}: acceptance criterion {ac_id} proves {local_ac[ac_id]}, not {rid}")
        for rid in sub_data.keys() - {r.get("requirement_id", "").strip() for r in sub_rows}:
            errors.append(f"{doc_id}: sub-requirement table row {rid} is absent from CSV registry")
        for rid in related_data.keys() - {r.get("requirement_id", "").strip() for r in sub_rows}:
            errors.append(f"{doc_id}: related-metadata row {rid} is absent from CSV registry")


def _validate_use_case_references(row: dict[str, str], function_ids: set[str], document_text: str, prefix: str, errors: list[str]) -> None:
    value = row.get("use_case_id", "").strip()
    if not value:
        errors.append(f"{prefix}: missing related function/use case")
        return
    for function_id in FN_RE.findall(value):
        if function_id not in function_ids:
            errors.append(f"{prefix}: unknown function reference {function_id}")
    if re.search(r"\bTBD\b", value, re.IGNORECASE):
        gaps = GAP_RE.findall(value)
        if not gaps:
            errors.append(f"{prefix}: TBD related function/use case must cite a documented RGAP-PHxx-NNN gap")
        for gap_id in gaps:
            if not re.search(rf"(?<![A-Z0-9-]){re.escape(gap_id)}(?![A-Z0-9-])", document_text):
                errors.append(f"{prefix}: cited gap {gap_id} is not documented in its requirement document")


def validate(rows: list[dict[str, str]], initial_errors: list[str], require_rows: bool, strict_ready: bool = False) -> list[str]:
    errors = list(initial_errors)
    if require_rows and not rows:
        errors.append("registry has no rows; at least one requirement row is required in strict mode")
    try:
        c1, c2 = load_elements()
        function_ids = load_function_ids()
    except Exception as exc:  # pragma: no cover - diagnostic path
        return errors + [f"cannot load architecture registries: {exc}"]

    ids: set[str] = set()
    main_ids: set[str] = set()
    for index, row in enumerate(rows, start=2):
        prefix = f"row {index}"
        rid = row.get("requirement_id", "").strip()
        level = row.get("level", "").strip().lower()
        phase = row.get("phase_id", "").strip()
        status = row.get("status", "").strip()
        title = row.get("title", "").strip()
        statement = row.get("statement", "").strip()
        document_id = row.get("document_id", "").strip()
        document_path = row.get("document_path", "").strip()
        parent = row.get("parent_requirement_id", "").strip()
        locations = split_values(row.get("locations", ""))
        containers = split_values(row.get("c4_containers", ""))
        actors = split_values(row.get("actor_ids", ""))

        if not rid:
            errors.append(f"{prefix}: missing requirement_id")
            continue
        if rid in ids:
            errors.append(f"{prefix}: duplicate requirement_id {rid}")
        ids.add(rid)
        if level not in {"main", "sub"}:
            errors.append(f"{prefix} {rid}: level must be main or sub")
        elif level == "main":
            if not MAIN_RE.fullmatch(rid):
                errors.append(f"{prefix} {rid}: invalid main requirement ID")
            if parent:
                errors.append(f"{prefix} {rid}: main requirement cannot have a parent")
            main_ids.add(rid)
        elif not SUB_RE.fullmatch(rid):
            errors.append(f"{prefix} {rid}: invalid sub-requirement ID")
        if phase not in PHASES:
            errors.append(f"{prefix} {rid}: invalid phase_id {phase!r}")
        elif phase == "PH-05":
            errors.append(f"{prefix} {rid}: Phase 05 is future-only and cannot contain requirements")
        if status not in STATUSES:
            errors.append(f"{prefix} {rid}: invalid status {status!r}")
        for field, value in (("title", title), ("statement", statement), ("document_id", document_id), ("document_path", document_path)):
            if not value:
                errors.append(f"{prefix} {rid}: missing {field}")
        if level == "sub" and not parent:
            errors.append(f"{prefix} {rid}: sub-requirement requires parent_requirement_id")
        if not actors:
            errors.append(f"{prefix} {rid}: at least one actor_id is required")
        for actor in actors:
            item = c1.get(actor)
            if not REF_RE.fullmatch(actor) or not item or item.get("type") not in {"person", "external_system", "system"}:
                errors.append(f"{prefix} {rid}: invalid actor reference {actor!r}")
        if not locations:
            errors.append(f"{prefix} {rid}: at least one canonical location is required")
        for location in locations:
            if not REF_RE.fullmatch(location) or location not in c1 or c1[location].get("type") != "system":
                errors.append(f"{prefix} {rid}: invalid C1 system location {location!r}")
        if not containers:
            errors.append(f"{prefix} {rid}: at least one C2 container is required")
        for container in containers:
            item = c2.get(container)
            if not item or item.get("type") not in {"service", "application", "data_store"}:
                errors.append(f"{prefix} {rid}: invalid C2 application/service/data-store {container!r}")
            elif item.get("parent_id") not in locations:
                errors.append(f"{prefix} {rid}: {container} parent {item.get('parent_id')} is not in locations")
        if not row.get("verification_refs", "").strip():
            errors.append(f"{prefix} {rid}: verification_refs is required")
        if not row.get("evidence_refs", "").strip():
            errors.append(f"{prefix} {rid}: evidence_refs is required")
        if phase in PHASES and phase != "PH-05" and document_path:
            expected_root = (PHASE_ROOT / PHASES[phase]).resolve()
            path = (ROOT / document_path).resolve() if not Path(document_path).is_absolute() else Path(document_path).resolve()
            valid_doc_path = True
            try:
                path.relative_to(expected_root)
            except ValueError:
                errors.append(f"{prefix} {rid}: document_path must be under {expected_root.relative_to(ROOT)}")
                valid_doc_path = False
            if valid_doc_path:
                if not path.exists():
                    errors.append(f"{prefix} {rid}: missing document_path {document_path}")
                else:
                    try:
                        text = path.read_text(encoding="utf-8")
                    except (OSError, UnicodeError) as exc:
                        errors.append(f"{prefix} {rid}: cannot read document_path {document_path}: {exc}")
                    else:
                        _validate_use_case_references(row, function_ids, text, f"{prefix} {rid}", errors)
        elif row.get("use_case_id", "").strip():
            _validate_use_case_references(row, function_ids, "", f"{prefix} {rid}", errors)

        if strict_ready:
            if status != "ACCEPTED":
                errors.append(f"{prefix} {rid}: strict-ready requires ACCEPTED status; found {status or 'blank'}")
            if re.search(r"\b(?:TBD|TBC|UNKNOWN|UNRESOLVED)\b", row.get("use_case_id", ""), re.IGNORECASE):
                errors.append(f"{prefix} {rid}: strict-ready rejects unresolved function/use-case placeholders")
            if row.get("open_decisions", "").strip():
                errors.append(f"{prefix} {rid}: strict-ready rejects open decisions")
            if re.search(r"\bplanned\b", row.get("verification_refs", ""), re.IGNORECASE):
                errors.append(f"{prefix} {rid}: strict-ready rejects planned-only verification")

    for index, row in enumerate(rows, start=2):
        if row.get("level", "").strip().lower() == "sub":
            parent = row.get("parent_requirement_id", "").strip()
            if parent and parent not in main_ids:
                errors.append(f"row {index} {row.get('requirement_id')}: parent {parent} is not a main requirement")

    validate_documents(rows, errors)
    return errors


def query(rows: list[dict[str, str]], phase: str | None, location: str | None, container: str | None) -> int:
    matches = []
    for row in rows:
        if phase and row.get("phase_id", "").strip() != phase:
            continue
        if location and location not in split_values(row.get("locations", "")):
            continue
        if container and container not in split_values(row.get("c4_containers", "")):
            continue
        matches.append(row)
    print("requirement_id | level | phase_id | title | locations | c4_containers | status")
    print("---|---|---|---|---|---|---")
    for row in matches:
        print(" | ".join([
            row.get("requirement_id", ""), row.get("level", ""), row.get("phase_id", ""),
            row.get("title", ""), row.get("locations", ""), row.get("c4_containers", ""), row.get("status", ""),
        ]))
    print(f"matches={len(matches)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--query", action="store_true")
    parser.add_argument("--require-rows", action="store_true", help="fail if the scaffold registry is empty")
    parser.add_argument("--strict-ready", action="store_true", help="add fail-closed readiness gates; does not certify implementation readiness")
    parser.add_argument("--phase", choices=sorted(PHASES))
    parser.add_argument("--location")
    parser.add_argument("--container")
    args = parser.parse_args()
    if args.strict_ready and not args.check:
        parser.error("--strict-ready can only be used with --check")
    rows, load_errors = load_rows()
    if args.query:
        if load_errors:
            for error in load_errors:
                print("ERROR:", error)
            return 1
        return query(rows, args.phase, args.location, args.container)
    errors = validate(rows, load_errors, args.require_rows, args.strict_ready)
    if errors:
        for error in errors:
            print("ERROR:", error)
        print(f"FAIL: {len(errors)} error(s); structural/readiness checks are not trustworthy")
        return 1
    print(f"PASS: requirements registry schema, exact document rows, acceptance links and C1/C2 references are valid; rows={len(rows)}")
    print("NOTE: semantic correctness, implementation, security, human approval, and production readiness remain unverified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
