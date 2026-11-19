#!/usr/bin/env python3
import sys
from validate_architecture import validate
errs,_=validate(sys.argv[1]); errs=[e for e in errs if any(w in e for w in ['mapping','orphan','operation','function','decision','parent reference'])]
print('PASS' if not errs else 'BLOCKED'); [print('- '+e) for e in errs]; sys.exit(bool(errs))
