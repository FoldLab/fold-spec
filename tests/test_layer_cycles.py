import copy
import unittest
from foldspec import SpecError, validate_layer_cycles, validate_document, loads, ROOT


def relation(a, b, **changes):
    result = dict(firstFace=a, secondFace=b, at=1, normal=[0, 0, 1],
                  planeOffsetMm=0, overlapMm=[[0, 0], [1, 0], [0, 1]])
    result.update(changes)
    return result


class LayerCycleTests(unittest.TestCase):
    def test_acyclic_and_duplicate_relations(self):
        validate_layer_cycles([relation('a', 'b'), relation('b', 'c'), relation('a', 'b')])

    def test_two_face_contradiction(self):
        with self.assertRaisesRegex(SpecError, 'E_LAYER'):
            validate_layer_cycles([relation('a', 'b'), relation('b', 'a')])

    def test_transitive_cycle(self):
        with self.assertRaisesRegex(SpecError, 'E_LAYER'):
            validate_layer_cycles([relation('a', 'b'), relation('b', 'c'), relation('c', 'a')])

    def test_rotated_reversed_closed_polygon_is_same_patch(self):
        with self.assertRaisesRegex(SpecError, 'E_LAYER'):
            validate_layer_cycles([relation('a', 'b'), relation('b', 'a',
                overlapMm=[[1, 0], [0, 0], [0, 1], [1, 0]])])

    def test_different_patch_or_state_not_global_cycle(self):
        variants = [dict(at=0), dict(planeOffsetMm=1), dict(normal=[0, 1, 0]),
                    dict(overlapMm=[[2, 0], [3, 0], [2, 1]])]
        for change in variants:
            with self.subTest(change=change):
                validate_layer_cycles([relation('a', 'b'), relation('b', 'a', **change)])

    def test_no_mutation(self):
        layers = [relation('a', 'b')]; before = copy.deepcopy(layers)
        validate_layer_cycles(layers)
        self.assertEqual(layers, before)

    def test_long_acyclic_chain_without_recursion(self):
        validate_layer_cycles([relation(str(i), str(i + 1)) for i in range(1500)])

    def test_document_validation_invokes_cycle_check(self):
        d = loads((ROOT / 'examples/hinge/center-fold.fold.json').read_bytes())
        faces = d['geometry']['meshes'][0]['faces']
        a, b = faces[0]['id'], faces[1]['id']
        d['geometry']['operations'][0]['layers'] = [relation(a, b), relation(b, a)]
        with self.assertRaisesRegex(SpecError, 'E_LAYER'):
            validate_document(d)
