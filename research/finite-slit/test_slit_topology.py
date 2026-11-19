import unittest
from slit_topology import welded_corners, resolve_frontmost_layer, derive_overlap_patches, remesh_single_triangle_slit
from fractions import Fraction

# Fan triangulation around interior pivot 4. Chord 0-4 is cut.
# The slit banks duplicate point 0, but stay welded at point 4 (finite stop).
FACES = [(0,1,4),(1,2,4),(2,3,4),(3,0,4)]
SLIT = frozenset((0,4))
class SlitConnectivity(unittest.TestCase):
    def test_two_banks_and_single_tip(self):
        ids = welded_corners(FACES, {SLIT})
        self.assertNotEqual(ids[0,0], ids[3,0])
        self.assertEqual(len({ids[i,4] for i in range(4)}), 1)
        self.assertEqual(ids[0,1], ids[1,1])
    def test_unselected_substrate_connectivity(self):
        # Centroid-projected overlap is irrelevant: underlying material IDs are distinct.
        faces = FACES + [tuple(v+5 for v in f) for f in FACES]
        ids = welded_corners(faces,{SLIT})
        self.assertEqual(ids[4,5], ids[7,5])
        self.assertNotEqual(ids[4,5], ids[0,0])
    def test_uncut_sheet_corners_remain_welded(self):
        # Include another part receiving a slit; original sheet untouched.
        faces = FACES + [tuple(v+5 for v in f) for f in FACES]
        ids = welded_corners(faces,{frozenset((5,9))})
        self.assertEqual(ids[0,0], ids[3,0])
    def test_fold_one_bank_only_requires_slit(self):
        # Rotate triangle 0 around the hinge 1--4. Its corner 0 moves;
        # without the slit, stationary triangle 3 shares that material corner.
        def off_hinge_weld(ids):
            return any(f != 0 and key == ids[0,0] for (f, p), key in ids.items())
        self.assertFalse(off_hinge_weld(welded_corners(FACES, {SLIT})))
        other = [tuple(v+5 for v in f) for f in FACES]
        self.assertTrue(off_hinge_weld(welded_corners(FACES+other, {frozenset((5,9))})))
    def test_boundary_edge_rejected(self):
        with self.assertRaises(ValueError):
            welded_corners(FACES,{frozenset((0,1))})

class LayerResolution(unittest.TestCase):
    def test_explicit_layer_proven_front_across_patches(self):
        self.assertEqual(resolve_frontmost_layer('flap', [
            ({'flap', 'middle', 'base'}, [('flap', 'middle'), ('middle', 'base')]),
            ({'flap', 'base'}, [('flap', 'base')]),
            ({'flap'}, []),
        ]), 'flap')

    def test_identifiers_alone_do_not_break_overlap_tie(self):
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            resolve_frontmost_layer('flap', [({'base', 'flap'}, [])])

    def test_order_reversal_blocks_finite_path(self):
        with self.assertRaisesRegex(ValueError, 'hidden'):
            resolve_frontmost_layer('flap', [
                ({'flap', 'base'}, [('flap', 'base')]),
                ({'flap', 'base'}, [('base', 'flap')]),
            ])

    def test_missing_coverage(self):
        with self.assertRaisesRegex(ValueError, 'full path'):
            resolve_frontmost_layer('flap', [({'base'}, [])])
        with self.assertRaisesRegex(ValueError, 'missing'):
            resolve_frontmost_layer('flap', [])

    def test_cycles_below_front_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'cyclic'):
            resolve_frontmost_layer('flap', [
                ({'flap', 'base', 'middle'},
                 [('flap', 'middle'), ('middle', 'base'), ('base', 'middle')]),
            ])

    def test_reference_outside_local_patch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'invalid'):
            resolve_frontmost_layer('flap', [({'flap'}, [('flap', 'base')])])


