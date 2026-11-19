"""Dependency-free document chunking and BM25 retrieval for architecture sources."""
from __future__ import annotations
import json, math, re
from pathlib import Path
from collections import Counter, defaultdict
TOKEN=re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_./:-]*|[\u0600-\u06ff]+")
STOP=set('a an and are as at be by can for from has have in into is it of on or that the this to was were with'.split())
SUPPORTED={'.md','.txt','.json'}
def tokenize(text): return [t.lower() for t in TOKEN.findall(text) if t.lower() not in STOP]
def extract(path):
 text=path.read_text(encoding='utf-8',errors='replace')
 if path.suffix.lower()=='.json':
  try:text=json.dumps(json.loads(text),ensure_ascii=False,indent=2)
  except json.JSONDecodeError: pass
 return text
def chunks(text,max_chars=1200,overlap=120):
 # Keep paragraph/heading context and bound chunk size; split overlong paragraphs safely.
 paras=[]
 for para in re.split(r'\n\s*\n',text):
  para=para.strip()
  while len(para)>max_chars:
   cut=para.rfind(' ',0,max_chars)
   if cut<max_chars//2:cut=max_chars
   paras.append(para[:cut]); para=para[max(0,cut-overlap):]
  if para:paras.append(para)
 out=[]; current=''
 for para in paras:
  candidate=(current+'\n\n'+para).strip() if current else para
  if len(candidate)>max_chars and current:out.append(current);current=para
  else:current=candidate
 if current:out.append(current)
 return out
def build(source_dir,index_path):
 source=Path(source_dir).resolve(); out=Path(index_path).resolve(); docs=[]
 for p in sorted(source.rglob('*')):
  if p.is_symlink() or not p.is_file() or p.stat().st_nlink>1 or p.suffix.lower() not in SUPPORTED or p.resolve()==out or any(part.startswith('.') for part in p.relative_to(source).parts):continue
  rel=p.relative_to(source).as_posix(); text=extract(p)
  for no,chunk in enumerate(chunks(text),1):
   toks=tokenize(chunk)
   if toks:docs.append({'id':f'{rel}#{no:04d}','source':rel,'chunk':no,'text':chunk,'tokens':toks})
 payload={'format':'architecture-assistant-bm25-v1','source_root':str(source),'document_count':len(docs),'documents':docs}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
 return payload

def search(index_path,query,top_k=5,k1=1.5,b=.75):
 idx=json.loads(Path(index_path).read_text(encoding='utf-8')); docs=idx.get('documents',[]); q=Counter(tokenize(query))
 if not q:return []
 n=len(docs); avgdl=sum(len(d['tokens']) for d in docs)/max(n,1); df=Counter(t for d in docs for t in set(d['tokens'])); results=[]
 for d in docs:
  tf=Counter(d['tokens']); dl=len(d['tokens']); score=0.0
  for t,qtf in q.items():
   if not tf[t]:continue
   idf=math.log(1+(n-df[t]+0.5)/(df[t]+0.5)); denom=tf[t]+k1*(1-b+b*dl/max(avgdl,1))
   score+=idf*(tf[t]*(k1+1)/denom)*(1+math.log(qtf))
  if score>0:results.append({'id':d['id'],'source':d['source'],'chunk':d['chunk'],'score':round(score,6),'text':d['text']})
 return sorted(results,key=lambda x:(-x['score'],x['source'],x['chunk']))[:max(1,top_k)]
