import math,unittest
from foldspec import ROOT,loads,indexed,positions_at,mesh_edges
from presentation import final_state,sample_flourish,flourish_angle,sample_step

class PresentationTests(unittest.TestCase):
    def setUp(self):self.d=loads((ROOT/'examples/presentation/wing-rig.fold.json').read_bytes())
    def test_endpoints_exact(self):
        final=final_state(self.d);self.assertEqual(sample_flourish(self.d,0),final);self.assertEqual(sample_flourish(self.d,1),final)
    def test_reduced_motion_still(self):self.assertEqual(sample_flourish(self.d,.38,True),final_state(self.d))
    def test_flourish_has_visible_motion(self):self.assertNotEqual(sample_flourish(self.d,.35),final_state(self.d))
    def test_shared_axis_stays_fixed(self):
        a=final_state(self.d)['paper'];b=sample_flourish(self.d,.35)['paper']
        for p,q in zip(a['positionsMm'],b['positionsMm']):
            if abs(p[0])<1e-10:self.assertLess(math.dist(p,q),1e-9)
    def test_wing_lengths_preserved(self):
        a=final_state(self.d)['paper'];b=sample_flourish(self.d,.35)['paper']
        for i,j in mesh_edges(a['mesh']):self.assertAlmostEqual(math.dist(a['positionsMm'][i],a['positionsMm'][j]),math.dist(b['positionsMm'][i],b['positionsMm'][j]),places=9)
    def test_source_is_immutable(self):
        before=repr(self.d);sample_flourish(self.d,.35);self.assertEqual(repr(self.d),before)
    def test_bounded_angle(self):
        f=self.d['presentation']['flourish'];self.assertLessEqual(max(abs(flourish_angle(f,t/200)) for t in range(201)),f['amplitudeDeg'])
    def test_duration_weighted_step(self):
        d=loads((ROOT/'examples/hinge/center-fold.fold.json').read_bytes());s=d['instructions']['steps'][1];sample=sample_step(d,s['id'],.5)
        ms=indexed(d['geometry']['meshes'],'mesh');op=d['geometry']['operations'][0];self.assertEqual(sample['positionsMm'],positions_at(op,ms,.5))
    def test_no_animation_invented(self):
        d=loads((ROOT/'examples/minimal-text/first-fold.fold.json').read_bytes());self.assertEqual(sample_step(d,d['instructions']['steps'][1]['id'],.5)['samples'],[])
