#!/usr/bin/env python3
"""Validate registered identifiers in Markdown Mermaid blocks; syntax rendering is not performed."""
import sys
from validate_architecture import validate
errs,_=validate(sys.argv[1]); errs=[e for e in errs if 'diagram references' in e]
print('PASS (ID consistency only; syntax/rendering NOT VERIFIED)' if not errs else 'BLOCKED'); [print('- '+e) for e in errs]; sys.exit(bool(errs))
