#!/usr/bin/env python3
import sys
from validate_architecture import validate
_,counts=validate(sys.argv[1]); print('Coverage report written (registry/decomposition states only; not semantic completeness).'); [print(f'{k}: in-scope={v["total"]}, decomposition_complete={v["decomposition_complete"]}, exceptions_not_complete={v["exceptions"]}, unresolved={v["unresolved"]}, missing={v["missing"]}') for k,v in sorted(counts.items())]
