import io,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'agent'))
from runtime import ArchitectureTools,AgentError,run_turn,load_instructions,SessionStore
class FakeClient:
 def __init__(self,responses):self.responses=iter(responses);self.calls=0
 def chat(self,*args,**kwargs):self.calls+=1;return next(self.responses)
def tool_call(name,args='{}',callid='c1'):
 return {'choices':[{'message':{'role':'assistant','content':None,'tool_calls':[{'id':callid,'type':'function','function':{'name':name,'arguments':args}}]}}]}
class RuntimeTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'system';self.root.mkdir();(self.root/'README.md').write_text('# Test\n\nContainer CNT-API validates shipment requests.');self.out=io.StringIO()
 def tearDown(self):self.tmp.cleanup()
 def test_autonomous_write_by_default(self):
  t=ArchitectureTools(self.root,stdout=self.out);r=t.write_file('new.md','# proposal');self.assertEqual('WRITTEN',r['status']);self.assertEqual('# proposal',(self.root/'new.md').read_text())
 def test_explicit_policy_denial_never_mutates(self):
  t=ArchitectureTools(self.root,approval=lambda *a:False,stdout=self.out);r=t.write_file('new.md','# proposal');self.assertEqual('DENIED',r['status']);self.assertFalse((self.root/'new.md').exists())
 def test_autonomous_update_creates_backup(self):
  p=self.root/'note.md';p.write_text('old');t=ArchitectureTools(self.root,stdout=self.out);r=t.write_file('note.md','new');self.assertEqual('new',p.read_text());self.assertTrue((self.root/r['backup']).is_file())
 def test_path_traversal_and_hidden_paths_rejected(self):
  t=ArchitectureTools(self.root,approval=lambda *a:True)
  with self.assertRaises(AgentError):t.read_file('../outside')
  with self.assertRaises(AgentError):t.read_file('docs/../README.md')
  with self.assertRaises(AgentError):t.write_file('.rag/index.json','bad')
 def test_hard_linked_file_is_not_read_or_overwritten(self):
  original=self.root/'note.md';original.write_text('sensitive');linked=self.root/'alias.md'
  try:linked.hardlink_to(original)
  except OSError:self.skipTest('hard links are unavailable on this filesystem')
  t=ArchitectureTools(self.root,approval=lambda *a:True)
  with self.assertRaises(AgentError):t.read_file('alias.md')
  with self.assertRaises(AgentError):t.write_file('alias.md','changed')
  self.assertEqual('sensitive',original.read_text())
 def test_core_diagram_and_microservices_policies_are_loaded(self):
  prompt=load_instructions(['diagram-selection','architecture-style'])
  self.assertIn('OUTPUT-DEPTH-AND-AMPLIFIER.md',prompt)
  self.assertIn('Final-stage amplifier',prompt)
  self.assertIn('CONSISTENCY-AND-POLISH-POLICY.md',prompt)
  self.assertIn('fixed-point process',prompt)
  self.assertIn('diagram-coverage-matrix.md',prompt)
  self.assertIn('validate_consistency_artifacts',prompt)
  self.assertIn('diagram-selection-policy.md',prompt)
  self.assertIn('system-landscape',prompt)
  self.assertIn('System size alone',prompt)
  self.assertIn('microservices',prompt.lower())
 def test_tool_loop_runs_read_tool_then_returns_final(self):
  t=ArchitectureTools(self.root,approval=lambda *a:False)
  c=FakeClient([tool_call('read_architecture_file',json.dumps({'path':'README.md'})),{'choices':[{'message':{'role':'assistant','content':'Evidence: README.md confirms CNT-API validates requests.'}}]}]);msgs=[{'role':'user','content':'What does the API do?'}]
  answer=run_turn(c,t,'test-model',msgs,skill_ids=['discovery']);self.assertIn('CNT-API',answer);self.assertEqual(2,c.calls);self.assertTrue(any(m.get('role')=='tool' for m in msgs))
 def test_checkpoint_round_trip_and_portable_handoff(self):
  s=SessionStore(self.root,'review-1');s.state['task']='Analyze a booking platform';s.record_stage('discovery','COMPLETE','Reviewed requirements and source inventory.',['Reconcile scope conflicts.'],['00-scope.md'],[]);s.save([{'role':'user','content':'Analyze'}],model='model-a')
  restored=SessionStore(self.root,'review-1');state=restored.load();self.assertEqual('discovery',state['current_stage']);self.assertIn('discovery',state['completed_stages']);self.assertTrue(restored.portable_path.is_file());self.assertIn('Reconcile scope conflicts.',restored.portable_path.read_text())
 def test_step_limit_saves_resumable_tool_results(self):
  s=SessionStore(self.root,'paused-1');tools=ArchitectureTools(self.root,session=s);c=FakeClient([tool_call('read_architecture_file',json.dumps({'path':'README.md'}))]);messages=[{'role':'user','content':'Inspect README'}]
  answer=run_turn(c,tools,'test-model',messages,max_steps=1,session=s);state=SessionStore(self.root,'paused-1').load()
  self.assertIn('Paused safely',answer);self.assertEqual('PAUSED_AT_STEP_LIMIT',state['status']);self.assertTrue(any(m.get('role')=='tool' for m in state['messages']))
 def test_truncated_file_read_names_range_and_next_line(self):
  p=self.root/'long.md';p.write_text('\n'.join(f'line {i}' for i in range(1,1001)));tools=ArchitectureTools(self.root)
  part=tools.read_file('long.md',20,900);self.assertTrue(part['truncated']);self.assertEqual(20,part['start_line']);self.assertEqual(part['end_line']+1,part['next_start_line']);self.assertIn('explicitly bounded',part['notice'])
 def test_provider_output_length_is_continued_not_reported_as_final(self):
  s=SessionStore(self.root,'length-1');tools=ArchitectureTools(self.root,session=s);c=FakeClient([{'choices':[{'finish_reason':'length','message':{'role':'assistant','content':'partial'}}]},{'choices':[{'finish_reason':'stop','message':{'role':'assistant','content':'completed answer'}}]}]);messages=[{'role':'user','content':'Write detailed analysis'}]
  answer=run_turn(c,tools,'test-model',messages,max_steps=3,session=s);self.assertEqual('completed answer',answer);self.assertEqual(2,c.calls);self.assertIn('Continue from the exact point',messages[-2]['content'])
 def test_stage_checkpoint_tool_is_exposed(self):
  tools=ArchitectureTools(self.root,session=SessionStore(self.root,'tool-1'));names=[x['function']['name'] for x in tools.tool_specs()]
  self.assertIn('checkpoint_architecture_stage',names)
 def test_runtime_depth_review_tool_writes_report_and_returns_findings(self):
  (self.root/'registry').mkdir();(self.root/'registry/elements.json').write_text(json.dumps({'elements':[{'id':'CNT-API','level':'C2','scope_status':'IN_SCOPE','doc':'README.md'}]}))
  tools=ArchitectureTools(self.root);result=tools.call('review_artifact_depth',{})
  self.assertEqual('BLOCKED_FOR_CONTENT_REVIEW',result['status']);self.assertGreater(len(result['findings']),0);self.assertTrue((self.root/'validation/depth-review-report.md').is_file())
 def test_runtime_consistency_validator_tool_is_exposed(self):
  tools=ArchitectureTools(self.root);names=[item['function']['name'] for item in tools.tool_specs()];self.assertIn('validate_consistency_artifacts',names)
  result=tools.call('validate_consistency_artifacts',{});self.assertEqual('BLOCKED',result['status']);self.assertTrue((self.root/'validation/consistency-artifact-validation.md').is_file())
 def test_model_stage_checkpoint_is_persisted(self):
  s=SessionStore(self.root,'stage-tool-1');tools=ArchitectureTools(self.root,session=s);args={'stage':'C2','status':'COMPLETE','summary':'Container inventory reconciled.','next_actions':['Start selected C3 work.'],'artifacts':['c2-containers/container-catalog.md'],'blockers':[]}
  c=FakeClient([tool_call('checkpoint_architecture_stage',json.dumps(args)),{'choices':[{'finish_reason':'stop','message':{'role':'assistant','content':'C2 checkpointed.'}}]}]);messages=[{'role':'user','content':'Checkpoint C2'}]
  self.assertIn('checkpointed',run_turn(c,tools,'test-model',messages,session=s));saved=SessionStore(self.root,'stage-tool-1').load();self.assertEqual('COMPLETE',saved['stage_status']['C2']);self.assertIn('Start selected C3 work.',saved['next_actions']);self.assertIn('c2-containers/container-catalog.md',s.portable_path.read_text())
if __name__=='__main__':unittest.main()
