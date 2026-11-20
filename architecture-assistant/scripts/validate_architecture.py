#!/usr/bin/env python3
"""Validate architecture registries and in-project references (structural checks only)."""
import argparse, json, re, sys
from pathlib import Path
LEVELS={'C1','C2','C3','C4','FUNCTION','INTERFACE','DATA','DECISION'}
GATES={'NOT_STARTED','IN_PROGRESS','BLOCKED','PASSED','WAIVED'}
SCOPES={'IN_SCOPE','OUT_OF_SCOPE','EXTERNAL','UNRESOLVED'}
DECOMP={'NOT_STARTED','IN_PROGRESS','COMPLETE','EXCEPTION','BLOCKED'}
KINDS={'CONTEXT_TO_CONTAINER','CONTAINER_TO_COMPONENT','COMPONENT_TO_CODE','OPERATION_TO_FUNCTION','DECISION_TO_ELEMENT','EXCEPTION'}
SCHEMA_DIR=Path(__file__).resolve().parents[1]/'schemas'

def schema_errors(value, schema, path='$'):
    """Small dependency-free JSON Schema subset used by the declared project schemas."""
    errors=[]
    typ=schema.get('type')
    type_ok={'object': isinstance(value,dict), 'array': isinstance(value,list), 'string': isinstance(value,str), 'boolean': isinstance(value,bool), 'null': value is None}
    if isinstance(typ,list):
        if not any(type_ok.get(t,False) for t in typ): errors.append(f'{path}: expected one of {typ}')
    elif typ and not type_ok.get(typ,False):
        errors.append(f'{path}: expected {typ}')
    if 'enum' in schema and value not in schema['enum']: errors.append(f'{path}: value {value!r} is not in enum')
    if isinstance(value,str):
        if 'minLength' in schema and len(value)<schema['minLength']: errors.append(f'{path}: shorter than minLength')
        if 'pattern' in schema and not re.search(schema['pattern'],value): errors.append(f'{path}: does not match pattern {schema["pattern"]!r}')
    if isinstance(value,dict):
        for required in schema.get('required',[]):
            if required not in value: errors.append(f'{path}.{required}: missing required property')
        for key,child in schema.get('properties',{}).items():
            if key in value: errors.extend(schema_errors(value[key],child,f'{path}.{key}'))
        if schema.get('additionalProperties') is False:
            allowed=set(schema.get('properties',{}))
            for key in value:
                if key not in allowed: errors.append(f'{path}: unexpected property {key!r}')
        elif isinstance(schema.get('additionalProperties'),dict):
            for key,val in value.items():
                if key not in schema.get('properties',{}): errors.extend(schema_errors(val,schema['additionalProperties'],f'{path}.{key}'))
    if isinstance(value,list) and isinstance(schema.get('items'),dict):
        for index,item in enumerate(value): errors.extend(schema_errors(item,schema['items'],f'{path}[{index}]'))
    return errors

def validate_declared_schemas(root, regs, errors):
    """Validate registry payloads against the schemas that explicitly describe them."""
    # These three schemas describe the registry payloads themselves. The
    # decision/function/interface schemas describe individual artifact
    # documents, while their registry files are intentionally indexes with a
    # smaller shape; applying those schemas to indexes would create a false
    # PASS/FAIL signal. They are reported as not bound until an artifact JSON
    # instance declares the corresponding schema.
    declared={
        'architecture-manifest.json': ('architecture-manifest.schema.json', lambda x:[x]),
        'elements.json': ('architectural-element.schema.json', lambda x:x.get('elements',[])),
        'decomposition-map.json': ('decomposition-map.schema.json', lambda x:[x]),
    }
    for registry,(schema_name,select) in declared.items():
        schema_path=SCHEMA_DIR/schema_name
        if not schema_path.is_file():
            errors.append(f'{schema_path}: declared JSON Schema is missing')
            continue
        try: schema=json.loads(schema_path.read_text(encoding='utf-8'))
        except (OSError,UnicodeError,json.JSONDecodeError) as exc:
            errors.append(f'{schema_path}: invalid JSON Schema: {exc}'); continue
        if not isinstance(schema,dict) or schema.get('type') not in {'object','array'}:
            errors.append(f'{schema_path}: unsupported or malformed declared schema'); continue
        try: records=select(regs[registry])
        except Exception as exc:
            errors.append(f'{registry}: cannot select schema records: {exc}'); continue
        if not isinstance(records,list): records=[records]
        for index,record in enumerate(records):
            for issue in schema_errors(record,schema,f'{registry}[{index}]'):
                errors.append(f'{issue} (schema {schema_name})')

