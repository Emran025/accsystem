#!/usr/bin/env python3
"""Validate and query the ACC execution-phase requirement registry.

This checker proves structural/reference integrity only. It does not prove that a
requirement is semantically correct, implemented, secure, or production-ready.
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


def split_values(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[,;]", value or "") if part.strip()]


def load_elements() -> tuple[dict[str, dict], dict[str, dict]]:
    with ELEMENTS.open(encoding="utf-8-sig") as handle:
        data = json.load(handle)["elements"]
    c1 = {item["id"]: item for item in data if item.get("level") == "C1"}
    c2 = {item["id"]: item for item in data if item.get("level") == "C2"}
    return c1, c2


def load_rows() -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    if not REGISTRY.exists():
        return [], [f"missing registry: {REGISTRY}"]
    with REGISTRY.open(newline="", encoding="utf-8") as handle:
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


def validate(rows: list[dict[str, str]], initial_errors: list[str], require_rows: bool) -> list[str]:
    errors = list(initial_errors)
    if require_rows and not rows:
        errors.append("registry has no rows; at least one requirement row is required in strict mode")
    try:
        c1, c2 = load_elements()
    except Exception as exc:  # pragma: no cover - diagnostic path
        return errors + [f"cannot load C4 registry: {exc}"]

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
        if locations:
            for location in locations:
                if not REF_RE.fullmatch(location) or location not in c1 or c1[location].get("type") != "system":
                    errors.append(f"{prefix} {rid}: invalid C1 system location {location!r}")
        else:
            errors.append(f"{prefix} {rid}: at least one canonical location is required")
        if not containers:
            errors.append(f"{prefix} {rid}: at least one C2 container is required")
        for container in containers:
            item = c2.get(container)
            if not item or item.get("type") not in {"service", "application", "data_store"}:
                errors.append(f"{prefix} {rid}: invalid C2 application/service/data-store {container!r}")
            elif item.get("parent_id") not in locations:
                errors.append(f"{prefix} {rid}: {container} parent {item.get('parent_id')} is not in locations")
        if phase in PHASES and document_path:
            expected_root = PHASE_ROOT / PHASES[phase]
            path = (ROOT / document_path).resolve() if not Path(document_path).is_absolute() else Path(document_path).resolve()
            try:
                path.relative_to(expected_root.resolve())
            except ValueError:
                errors.append(f"{prefix} {rid}: document_path must be under {expected_root.relative_to(ROOT)}")
            if not path.exists():
                errors.append(f"{prefix} {rid}: missing document_path {document_path}")
            else:
                text = path.read_text(encoding="utf-8")
                if rid not in text:
                    errors.append(f"{prefix} {rid}: document does not contain its requirement ID")
                for container in containers:
                    if container not in text:
                        errors.append(f"{prefix} {rid}: document does not mention C4 container {container}")
        if level == "sub" and parent and parent not in ids and parent not in main_ids:
            # A later main row is allowed in CSV, so defer this check below.
            pass

    for index, row in enumerate(rows, start=2):
        if row.get("level", "").strip().lower() == "sub":
            parent = row.get("parent_requirement_id", "").strip()
            if parent and parent not in main_ids:
                errors.append(f"row {index} {row.get('requirement_id')}: parent {parent} is not a main requirement")
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
    parser.add_argument("--phase", choices=sorted(PHASES))
    parser.add_argument("--location")
    parser.add_argument("--container")
    args = parser.parse_args()
    rows, load_errors = load_rows()
    if args.query:
        if load_errors:
            for error in load_errors:
                print("ERROR:", error)
            return 1
        return query(rows, args.phase, args.location, args.container)
    errors = validate(rows, load_errors, args.require_rows)
    if errors:
        for error in errors:
            print("ERROR:", error)
        print(f"FAIL: {len(errors)} error(s); structural references are not trustworthy")
        return 1
    print(f"PASS: requirements registry schema and C4 references are valid; rows={len(rows)}")
    print("NOTE: semantic correctness, implementation, security, and owner approval remain unverified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
