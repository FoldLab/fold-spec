import unittest
from foldspec import ROOT,loads,validate_document,SpecError
class FixtureTests(unittest.TestCase):
    def test_language_neutral_cases(self):
        manifest=loads((ROOT/'conformance/cases.json').read_bytes())
        for case in manifest['cases']:
            with self.subTest(case=case['id']):
                data=(ROOT/'conformance'/case['file']).read_bytes()
                if case['valid']:validate_document(loads(data))
                else:
                    with self.assertRaises(SpecError) as caught:validate_document(loads(data))
                    self.assertEqual(caught.exception.code,case['error'])