class GeometricPartition(unittest.TestCase):
    def rect(self, x0, x1, y0=-2, y1=2, z=0):
        return [(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)]

    def patches(self, other, witnesses=()):
        return derive_overlap_patches((0,0,0),(10,0,0),
                    {'flap': self.rect(0,11), 'base': other}, witnesses)

    def test_partial_overlay(self):
        p = self.patches(self.rect(2,7), [('flap','base',Fraction(1,5),Fraction(7,10))])
        self.assertEqual([c for c, _ in p], [{'flap'},{'flap','base'},{'flap'}])
        self.assertEqual(resolve_frontmost_layer('flap',p), 'flap')

    def test_hidden_or_unproved_midpath(self):
        for order, error in [([], 'ambiguous'),
                             ([('base','flap',Fraction(2,5),Fraction(3,5))], 'hidden')]:
            with self.subTest(order=order), self.assertRaisesRegex(ValueError,error):
                resolve_frontmost_layer('flap',self.patches(self.rect(4,6),order))

    def test_direction_switch_splits_even_with_same_polygon_coverage(self):
        p = self.patches(self.rect(-1,11), [('flap','base',0,Fraction(1,2)),
                                          ('base','flap',Fraction(1,2),1)])
        self.assertEqual(len(p), 2)
        with self.assertRaisesRegex(ValueError,'hidden'):
            resolve_frontmost_layer('flap',p)

    def test_boundary_coincidence_or_grazing_rejected(self):
        for poly in [self.rect(2,7,0,2), [(2,0,0),(3,2,0),(1,2,0)]]:
            with self.subTest(poly=poly), self.assertRaisesRegex(ValueError,'boundary'):
                self.patches(poly)

    def test_noncoplanar_and_invalid_polygon_rejected(self):
        with self.assertRaisesRegex(ValueError,'noncoplanar'):
            self.patches(self.rect(2,7,z=1))
        with self.assertRaisesRegex(ValueError,'convex'):
            self.patches([(2,-2,0),(7,2,0),(7,-2,0),(2,2,0)])

    def test_witness_outside_overlay_rejected(self):
        with self.assertRaisesRegex(ValueError,'co-coverage'):
            self.patches(self.rect(2,7),[('flap','base',0,1)])


class BoundedRemesh(unittest.TestCase):
    # A flap shares an uncut edge with attached sheet. The independent
    # lower layer has identical projected footprint but distinct IDs.
    points = {0:(0,0),1:(8,0),2:(0,8),3:(8,8),4:(0,0),5:(8,0),6:(0,8)}
    faces = [(0,1,2),(2,1,3),(4,5,6)]

    def test_exact_rational_partition_and_unchanged_remainder(self):
        mouth, tip = (Fraction(5,2),0), (Fraction(9,4),Fraction(5,4))
        out, xy, cut = remesh_single_triangle_slit(self.faces,self.points,0,(0,1),mouth,tip)
        self.assertEqual(out[4:],self.faces[1:])
        self.assertEqual({k:xy[k] for k in self.points},self.points)
        self.assertEqual([xy[k] for k in sorted(next(iter(cut)))],[mouth,tip])
        self.assertEqual(sum((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
                             for a,b,c in ([xy[v] for v in f] for f in out[:4])),64)
        self.assertEqual(len(self.faces),3)
        self.assertEqual(len(self.points),7)
        # Attached neighbors still weld; slit banks at mouth do not.
        weld = welded_corners(out,cut)
        self.assertEqual(weld[2,1],weld[4,1])
        self.assertNotEqual(weld[0,7],weld[1,7])
        self.assertEqual(len({weld[k,8] for k in range(4)}),1)
        self.assertEqual(out[5],(4,5,6))

    def test_clockwise_triangle_supported(self):
        out, _, _ = remesh_single_triangle_slit([(2,1,0)],self.points,0,(0,1),(3,0),(2,1))
        self.assertEqual(len(out),4)

    def test_attached_or_invalid_mouth_rejected(self):
        with self.assertRaisesRegex(ValueError,'free'):
            remesh_single_triangle_slit(self.faces,self.points,0,(1,2),(4,4),(2,2))
        for mouth in [(0,0),(-2,0),(3,1)]:
            with self.subTest(mouth=mouth), self.assertRaisesRegex(ValueError,'strictly'):
                remesh_single_triangle_slit(self.faces,self.points,0,(0,1),mouth,(2,2))

    def test_tip_boundary_or_overrun_rejected(self):
        for tip in [(2,0),(4,4),(6,6),(-1,1)]:
            with self.subTest(tip=tip), self.assertRaisesRegex(ValueError,'strictly'):
                remesh_single_triangle_slit(self.faces,self.points,0,(0,1),(3,0),tip)


if __name__ == '__main__':
    unittest.main()
