import copy,json,math,unittest
from foldspec import ROOT,SpecError,loads,validate_document,positions_at,indexed,resolve_locale,html_export,text_export,json_bytes,digest,safe_path,safe_https

def example(name='hinge/center-fold.fold.json'):
    return loads((ROOT/'examples'/name).read_bytes())

class JsonTests(unittest.TestCase):
    def test_valid_unicode(self):self.assertEqual(loads('{"crane":"鶴"}'),{'crane':'鶴'})
    def test_duplicate_keys(self):
        with self.assertRaisesRegex(SpecError,'E_DUPLICATE_KEY'):loads('{"a":1,"a":2}')
    def test_nan(self):
        with self.assertRaisesRegex(SpecError,'E_NUMBER'):loads('{"a":NaN}')
    def test_overflow(self):
        with self.assertRaisesRegex(SpecError,'E_NUMBER'):loads('{"a":1e400}')
    def test_bom(self):
        with self.assertRaisesRegex(SpecError,'E_ENCODING'):loads(b'\xef\xbb\xbf{}')
    def test_bad_utf8(self):
        with self.assertRaisesRegex(SpecError,'E_ENCODING'):loads(b'\xff')
    def test_surrogate(self):
        with self.assertRaisesRegex(SpecError,'E_UNICODE'):loads('"\\ud800"')
    def test_depth(self):
        with self.assertRaisesRegex(SpecError,'E_LIMIT'):loads('['*100+'0'+']'*100)
    def test_zero_character(self):
        with self.assertRaisesRegex(SpecError,'E_UNICODE'):loads('"\\u0000"')
    def test_safe_paths(self):
        for path in ['assets/a.png','assets/paper-1.png','library/base.json']:self.assertEqual(safe_path(path),path)
    def test_unsafe_paths(self):
        for path in ['../x','/x','C:/x','a//b','a/./b','a/../b','con.txt','folder/COM1.png','a\\b','a.']:
            with self.subTest(path=path),self.assertRaises(SpecError):safe_path(path)
    def test_https_not_credentials(self):
        safe_https('https://example.com/audio/step.mp3')
        for url in ['http://example.com','javascript:alert(1)','https://u:p@example.com/file','https://example.com\\evil','https://example.com/\nfile']:
            with self.subTest(url=url),self.assertRaises(SpecError):safe_https(url)

