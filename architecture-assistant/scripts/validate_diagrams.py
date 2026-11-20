#!/usr/bin/env python3
import argparse
from validate_architecture import validate
p=argparse.ArgumentParser(description='Validate registered IDs used in Mermaid blocks.')
p.add_argument('architecture_dir')
a=p.parse_args(); errs,_=validate(a.architecture_dir); errs=[e for e in errs if 'diagram references' in e]
for e in errs: print('- '+e)
raise SystemExit(1 if errs else 0)
