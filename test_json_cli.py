import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

class CLITests(unittest.TestCase):
    def run_case(self,left,right,*options):
        with tempfile.TemporaryDirectory() as folder:
            a=Path(folder)/'a.json';b=Path(folder)/'b.json'
            a.write_text(left,encoding='utf-8');b.write_text(right,encoding='utf-8')
            return subprocess.run([sys.executable,str(Path(__file__).with_name('json_cli.py')),str(a),str(b),*options],capture_output=True,text=True,timeout=5)
    def test_ignore_unordered_and_unicode(self):
        r=self.run_case('{"時間":1,"ids":[1,2]}','{"時間":2,"ids":[2,1]}','--ignore','/時間','--unordered')
        self.assertEqual(r.returncode,0);self.assertTrue(json.loads(r.stdout)['equal'])
    def test_duplicate_counts_and_no_value_output(self):
        r=self.run_case('["private-value","private-value",2]','["private-value",2,2]','--unordered')
        self.assertEqual(r.returncode,1);self.assertNotIn('private-value',r.stdout+r.stderr)
    def test_invalid_json(self):
        r=self.run_case('{broken','{}');self.assertEqual(r.returncode,2)
        self.assertIn('error',json.loads(r.stdout))
    def test_strict_types(self):
        self.assertEqual(self.run_case('{"a":true}','{"a":1}').returncode,1)
    def test_oversized_input(self):
        self.assertEqual(self.run_case(' '*262145,'{}').returncode,2)

if __name__=='__main__':unittest.main(verbosity=2)