def load(p, errors, required=False):
    if not p.is_file():
        if required: errors.append(f'{p}: required registry missing')
        return {}
    try:
        value=json.loads(p.read_text(encoding='utf-8-sig'))
        if not isinstance(value,dict): errors.append(f'{p}: registry root must be an object'); return {}
        return value
    except (OSError,UnicodeError,json.JSONDecodeError) as e:
        errors.append(f'{p}: invalid/unreadable JSON: {e}'); return {}

def safe_target(root, ref):
    if not isinstance(ref,str) or not ref.strip(): return None
    raw=Path(ref)
    if raw.is_absolute() or '..' in raw.parts: return None
    target=(root/raw).resolve()
    try: target.relative_to(root)
    except ValueError: return None
    return target

def check_ref(root, ref, errors, owner):
    p=safe_target(root,ref)
    if p is None: errors.append(f'{owner}: invalid or out-of-project documentation reference: {ref!r}')
    elif not p.is_file(): errors.append(f'{owner}: referenced file does not exist: {ref}')

def check_exception(root, ex, errors, owner):
    if not isinstance(ex,dict) or not ex.get('reason') or not isinstance(ex.get('replacement_docs'),list) or not ex['replacement_docs'] or not ex.get('approved'):
        errors.append(f'{owner}: undocumented/unapproved exception (reason, replacement_docs, approved required)'); return
    approver=ex.get('accepted_by','')
    if not isinstance(approver,str) or re.search(r'architecture\s+assistant|\bassistant\b|\bagent\b|\bmodel\b|\bllm\b',approver,re.I):
        errors.append(f'{owner}: assistant/model cannot self-approve an exception; require explicit authorized stakeholder acceptance')
        return
    for ref in ex['replacement_docs']: check_ref(root,ref,errors,owner+' exception')

def check_markdown_links(root, md, errors):
    text=md.read_text(encoding='utf-8',errors='replace')
    for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
        ref = ref.strip().strip('<>')
        if ref.startswith(('http://','https://','#','mailto:')): continue
        path_ref = ref.split('?', 1)[0].split('#', 1)[0]
        if not path_ref: continue
        try:
            rel = (md.parent / path_ref).resolve().relative_to(root).as_posix()
        except (ValueError, OSError):
            errors.append(f'{md.relative_to(root)}: broken/unsafe Markdown reference {ref}')
            continue
        target = safe_target(root, rel)
        if target is None or not target.exists() or target.is_symlink(): errors.append(f'{md.relative_to(root)}: broken/unsafe Markdown reference {ref}')