class DocumentTests(unittest.TestCase):
    def setUp(self):self.d=example()
    def bad(self,code):
        with self.assertRaisesRegex(SpecError,code):validate_document(self.d)
    def test_analytic_document(self):self.assertEqual(validate_document(self.d)['geometry']['operations'],2)
    def test_no_mutation(self):
        before=json_bytes(self.d);validate_document(self.d);self.assertEqual(json_bytes(self.d),before)
    def test_unknown_root_field(self):self.d['execute']='anything';self.bad('E_SCHEMA')
    def test_future_version(self):self.d['specVersion']='20.0.0';self.bad('E_SCHEMA')
    def test_missing_default_locale(self):self.d['metadata']['title']={'fr':'Grue'};self.bad('E_LOCALE')
    def test_case_duplicate_locale(self):self.d['metadata']['title']['EN']='Other';self.bad('E_LOCALE')
    def test_step_duplicate(self):self.d['instructions']['steps'].append(copy.deepcopy(self.d['instructions']['steps'][0]));self.bad('E_DUPLICATE_ID')
    def test_undefined_landmark(self):self.d['instructions']['steps'][0]['tactile']['landmarkIds']=['nope'];self.bad('E_REFERENCE')
    def test_review_claim_requires_evidence(self):self.d['accessibility']['review']={'status':'tested'};self.bad('E_REVIEW')
    def test_planned_cannot_contain_geometry(self):self.d['status']='planned';self.bad('E_SCHEMA')
    def test_text_cannot_contain_geometry(self):self.d['status']='instructions';self.bad('E_SCHEMA')
    def test_resolved_missing_action(self):
        s=self.d['instructions']['steps'][1];s['animation']='not-authored';s['runs']=[];self.bad('E_RUN_COVERAGE')
    def test_run_gap(self):self.d['instructions']['steps'][1]['runs'][0]['from']=.1;self.bad('E_RUN_COVERAGE')
    def test_reversed_run(self):self.d['instructions']['steps'][1]['runs'][0]['to']=0;self.bad('E_TIME')
    def test_partial_prefix_cannot_restart(self):
        self.d['status']='partial';self.d['geometry']['status']='partial';del self.d['presentation']
        s=copy.deepcopy(self.d['instructions']['steps'][0]);s.update(id='manual-gap',kind='shape',animation='not-authored')
        self.d['instructions']['steps'].insert(2,s);self.bad('E_RUN_COVERAGE')
    def test_illegal_face_winding(self):self.d['geometry']['meshes'][0]['faces'][0]['vertices'].reverse();self.bad('E_TOPOLOGY')
    def test_out_of_bounds_material(self):self.d['geometry']['meshes'][0]['vertices'][0]['uvMm'][0]=999;self.bad('E_MATERIAL')
    def test_unknown_moving_face(self):self.d['geometry']['operations'][0]['movingFaces']=['missing'];self.bad('E_SELECTION')
    def test_shared_hinge_must_join(self):
        op=self.d['geometry']['operations'][0];op['axisMm']=[[2,-75,0],[2,75,0]];self.bad('E_TEAR')
    def test_geometry_does_not_teleport(self):
        op=self.d['geometry']['operations'][1];op['startPositionsMm']=[[x+1,y,z] for x,y,z in op['startPositionsMm']];op['axisMm']=[[x+1,y,z] for x,y,z in op['axisMm']];self.bad('E_CONTINUITY')
    def test_first_state_must_be_flat(self):
        op=self.d['geometry']['operations'][0];op['startPositionsMm']=[[x,y,z+1] for x,y,z in op['startPositionsMm']];op['axisMm']=[[x,y,z+1] for x,y,z in op['axisMm']];self.bad('E_INITIAL')
    def test_paper_dimensional_edge_budget(self):self.d['geometry']['operations'][0]['startPositionsMm'][0][0]-=1;self.bad('E_STRAIN')
    def test_invalid_camera(self):self.d['instructions']['steps'][0]['camera']['up']=[0,0,0];self.bad('E_CAMERA')
    def test_narration_hash_checked(self):self.d['narration'][0]['textSha256']='0'*64;self.bad('E_NARRATION_HASH')
    def test_narration_ready_matches_text(self):
        n=self.d['narration'][0];n.update(status='ready',url='https://example.com/audio.mp3');validate_document(self.d)
        self.d['instructions']['steps'][1]['body']['en']+=' Changed.';self.bad('E_NARRATION_STALE')
    def test_narration_missing_not_playable(self):self.d['narration'][0]['url']='https://example.com/file';self.bad('E_NARRATION')
    def test_narration_reference_owns_step(self):
        self.d['instructions']['steps'][0]['narrationIds']=[self.d['narration'][0]['id']];self.bad('E_REFERENCE')
    def test_narration_url_credentials(self):
        self.d['narration'][0].update(status='ready',url='https://secret:pass@example.com/audio');self.bad('E_URL')
    def test_flourish_requires_axis(self):del self.d['presentation']['flourish']['axisMm'];self.bad('E_AXIS')
    def test_print_references_real_step(self):self.d['print']['panels'][0]['step']='nonexistent';self.bad('E_REFERENCE')
    def test_authoring_cycle(self):
        self.d=example('authoring/named-fold.fold.json');a=self.d['authoring'];a['points'][0]['definition']={'kind':'midpoint','a':a['points'][0]['id'],'b':a['points'][1]['id']};self.bad('E_CYCLE')
    def test_authoring_wrong_reference_type(self):
        self.d=example('authoring/named-fold.fold.json');self.d['authoring']['lines'][0]['definition']['constraint']['a']='center-crease';self.bad('E_REFERENCE')
    def test_sampled_intermediate_shrink_detected(self):
        self.d=example();g=self.d['geometry'];op=g['operations'][0];ps=op['startPositionsMm'];m=g['meshes'][0]
        motion={'id':op['id'],'sheet':op['sheet'],'mesh':op['mesh'],'durationMs':1000,'kind':'sampled','creases':[],'layers':[],'interpolation':'linear','maxRelativeEdgeError':.005,
                'keys':[{'at':0,'positionsMm':ps},{'at':1,'positionsMm':[[-x,-y,z] for x,y,z in ps]}]}
        g['operations'][0]=motion;self.bad('E_STRAIN')
    def test_fold_unfold_returns_start(self):
        ms=indexed(self.d['geometry']['meshes'],'mesh');ops=self.d['geometry']['operations']
        for p,q in zip(positions_at(ops[0],ms,0),positions_at(ops[-1],ms,1)):
            self.assertLess(math.dist(p,q),1e-9)
    def test_unknown_mandatory_extension_metadata_preserved(self):
        self.d['extensions']=[{'id':'org.example:future-joint','version':'1.0.0','requiredFor':['playback'],'data':{'enabled':True}}]
        validate_document(self.d)
        from presentation import final_state
        with self.assertRaisesRegex(SpecError,'E_UNSUPPORTED'):final_state(self.d)
    def test_locale_fallback_and_language(self):
        d=example('minimal-text/first-fold.fold.json');d['metadata']['title']['fr']='Premier pli'
        self.assertEqual(resolve_locale(d['metadata']['title'],'fr-CA','en'),('fr','Premier pli'))
        h=html_export(d,'fr-CA',True);self.assertIn('lang="fr">Premier pli',h);self.assertIn('lang="en"',h)
    def test_export_escapes_html(self):
        self.d['instructions']['steps'][0]['body']['en']='<script>alert(1)</script>'
        h=html_export(self.d,descriptive=True);self.assertNotIn('<script>',h);self.assertIn('&lt;script&gt;',h)
    def test_text_view_keeps_source_and_limitations(self):
        d=example('crane/crane-text.fold.json');t=text_export(d,descriptive=True)
        self.assertIn('FINAL PRESENTATION',t);self.assertIn('LIMITATIONS',t);self.assertIn('https://www.city.hiroshima',t)
    def test_text_only_never_resolves_geometry(self):
        d=example('minimal-text/first-fold.fold.json');r=validate_document(d);self.assertEqual(r['geometry']['checks'],'no-geometry');self.assertIn('Animation not authored',html_export(d))

    def test_physical_action_not_disguised_as_check(self):
        self.d['instructions']['steps'][1]['runs']=[];self.d['instructions']['steps'][1]['animation']='not-applicable';self.bad('E_STATUS')
    def test_text_required_extension_not_silently_ignored(self):
        self.d['extensions']=[{'id':'org.example:dependent-copy','version':'1.0.0','requiredFor':['text'],'data':{}}]
        with self.assertRaisesRegex(SpecError,'E_UNSUPPORTED'):html_export(self.d)
        with self.assertRaisesRegex(SpecError,'E_UNSUPPORTED'):text_export(self.d)
    def test_optional_extension_retained(self):
        self.d['extensions']=[{'id':'org.example:catalog-note','version':'1.0.0','requiredFor':[],'data':{'note':'extra'}}]
        validate_document(self.d);self.assertTrue(text_export(self.d))
    def test_named_material_point_must_lie_on_paper(self):
        self.d=example('authoring/named-fold.fold.json');self.d['authoring']['points'][0]['definition']['uvMm']=[10000,10000];self.bad('E_MATERIAL')
    def test_export_retains_rights_and_qualifications(self):
        self.d['metadata']['rightsNote']={'en':'Example rights notice'}
        self.d['metadata']['sources']=[{'id':'research','title':'Research','url':'https://example.com/source','rightsNote':'Source rights retained'}]
        self.d['history']=[{'id':'context','scope':'symbol','title':{'en':'Context'},'summary':{'en':'A qualified example'},'sourceIds':['research'],'qualifications':[{'en':'Not a claim about this exact construction.'}],'review':{'status':'authored'}}]
        for text in (text_export(self.d),html_export(self.d)):
            self.assertIn('Example rights notice',text);self.assertIn('Source rights retained',text);self.assertIn('Not a claim about this exact construction.',text)

    def test_intent_material_filter_inside_sheet(self):
        self.d=example('authoring/named-fold.fold.json')
        self.d['authoring']['intents'][0]['materialFilter']=[[[-75,-75],[0,-75],[0,75],[-75,75]]]
        validate_document(self.d)
    def test_intent_material_filter_outside_sheet_rejected(self):
        self.d=example('authoring/named-fold.fold.json')
        self.d['authoring']['intents'][0]['materialFilter']=[[[-90,-75],[0,-75],[0,75]]]
        self.bad('E_MATERIAL')
