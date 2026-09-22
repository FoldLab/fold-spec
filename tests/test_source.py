import json,unittest
from pathlib import Path
from foldspec import ROOT,SpecError,validate_document
from source_parser import parse_source

class SourceTests(unittest.TestCase):
    def setUp(self):self.path=ROOT/'examples/authoring/named-fold.foldsrc';self.source=self.path.read_text()
    def test_ast_matches_json(self):self.assertEqual(parse_source(self.source),json.loads(self.path.with_suffix('.json').read_text()) if self.path.with_suffix('.json').exists() else json.loads(self.path.with_name('named-fold.fold.json').read_text()))
    def test_crane_source_matches_ast(self):
        p=ROOT/'examples/crane/crane-authoring.foldsrc';self.assertEqual(parse_source(p.read_text()),json.loads(p.with_suffix('.fold.json').read_text()))
    def test_source_validates(self):validate_document(parse_source(self.source))
    def test_bad_version(self):
        with self.assertRaisesRegex(SpecError,'E_SOURCE'):parse_source(self.source.replace('fold-source "1.0.0-draft.1"','fold-source "8.0.0"'))
    def test_semicolon_required(self):
        with self.assertRaises(SpecError):parse_source(self.source.replace('"1.0.0-draft.1";','"1.0.0-draft.1"',1))
    def test_unknown_execution_rejected(self):
        with self.assertRaises(SpecError):parse_source(self.source+'\nexecute code {};')
    def test_no_keyword_prefix(self):
        with self.assertRaises(SpecError):parse_source(self.source.replace(' in work',' inwork'))
    def test_bad_units(self):
        with self.assertRaisesRegex(SpecError,'E_SOURCE_TYPE'):parse_source(self.source.replace('-75mm','-75deg',1))
    def test_duplicate_json_members_rejected(self):
        with self.assertRaisesRegex(SpecError,'E_DUPLICATE_KEY'):parse_source(self.source.replace('"revision": 1','"revision": 1, "revision": 2',1))
    def test_comments_outside_json(self):self.assertEqual(parse_source('// preface\n'+self.source+'\n// tail'),parse_source(self.source))
    def test_incomplete_declaration(self):
        with self.assertRaises(SpecError):parse_source(self.source+'\npoint')

    def test_deep_source_function_is_bounded(self):
        hostile=self.source+'\npoint deep in work = '+('midpoint('*1600)+'nw'+', ne)'*1600+';'
        with self.assertRaisesRegex(SpecError,'E_LIMIT'):parse_source(hostile)
