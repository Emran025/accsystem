import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'rag'))
from indexer import build,search,chunks
class RagTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'docs';self.root.mkdir();(self.root/'a.md').write_text('# Idempotency\n\nBooking retries use the same idempotency key to avoid duplicate carrier shipments.');(self.root/'b.md').write_text('# Persistence\n\nShipment records are stored in the relational parcel database.')
  self.index=Path(self.tmp.name)/'index.json';build(self.root,self.index)
 def tearDown(self):self.tmp.cleanup()
 def test_rank_relevant_source_with_citation(self):
  r=search(self.index,'idempotency carrier duplicate shipment retry',2);self.assertTrue(r);self.assertEqual('a.md',r[0]['source']);self.assertIn('id',r[0]);self.assertIn('text',r[0])
 def test_empty_or_unmatched_query_returns_no_claim(self):self.assertEqual([],search(self.index,'zzznomatch',5));self.assertEqual([],search(self.index,'the and of',5))
 def test_chunker_bounds_long_text(self):self.assertTrue(all(len(x)<=1200 for x in chunks('word '*2000)))
 def test_external_symlink_is_not_indexed(self):
  secret=Path(self.tmp.name)/'outside.md';secret.write_text('unique external confidential token')
  link=self.root/'linked.md'
  try:link.symlink_to(secret)
  except OSError:self.skipTest('symbolic links are unavailable on this filesystem')
  idx=Path(self.tmp.name)/'fresh-index.json';build(self.root,idx)
  self.assertEqual([],search(idx,'confidential unique external'))
 def test_hard_linked_source_is_not_indexed(self):
  outside=Path(self.tmp.name)/'hardlink-source.md';outside.write_text('unique hidden hardlink material')
  try:(self.root/'hardlink.md').hardlink_to(outside)
  except OSError:self.skipTest('hard links are unavailable on this filesystem')
  idx=Path(self.tmp.name)/'fresh-index.json';build(self.root,idx)
  self.assertEqual([],search(idx,'hidden hardlink material'))
if __name__=='__main__':unittest.main()
