#!/usr/bin/env python3
import argparse
from validate_architecture import validate
p=argparse.ArgumentParser(description='Validate architecture traceability mappings.')
p.add_argument('architecture_dir')
a=p.parse_args(); errs,_=validate(a.architecture_dir); errs=[e for e in errs if any(w in e for w in ['mapping','orphan','operation','function','decision','parent reference'])]
for e in errs: print('- '+e)
raise SystemExit(1 if errs else 0)