def validate(root):
    root=Path(root).resolve(); errors=[]; rp=root/'registry'
    names=['architecture-manifest.json','elements.json','decomposition-map.json','interfaces.json','functions.json','decisions.json']
    regs={n:load(rp/n,errors,True) for n in names}
    validate_declared_schemas(root, regs, errors)
    man,data,mp=regs[names[0]],regs[names[1]],regs[names[2]]
    for k in ['system_id','slug','name','language','stages']:
        if not man.get(k): errors.append(f'registry/architecture-manifest.json: required field {k!r} is missing')
    if man.get('language') not in ('English','Arabic'): errors.append('manifest language must be English or Arabic')
    if not isinstance(man.get('stages',{}),dict): errors.append('manifest stages must be an object'); man['stages']={}
    for k,v in man['stages'].items():
        if v not in GATES: errors.append(f'stage {k}: invalid status {v!r}')
    elems=data.get('elements',[]); ops=data.get('operations',[])
    if not isinstance(elems,list): errors.append('elements.json elements must be an array'); elems=[]
    if not isinstance(ops,list): errors.append('elements.json operations must be an array'); ops=[]
    ids={}
    for i,e in enumerate(elems):
        if not isinstance(e,dict): errors.append(f'elements[{i}] must be an object'); continue
        eid=e.get('id',f'<missing-{i}>')
        if not all(isinstance(e.get(k),str) and e.get(k) for k in ('id','name','level','doc')): errors.append(f'elements[{i}] ({eid}): missing/invalid required id/name/level/doc')
        if eid in ids: errors.append(f'duplicate element ID {eid} (elements[{ids[eid]}] and [{i}])')
        ids[eid]=i
        if e.get('level') not in LEVELS: errors.append(f'{eid}: unknown level {e.get("level")}')
        if e.get('scope_status') not in SCOPES: errors.append(f'{eid}: invalid scope_status')
        if e.get('decomposition_status') not in DECOMP: errors.append(f'{eid}: invalid decomposition_status')
        if e.get('parent_id') is not None and not isinstance(e.get('parent_id'),str): errors.append(f'{eid}: parent_id must be string or null')
        check_ref(root,e.get('doc'),errors,eid)
        if e.get('decomposition_status')=='EXCEPTION': check_exception(root,e.get('exception'),errors,eid)
    op_ids={}
    for i,o in enumerate(ops):
        if not isinstance(o,dict) or not isinstance(o.get('id'),str) or not o['id']: errors.append(f'operations[{i}] missing valid id'); continue
        if o['id'] in ids or o['id'] in op_ids: errors.append(f'duplicate operation/element ID {o["id"]}')
        op_ids[o['id']]=o; check_ref(root,o.get('doc'),errors,o['id'])
    all_ids=set(ids)|set(op_ids)
    for e in elems:
        if isinstance(e,dict) and e.get('parent_id') and e['parent_id'] not in all_ids: errors.append(f'{e.get("id")}: invalid parent reference {e["parent_id"]}')
    maps=mp.get('mappings',[])
    if not isinstance(maps,list): errors.append('decomposition-map mappings must be an array'); maps=[]
    byparent={}; mapped=set()
    for i,m in enumerate(maps):
        if not isinstance(m,dict): errors.append(f'mapping[{i}] must be an object'); continue
        par,children,kind=m.get('parent_id'),m.get('child_ids'),m.get('kind')
        if not isinstance(par,str) or par not in all_ids: errors.append(f'mapping[{i}]: invalid parent reference {par}')
        if kind not in KINDS: errors.append(f'mapping {par}: invalid kind {kind!r}')
        if not isinstance(children,list) or any(not isinstance(c,str) for c in children): errors.append(f'mapping {par}: child_ids must be strings'); children=[]
        if len(children)!=len(set(children)): errors.append(f'mapping {par}: duplicate child IDs')
        byparent.setdefault(par,[]).append(m)
        for c in children:
            if not isinstance(c,str) or c not in all_ids: errors.append(f'mapping {par}: invalid child reference {c}')
            mapped.add(c)
        if kind=='EXCEPTION': check_exception(root,m.get('exception'),errors,f'mapping {par}')
    for e in elems:
        if not isinstance(e,dict) or e.get('scope_status')!='IN_SCOPE': continue
        eid,lev=e.get('id'),e.get('level'); ms=byparent.get(eid,[])
        if lev in ('C2','C3') and e.get('children_expected',True) and not (any(m.get('kind')=='EXCEPTION' and isinstance(m.get('exception'),dict) and m['exception'].get('approved') for m in ms) or any(m.get('child_ids') for m in ms)):
            errors.append(f'{eid}: missing {"component" if lev=="C2" else "code-level"} decomposition mapping')
        if lev in ('C2','C3','C4','FUNCTION','INTERFACE') and e.get('parent_id') and eid not in mapped: errors.append(f'{eid}: orphaned element; absent from parent-child mapping')
    for opid in op_ids:
        if not any(isinstance(m,dict) and m.get('kind')=='OPERATION_TO_FUNCTION' and m.get('parent_id')==opid and m.get('child_ids') for m in maps): errors.append(f'{opid}: business operation has no function mapping')
    funcs=regs['functions.json'].get('functions',[])
    if not isinstance(funcs,list): errors.append('functions.json functions must be an array'); funcs=[]
    fids=set()
    for i,f in enumerate(funcs):
        if not isinstance(f,dict): errors.append(f'functions[{i}] must be an object'); continue
        fid=f.get('id')
        if not isinstance(fid,str) or not fid: errors.append(f'functions[{i}] missing id'); continue
        if fid in fids: errors.append(f'duplicate function ID {fid}')
        fids.add(fid)
        for k in ('parent_system','parent_container','parent_component'):
            if not isinstance(f.get(k),str) or f.get(k) not in ids: errors.append(f'{fid}: invalid {k} reference {f.get(k)}')
        check_ref(root,f.get('doc'),errors,fid)
        if not any(isinstance(m,dict) and m.get('kind')=='OPERATION_TO_FUNCTION' and isinstance(m.get('child_ids'),list) and fid in m.get('child_ids',[]) for m in maps): errors.append(f'{fid}: function has no business operation mapping')
    for filename,collection in [('decisions.json','decisions'),('interfaces.json','interfaces')]:
        records=regs[filename].get(collection,[])
        if not isinstance(records,list): errors.append(f'{filename} {collection} must be an array'); continue
        seen=set()
        for i,r in enumerate(records):
            if not isinstance(r,dict): errors.append(f'{filename} {collection}[{i}] must be an object'); continue
            rid=r.get('id')
            if not isinstance(rid,str) or not rid: errors.append(f'{filename} {collection}[{i}] missing id'); continue
            if rid in seen: errors.append(f'{filename}: duplicate ID {rid}')
            seen.add(rid)
            if collection=='decisions':
                refs=r.get('affected_element_ids',[])
                if not isinstance(refs,list) or not refs: errors.append(f'{rid}: decision missing affected element references'); refs=[]
                for target in refs:
                    if not isinstance(target,str) or target not in ids: errors.append(f'{rid}: missing decision reference to element {target}')
                check_ref(root,r.get('doc'),errors,rid)
            else:
                if not isinstance(r.get('provider_id'),str) or r.get('provider_id') not in all_ids: errors.append(f'{rid}: invalid provider reference {r.get("provider_id")}')
                consumers=r.get('consumer_ids',[])
                if not isinstance(consumers,list): errors.append(f'{rid}: consumer_ids must be an array'); consumers=[]
                for c in consumers:
                    if not isinstance(c,str) or c not in all_ids: errors.append(f'{rid}: invalid consumer reference {c}')
                check_ref(root,r.get('contract_ref'),errors,rid)
    for md in root.rglob('*.md'):
        if any(x.startswith('.') for x in md.relative_to(root).parts): continue
        check_markdown_links(root,md,errors)
        text=md.read_text(encoding='utf-8',errors='replace')
        if '```mermaid' in text:
            for token in re.findall(r'\b(?:SYS|ACT|EXT|CNT|CMP|CODE|FN|IF|ADR|OP)-[A-Z0-9-]+\b',text):
                if token not in all_ids and token not in fids: errors.append(f'{md.relative_to(root)}: diagram references unknown registry ID {token}')
    for gate in ('C3','C4'):
        if man.get('stages',{}).get(gate)=='PASSED' and any(any(w in err for w in ('decomposition mapping','code-level','orphaned element','business operation has no function mapping')) for err in errors): errors.append(f'stage {gate} marked PASSED despite failed completeness requirements')
    report_path=root/'validation'/'validation-status.md'
    report_gate=None
    if report_path.is_file():
        report_text=report_path.read_text(encoding='utf-8',errors='replace')
        match=re.search(r'^\|\s*Gate\s*7\s*\|[^\n]*?\|\s*\*\*(PASSED|BLOCKED|IN_PROGRESS|NOT_STARTED|WAIVED)\*\*\s*\|',report_text,re.M)
        if match: report_gate=match.group(1)
    manifest_gate=man.get('stages',{}).get('validation')
    if report_gate and manifest_gate and report_gate!=manifest_gate:
        errors.append(f'validation-status.md Gate 7 is {report_gate} but manifest validation stage is {manifest_gate}')
    if report_gate=='PASSED' and errors:
        errors.append('validation-status.md Gate 7 marked PASSED despite current structural validation findings')
    if manifest_gate=='PASSED' and errors:
        errors.append('validation stage marked PASSED despite structural validation findings')
    counts={}
    for e in elems:
        if not isinstance(e,dict): continue
        lev=e.get('level','UNKNOWN'); row=counts.setdefault(lev,{'total':0,'decomposition_complete':0,'exceptions':0,'unresolved':0,'missing':[]})
        if e.get('scope_status')=='IN_SCOPE': row['total']+=1
        ms=byparent.get(e.get('id'),[]); mapped_ok=any(m.get('child_ids') and m.get('status')=='COMPLETE' for m in ms)
        exok=any(m.get('kind')=='EXCEPTION' and isinstance(m.get('exception'),dict) and m['exception'].get('approved') for m in ms) or e.get('decomposition_status')=='EXCEPTION'
        okay=(not exok) and e.get('decomposition_status')=='COMPLETE' and (not e.get('children_expected',False) or mapped_ok)
        if okay and e.get('scope_status')=='IN_SCOPE': row['decomposition_complete']+=1
        if exok and e.get('scope_status')=='IN_SCOPE': row['exceptions']+=1
        if e.get('scope_status')=='IN_SCOPE' and e.get('decomposition_status') in ('BLOCKED','IN_PROGRESS','NOT_STARTED'):
            row['unresolved']+=1
        if e.get('scope_status')=='IN_SCOPE' and e.get('children_expected',False) and not okay and not exok: row['missing'].append(e.get('id'))
    coverage=['# Coverage report','','System: '+str(man.get('name','unknown'))+' (`'+str(man.get('system_id','unknown'))+'`)','','**Interpretation:** counts below report registry/decomposition states only. They do not establish semantic correctness, documentation depth, implemented behavior, stakeholder acceptance, or production readiness. Exceptions are reported separately and are not counted as decomposition-complete.','','| Level | In-scope total | Decomposition complete | Exceptions (not complete) | Blocked/in progress/not started | Missing IDs |','|---|---:|---:|---:|---:|---|']
    for lev,row in sorted(counts.items()): coverage.append(f'| {lev} | {row["total"]} | {row["decomposition_complete"]} | {row["exceptions"]} | {row["unresolved"]} | {", ".join(row["missing"]) or "None"} |')
    coverage+=['',f'Unmapped validation findings: {len(errors)}','','This is not a single overall completeness percentage. An exception/deferred item is not a delivered artifact; any named gap or failed gate overrides aggregate counts.','','Semantic depth, cross-artifact consistency, security, full JSON Schema conformance, and diagram syntax/render/visual quality are NOT VERIFIED by this structural validator.']
    trace=['# Traceability report','','## Findings']+([f'- BLOCKER: {e}' for e in errors] or ['- No automated structural blockers detected.'])+['','## Not verified','- Semantic correctness, security, full JSON Schema conformance, and diagram syntax/rendering are not certified by this validator.']
    out=root/'validation'
    if out.is_symlink(): errors.append('validation report directory must not be a symbolic link')
    else:
        out.mkdir(exist_ok=True)
        import tempfile, os
        for name, payload in (("coverage-report.md", coverage), ("traceability-report.md", trace)):
            target = out / name
            if target.is_symlink() or (target.exists() and target.stat().st_nlink > 1):
                errors.append(f'validation report target must not be a symlink or hard link: {target}')
                continue
            fd, tmp_name = tempfile.mkstemp(prefix=f'.{name}.', dir=out)
            try:
                with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write('\n'.join(payload)+'\n'); fh.flush(); os.fsync(fh.fileno())
                os.replace(tmp_name, target)
            finally:
                if os.path.exists(tmp_name): os.unlink(tmp_name)
    return errors,counts

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('architecture_dir'); a=p.parse_args(); errs,counts=validate(a.architecture_dir)
    if errs:
        print(f'BLOCKED: {len(errs)} issue(s). Reports written to {Path(a.architecture_dir)/"validation"}/')
        for e in errs: print('- '+e)
        return 1
    print(f'PASS: structural/registry checks completed for {len(counts)} levels. Semantic, security, schema-conformance and renderer checks are not certified.')
    return 0
if __name__=='__main__': sys.exit(main())
