#!/usr/bin/env python3
import argparse
from validate_architecture import validate
p=argparse.ArgumentParser(description='Validate architecture document references.')
p.add_argument('architecture_dir')
a=p.parse_args(); errs,_=validate(a.architecture_dir); errs=[e for e in errs if 'reference' in e or 'referenced file' in e]
for e in errs: print('- '+e)
raise SystemExit(1 if errs else 0)
