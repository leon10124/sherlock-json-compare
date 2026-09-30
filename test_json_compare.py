import unittest
import os
import sys
if os.environ.get('SHERLOCK_JSON_ROOT'):sys.path.insert(0,os.environ['SHERLOCK_JSON_ROOT'])
from json_compare import compare

class JSONTests(unittest.TestCase):
    def test_keys(self):self.assertTrue(compare('{"b":2,"a":1}','{"a":1,"b":2}')['equal'])
    def test_types(self):self.assertFalse(compare('true','1')['equal'])
    def test_nested(self):self.assertEqual(compare('{"a":{"b":1}}','{"a":{"b":2}}')['changes'][0]['path'],'/a/b')
    def test_pointer_escape(self):self.assertTrue(compare('{"a/b":1}','{"a/b":2}',['/a~1b'])['equal'])
    def test_exclude(self):self.assertTrue(compare('{"time":1,"x":2}','{"time":3,"x":2}',['/time'])['equal'])
    def test_array_order(self):self.assertFalse(compare('[1,2]','[2,1]')['equal']);self.assertTrue(compare('[1,2]','[2,1]',unordered=True)['equal'])
    def test_duplicates(self):self.assertFalse(compare('[1,1,2]','[1,2,2]',unordered=True)['equal'])
    def test_object_array(self):self.assertTrue(compare('[{"a":1},{"a":2}]','[{"a":2},{"a":1}]',unordered=True)['equal'])
    def test_added_removed(self):self.assertEqual(compare('{"x":null}','{"y":null}')['change_count'],2)
    def test_bad_inputs(self):
        for value in ('{"x":1,"x":2}','NaN','1e999','{','['*70+'0'+']'*70):
            with self.assertRaises(ValueError):compare(value,'null')
    def test_size_limit(self):
        with self.assertRaises(ValueError):compare('"'+'a'*262144+'"','null')
    def test_report_limit(self):self.assertTrue(compare('{}',__import__('json').dumps({str(n):n for n in range(250)}))['truncated'])
    def test_portable_server_from_package_or_sources(self):
        import json
        import shutil
        import subprocess
        import tempfile
        import urllib.request
        import urllib.error
        import zipfile
        from pathlib import Path
        source=Path(os.environ.get('SHERLOCK_JSON_ROOT',Path(__file__).resolve().parent))
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            archive=source/'json-compare-portable.zip'
            if archive.exists():
                with zipfile.ZipFile(archive) as package:package.extractall(root)
                root=root/'json-compare'
                self.assertTrue((root/'Start.cmd').is_file())
            else:
                for name in ('json_compare.py','portable_json.py','json-product.js','style.css'):shutil.copy2(source/name,root/name)
                shutil.copy2(source/'index.html',root/'index.html')
            process=subprocess.Popen([sys.executable,str(root/'portable_json.py'),'--no-browser'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            try:
                url=process.stdout.readline().strip()
                self.assertTrue(url.startswith('http://127.0.0.1:'))
                with urllib.request.urlopen(url,timeout=5) as response:self.assertIn(b'JSON Structure Compare',response.read())
                payload={'left':'{"名字":1}','right':'{"名字":2}'}
                req=urllib.request.Request(url+'venture/json-compare/api/compare',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req,timeout=5) as response:result=json.loads(response.read())
                self.assertEqual(result['change_count'],1);self.assertEqual(result['changes'][0]['path'],'/名字')
                req=urllib.request.Request(url,headers={'Origin':'https://example.org'})
                with self.assertRaises(urllib.error.HTTPError) as denied:urllib.request.urlopen(req,timeout=5)
                self.assertEqual(denied.exception.code,403)
            finally:process.terminate();process.communicate(timeout=5)

if __name__=='__main__':unittest.main(verbosity=2)
