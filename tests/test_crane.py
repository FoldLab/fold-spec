import copy,math,unittest
from foldspec import ROOT,loads,validate_document,indexed,positions_at,norm,sub
from presentation import sample_step,sample_flourish,final_state

class CraneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=loads((ROOT/'examples/crane/crane.fold.json').read_bytes())
    def test_full_geometric_demonstration(self):
        r=validate_document(self.d);self.assertEqual(r['geometry']['operations'],40);self.assertEqual(r['steps'],44);self.assertLess(r['geometry']['maxMeasuredRelativeEdgeError'],.005)
    def test_subdivided_collapse_does_not_jump(self):
        ids=['begin-base','guide-pockets','lower-panel','flatten-base'];d=self.d
        for a,b in zip(ids,ids[1:]):
            p=sample_step(d,a,1)['positionsMm'];q=sample_step(d,b,0)['positionsMm'];self.assertEqual(p,q)
    def test_subdivided_collapse_matches_original_operation(self):
        d=self.d;a=sample_step(d,'begin-base',0);b=sample_step(d,'flatten-base',1);op=indexed(d['geometry']['operations'],'operation')[a['operation']];ms=indexed(d['geometry']['meshes'],'mesh')
        self.assertEqual(a['positionsMm'],positions_at(op,ms,0));self.assertEqual(b['positionsMm'],positions_at(op,ms,1))
    def test_text_counterpart_same_canonical_copy(self):
        t=loads((ROOT/'examples/crane/crane-text.fold.json').read_bytes());self.assertEqual([s['body'] for s in t['instructions']['steps']],[s['body'] for s in self.d['instructions']['steps']]);self.assertNotIn('geometry',t)
    def test_static_presentation_not_flourish_midframe(self):
        f=final_state(self.d);self.assertEqual(sample_flourish(self.d,0),f);self.assertEqual(sample_flourish(self.d,1),f);self.assertNotEqual(sample_flourish(self.d,.25),f)
    def test_every_operation_samples_finite_positions(self):
        d=self.d;ms=indexed(d['geometry']['meshes'],'mesh')
        for op in d['geometry']['operations']:
            for t in (0,.01,.18,.5,.88,.99999,1):
                with self.subTest(operation=op['id'],progress=t):
                    p=positions_at(op,ms,t);self.assertTrue(all(math.isfinite(x) for v in p for x in v))
    def test_review_claims_not_user_tested(self):
        self.assertNotEqual(self.d['accessibility']['review']['status'],'tested');self.assertNotEqual(self.d['geometry']['review']['status'],'tested');self.assertTrue(self.d['geometry']['limitations'])
