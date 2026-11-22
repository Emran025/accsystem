#!/usr/bin/env python3
"""Validate every Mermaid block for registry IDs and renderer syntax.

A missing renderer is explicitly NOT_VERIFIED (exit 2), never PASS.
"""
import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from validate_architecture import validate

BLOCK = re.compile(r"```mermaid\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("architecture_dir")
    args = parser.parse_args()
    root = Path(args.architecture_dir).resolve()
    errors, _ = validate(root)
    errors = [e for e in errors if "diagram references" in e]
    blocks = []
    for md in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in md.relative_to(root).parts):
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        for index, match in enumerate(BLOCK.finditer(text), 1):
            blocks.append((md.relative_to(root).as_posix(), index, match.group(1)))
    renderer = shutil.which("mmdc")
    if not renderer:
        print(f"NOT_VERIFIED: Mermaid renderer mmdc is unavailable; discovered {len(blocks)} block(s)")
        for error in errors:
            print(f"- {error}")
        return 2 if not errors else 1
    with tempfile.TemporaryDirectory(prefix="acc-mermaid-") as tmp:
        for rel, index, source in blocks:
            source_path = Path(tmp) / f"{len(errors)}.mmd"
            output_path = Path(tmp) / f"{len(errors)}.svg"
            source_path.write_text(source, encoding="utf-8")
            result = subprocess.run([renderer, "-i", str(source_path), "-o", str(output_path), "--quiet"], text=True, capture_output=True)
            if result.returncode:
                detail = (result.stderr or result.stdout).strip().splitlines()[-1:]
                errors.append(f"{rel} Mermaid block {index} failed to render: {' '.join(detail) or 'renderer error'}")
    if errors:
        print(f"BLOCKED: {len(errors)} Mermaid/registry issue(s) across {len(blocks)} block(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: rendered and checked {len(blocks)} Mermaid block(s); semantic C4 correctness and owner approval remain unverified")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
