import unittest
from slit_topology import welded_corners

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

if __name__ == '__main__':
    unittest.main()
