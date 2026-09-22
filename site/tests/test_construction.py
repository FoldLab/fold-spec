import math,unittest
from construction import canonical,through,reflect_point,intersect,enumerate_solutions,choose,witness_residuals
from foldspec import SpecError,norm,sub

class ConstructionTests(unittest.TestCase):
    def setUp(self):
        self.points={'a':[-2,1],'b':[2,1],'p':[-2,1],'q':[0,3]}
        self.lines={'x':canonical([1,0],0),'y':canonical([0,1],0),'right':canonical([1,0],2),'far':canonical([1,0],4)}
    def test_canonical_sign(self):self.assertEqual(canonical([-2,0],-4),canonical([1,0],2))
    def test_line_through(self):self.assertEqual(through([-1,2],[3,2]),canonical([0,1],2))
    def test_reflection(self):self.assertEqual(reflect_point([-2,1],canonical([1,0],0)),[2,1])
    def test_intersection(self):self.assertEqual(intersect(self.lines['right'],canonical([0,1],3)),[2,3])
    def test_parallel_intersection_rejected(self):
        with self.assertRaises(SpecError):intersect(self.lines['right'],self.lines['far'])
    def test_coincident_points_rejected(self):
        with self.assertRaises(SpecError):enumerate_solutions({'kind':'point-to-point','a':'a','b':'a'},self.points,self.lines)
    def test_point_alignment(self):
        r=choose({'kind':'point-to-point','a':'a','b':'b'},{'mode':'unique'},self.points,self.lines)
        self.assertEqual(r,canonical([1,0],0))
    def test_two_line_bisectors(self):
        c={'kind':'line-to-line','a':'x','b':'y'};s=enumerate_solutions(c,self.points,self.lines)
        self.assertEqual(len(s),2)
        for w in s:self.assertLess(witness_residuals(c,w,self.points,self.lines)['positionMm'],1e-8)
    def test_ambiguity_not_silently_resolved(self):
        with self.assertRaisesRegex(SpecError,'E_AMBIGUOUS'):choose({'kind':'line-to-line','a':'x','b':'y'},{'mode':'unique'},self.points,self.lines)
    def test_parallel_line_midway(self):
        c={'kind':'line-to-line','a':'right','b':'far'}
        self.assertEqual(choose(c,{'mode':'unique'},self.points,self.lines),canonical([1,0],3))
    def test_wrong_witness(self):
        with self.assertRaisesRegex(SpecError,'E_CONSTRAINT'):choose({'kind':'point-to-point','a':'a','b':'b'},{'mode':'witness','normal':[0,1],'offsetMm':0},self.points,self.lines)
    def test_all_seven_witness_families(self):
        examples=[
          ({'kind':'through-points','a':'a','b':'b'},canonical([0,1],1)),
          ({'kind':'point-to-point','a':'a','b':'b'},canonical([1,0],0)),
          ({'kind':'line-to-line','a':'x','b':'y'},canonical([1,1],0)),
          ({'kind':'perpendicular-through','line':'y','point':'q'},canonical([1,0],0)),
          ({'kind':'point-to-line-through','point':'p','line':'right','through':'q'},canonical([1,0],0)),
          ({'kind':'two-points-to-lines','a':'p','lineA':'right','b':'a','lineB':'right'},canonical([1,0],0)),
          ({'kind':'point-to-line-perpendicular','point':'p','line':'right','perpendicularTo':'y'},canonical([1,0],0))]
        for c,w in examples:
            with self.subTest(family=c['kind']):
                r=choose(c,{'mode':'witness',**w},self.points,self.lines)
                self.assertLess(witness_residuals(c,r,self.points,self.lines)['positionMm'],1e-7)
    def test_unsupported_enumeration_explicit(self):
        with self.assertRaisesRegex(SpecError,'E_SOLVER_UNSUPPORTED'):enumerate_solutions({'kind':'two-points-to-lines'},self.points,self.lines)
    def test_distance_and_angle_are_separate(self):
        r=witness_residuals({'kind':'perpendicular-through','line':'y','point':'q'},canonical([1,1],0),self.points,self.lines)
        self.assertAlmostEqual(r['angularDeg'],45);self.assertGreater(r['positionMm'],2)
