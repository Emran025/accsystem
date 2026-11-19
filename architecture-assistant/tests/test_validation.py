import json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from validate_architecture import validate
SAMPLE=Path(__file__).resolve().parents[1]/'examples'/'sample-system'
class ValidationTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)/'arch'
  import shutil; shutil.copytree(SAMPLE,self.root)
 def tearDown(self): self.tmp.cleanup()
 def edit(self,file,fn):
  p=self.root/file; x=json.loads(p.read_text()); fn(x);p.write_text(json.dumps(x,indent=2))
 def errs(self):return validate(self.root)[0]
 def test_sample_fixture_passes_registry_checks(self):self.assertEqual([],self.errs())
 def test_container_without_components(self):
  self.edit('registry/decomposition-map.json',lambda x:x['mappings'].__setitem__(slice(None),[m for m in x['mappings'] if m['parent_id']!='CNT-WEB']))
  self.assertTrue(any('CNT-WEB: missing component' in e for e in self.errs()))
 def test_component_without_code_mapping(self):
  self.edit('registry/decomposition-map.json',lambda x:x['mappings'].__setitem__(slice(None),[m for m in x['mappings'] if m['parent_id']!='CMP-WEB-FORM']))
  self.assertTrue(any('CMP-WEB-FORM: missing code-level' in e for e in self.errs()))
 def test_operation_without_function(self):
  self.edit('registry/decomposition-map.json',lambda x:x['mappings'].__setitem__(slice(None),[m for m in x['mappings'] if m['parent_id']!='OP-SHIPMENT-BOOKING']))
  self.assertTrue(any('OP-SHIPMENT-BOOKING: business operation has no function mapping' in e for e in self.errs()))
 def test_duplicate_element_ids(self):
  self.edit('registry/elements.json',lambda x:x['elements'].append(dict(x['elements'][0])))
  self.assertTrue(any('duplicate element ID SYS-PARCELFLOW' in e for e in self.errs()))
 def test_invalid_parent(self):
  self.edit('registry/elements.json',lambda x:x['elements'][3].update(parent_id='NO-SUCH-PARENT'))
  self.assertTrue(any('invalid parent reference NO-SUCH-PARENT' in e for e in self.errs()))
 def test_orphan_child(self):
  self.edit('registry/decomposition-map.json',lambda x:x['mappings'].__setitem__(slice(None),[m for m in x['mappings'] if 'CMP-WEB-FORM' not in m['child_ids']]))
  self.assertTrue(any('CMP-WEB-FORM: orphaned element' in e for e in self.errs()))
 def test_undocumented_exception(self):
  self.edit('registry/elements.json',lambda x:x['elements'][5].update(exception={'reason':'','approved':False}))
  self.assertTrue(any('CNT-DB: undocumented/unapproved' in e for e in self.errs()))
 def test_assistant_cannot_self_approve_exception(self):
  def make_self_approved(x):
   e=next(e for e in x['elements'] if e['id']=='CNT-DB');e['exception']['accepted_by']='Architecture Assistant Review'
  self.edit('registry/elements.json',make_self_approved)
  self.assertTrue(any('CNT-DB: assistant/model cannot self-approve' in e for e in self.errs()))
 def test_missing_decision_reference(self):
  self.edit('registry/decisions.json',lambda x:x['decisions'][0].update(affected_element_ids=['NO-SUCH']))
  self.assertTrue(any('ADR-001: missing decision reference' in e for e in self.errs()))
 def test_broken_markdown_reference(self):
  (self.root/'bad.md').write_text('[broken](absent.md)')
  self.assertTrue(any('broken/unsafe Markdown reference absent.md' in e for e in self.errs()))
 def test_markdown_reference_cannot_escape_project_root(self):
  outside=Path(self.tmp.name)/'outside.md';outside.write_text('not architecture evidence')
  (self.root/'bad.md').write_text('[outside](../outside.md)')
  self.assertTrue(any('broken/unsafe Markdown reference' in e for e in self.errs()))
 def test_interface_registry_references_are_checked(self):
  self.edit('registry/interfaces.json',lambda x:x['interfaces'][0].update(provider_id='NO-SUCH-SERVICE'))
  self.assertTrue(any('IF-CARRIER-001: invalid provider reference' in e for e in self.errs()))
 def test_malformed_reference_types_are_reported_without_crashing(self):
  self.edit('registry/interfaces.json',lambda x:x['interfaces'][0].update(consumer_ids=[{}]))
  self.assertTrue(any('invalid consumer reference' in e for e in self.errs()))
 def test_coverage_report_is_generated_with_gaps(self):
  self.edit('registry/decomposition-map.json',lambda x:x['mappings'].__setitem__(slice(None),[m for m in x['mappings'] if m['parent_id']!='CNT-WEB']))
  self.errs(); report=(self.root/'validation/coverage-report.md').read_text()
  self.assertIn('CNT-WEB',report);self.assertIn('CNT-WEB',report.split('Missing IDs')[1]);self.assertIn('Unmapped validation findings:',report);self.assertIn('Exceptions (not complete)',report);self.assertIn('do not establish semantic correctness',report)
 def test_exceptions_not_counted_as_decomposition_complete(self):
  _,counts=validate(self.root);row=counts['C2'];self.assertGreater(row['exceptions'],0);self.assertLess(row['decomposition_complete'],row['total']);self.assertLessEqual(row['decomposition_complete']+row['exceptions']+len(row['missing']),row['total'])
 def test_passed_gate_rejected_when_requirements_fail(self):
  self.edit('registry/decomposition-map.json',lambda x:x['mappings'].__setitem__(slice(None),[m for m in x['mappings'] if m['parent_id']!='CNT-WEB']))
  self.edit('registry/architecture-manifest.json',lambda x:x['stages'].update(C3='PASSED'))
  self.assertTrue(any('stage C3 marked PASSED' in e for e in self.errs()))
 def test_validation_gate_report_must_match_manifest_and_current_findings(self):
  (self.root/'validation/validation-status.md').write_text('| Gate 7 | Automated | **PASSED** | executed | details |\n')
  self.assertTrue(any('Gate 7 is PASSED but manifest validation stage is IN_PROGRESS' in e for e in self.errs()))
  self.assertTrue(any('Gate 7 marked PASSED despite current structural validation findings' in e for e in self.errs()))
 def test_hidden_backup_markdown_is_ignored(self):
  hidden=self.root/'.assistant-backups';hidden.mkdir();(hidden/'old.md').write_text('[stale](missing-file.md)')
  self.assertFalse(any('broken Markdown reference' in e for e in self.errs()))
 def test_diagram_unknown_id(self):
  with (self.root/'c1-context/context-diagram.md').open('a') as f:f.write('\n```mermaid\nflowchart LR\n X["CMP-NOPE"]\n```\n')
  self.assertTrue(any('diagram references unknown registry ID CMP-NOPE' in e for e in self.errs()))
if __name__=='__main__':unittest.main()
