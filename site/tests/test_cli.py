"""Exercise the commands documented in the README as real subprocesses."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from foldspec import ROOT, loads


class CommandLineTests(unittest.TestCase):
    def run_cli(self, *args, ok=True):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'tools/foldspec.py'), *map(str, args)],
            cwd=ROOT, capture_output=True, text=True, timeout=45,
        )
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def test_validate_real_crane(self):
        result = json.loads(self.run_cli('validate', 'examples/crane/crane.fold.json').stdout)
        self.assertEqual(result['steps'], 44)
        self.assertEqual(result['geometry']['operations'], 40)

    def test_parse_source_to_new_file(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / 'nested/parsed.fold.json'
            self.run_cli('parse-source', 'examples/authoring/named-fold.foldsrc', '-o', out)
            self.assertEqual(loads(out.read_bytes()), loads((ROOT / 'examples/authoring/named-fold.fold.json').read_bytes()))
            self.run_cli('validate', out)

    def test_sample_real_operation_to_new_file(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / 'sample.json'
            self.run_cli('sample', 'examples/hinge/center-fold.fold.json', '--operation', 'fold-center', '--progress', '0.5', '-o', out)
            data = loads(out.read_bytes())
            self.assertEqual(data['operation'], 'fold-center')
            self.assertEqual(len(data['positionsMm']), len(data['mesh']['vertices']))

    def test_text_and_html_exports(self):
        with tempfile.TemporaryDirectory() as folder:
            for suffix in ('txt', 'html'):
                out = Path(folder) / ('crane.' + suffix)
                args = ['text', 'examples/crane/crane.fold.json', '--descriptive', '-o', out]
                if suffix == 'html':
                    args.append('--html')
                self.run_cli(*args)
                content = out.read_text()
                self.assertIn('Final presentation' if suffix == 'html' else 'FINAL PRESENTATION', content)
                self.assertIn('Hiroshima', content)

    def test_real_package_round_trip_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / 'staged.foldlab'
            self.run_cli('pack', 'examples/scene/staged-fold.fold.json', '-o', out)
            result = json.loads(self.run_cli('inspect', out).stdout)
            self.assertEqual(result['status'], 'resolved')
            failed = self.run_cli('pack', 'examples/scene/staged-fold.fold.json', '-o', out, ok=False)
            self.assertIn('error', json.loads(failed.stderr))

    def test_schema_only_is_labelled(self):
        result = json.loads(self.run_cli('validate', 'examples/hinge/center-fold.fold.json', '--schema-only').stdout)
        self.assertIn('schema-only', result['checks'])

    def test_invalid_command_produces_json_error(self):
        result = self.run_cli('sample', 'examples/hinge/center-fold.fold.json', '--operation', 'absent', '--progress', '0.5', ok=False)
        self.assertEqual(json.loads(result.stderr)['error'], 'E_REFERENCE')
