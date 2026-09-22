import copy,json,stat,tempfile,unittest,warnings,zipfile
from pathlib import Path
from foldspec import ROOT,SpecError,loads,json_bytes,digest,pack_document,inspect_package,check_asset_bytes,asset_data

class PackageTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.directory=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def package(self,relative='examples/hinge/center-fold.fold.json'):
        target=self.directory/'demo.foldlab';pack_document(ROOT/relative,target);return target
    def rewrite(self,path,mutate):
        with zipfile.ZipFile(path) as z:files={i.filename:z.read(i) for i in z.infolist()}
        mutate(files)
        with zipfile.ZipFile(path,'w') as z:
            for p,b in files.items():z.writestr(p,b)
    def test_round_trip(self):
        path=self.package();d,r=inspect_package(path);self.assertEqual(d,loads((ROOT/'examples/hinge/center-fold.fold.json').read_bytes()));self.assertEqual(r['package']['entries'],2)
    def test_reproducible_package_bytes(self):
        a=self.package();b=self.directory/'second.foldlab';pack_document(ROOT/'examples/hinge/center-fold.fold.json',b);self.assertEqual(a.read_bytes(),b.read_bytes())
    def test_no_overwrite(self):
        path=self.package();before=path.read_bytes()
        with self.assertRaisesRegex(SpecError,'E_EXISTS'):pack_document(ROOT/'examples/hinge/center-fold.fold.json',path)
        self.assertEqual(path.read_bytes(),before)
    def test_payload_tamper(self):
        p=self.package();self.rewrite(p,lambda f:f.update({'document.json':f['document.json']+b' '}))
        with self.assertRaisesRegex(SpecError,'E_PACKAGE_HASH'):inspect_package(p)
    def test_unlisted_file(self):
        p=self.package();self.rewrite(p,lambda f:f.update({'extra.json':b'{}'}))
        with self.assertRaisesRegex(SpecError,'E_MANIFEST'):inspect_package(p)
    def test_zip_traversal(self):
        p=self.package();self.rewrite(p,lambda f:f.update({'../evil.json':b'{}'}))
        with self.assertRaisesRegex(SpecError,'E_PATH'):inspect_package(p)
    def test_case_collision(self):
        p=self.package();self.rewrite(p,lambda f:f.update({'DOCUMENT.json':b'{}'}))
        with self.assertRaisesRegex(SpecError,'E_PATH'):inspect_package(p)
    def test_duplicate_entry(self):
        p=self.package()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            with zipfile.ZipFile(p,'a') as z:z.writestr('document.json',b'{}')
        with self.assertRaisesRegex(SpecError,'E_PATH'):inspect_package(p)
    def test_symlink_rejected(self):
        p=self.package()
        with zipfile.ZipFile(p,'a') as z:
            i=zipfile.ZipInfo('assets/link');i.create_system=3;i.external_attr=(stat.S_IFLNK|0o777)<<16;z.writestr(i,b'/etc/passwd')
        with self.assertRaisesRegex(SpecError,'E_PATH'):inspect_package(p)
    def test_executable_permissions_rejected(self):
        p=self.package()
        with zipfile.ZipFile(p,'a') as z:
            i=zipfile.ZipInfo('assets/run');i.create_system=3;i.external_attr=(stat.S_IFREG|0o755)<<16;z.writestr(i,b'not executed')
        with self.assertRaisesRegex(SpecError,'E_PATH'):inspect_package(p)
    def test_unsupported_zip_codec(self):
        p=self.package()
        with zipfile.ZipFile(p,'a') as z:z.writestr('extra.json',b'{}',compress_type=zipfile.ZIP_BZIP2)
        with self.assertRaisesRegex(SpecError,'E_ZIP'):inspect_package(p)
    def test_static_asset_embedded(self):
        p=self.package('examples/scene/staged-fold.fold.json');d,r=inspect_package(p);self.assertEqual(r['package']['entries'],3)
        with zipfile.ZipFile(p) as z:self.assertEqual(z.read('assets/grid.png'),(ROOT/'examples/scene/assets/grid.png').read_bytes())
    def test_asset_hash_mismatch(self):
        d=loads((ROOT/'examples/scene/staged-fold.fold.json').read_bytes());a=d['assets'][0];raw=(ROOT/'examples/scene/assets/grid.png').read_bytes();a['sha256']='0'*64
        with self.assertRaisesRegex(SpecError,'E_ASSET_HASH'):check_asset_bytes(raw,a)
    def test_png_structure_after_correct_hash(self):
        d=loads((ROOT/'examples/scene/staged-fold.fold.json').read_bytes());a=d['assets'][0];raw=b'not a png';a.update(sha256=digest(raw),byteLength=len(raw))
        with self.assertRaisesRegex(SpecError,'E_IMAGE'):check_asset_bytes(raw,a)
    def test_symlink_source_asset_rejected(self):
        d=loads((ROOT/'examples/scene/staged-fold.fold.json').read_bytes());a=d['assets'][0];(self.directory/'assets').mkdir();(self.directory/a['path']).symlink_to(ROOT/'examples/scene/assets/grid.png')
        with self.assertRaisesRegex(SpecError,'E_PATH'):asset_data(self.directory,a)
    def test_not_zip(self):
        p=self.directory/'bad.foldlab';p.write_bytes(b'not a zip')
        with self.assertRaisesRegex(SpecError,'E_ZIP'):inspect_package(p)
