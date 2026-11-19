import argparse
from pathlib import Path
from indexer import build,search

def main():
 p=argparse.ArgumentParser(description='Build/search the local architecture knowledge index (BM25, no external service).');s=p.add_subparsers(dest='cmd',required=True)
 b=s.add_parser('index');b.add_argument('source');b.add_argument('--output',default='.rag/index.json')
 q=s.add_parser('search');q.add_argument('query');q.add_argument('--index',default='.rag/index.json');q.add_argument('-k',type=int,default=5)
 a=p.parse_args()
 if a.cmd=='index':
  x=build(a.source,a.output);print(f'Indexed {x["document_count"]} chunks from {x["source_root"]} -> {Path(a.output).resolve()}')
 else:
  for r in search(a.index,a.query,a.k):print(f'[{r["score"]:.3f}] {r["source"]}#{r["chunk"]}\n{r["text"]}\n')
if __name__=='__main__':main()
