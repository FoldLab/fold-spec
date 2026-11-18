import copy,io,json,tempfile,unittest,zipfile
from pathlib import Path
from foldspec import ROOT,SpecError,loads,json_bytes,digest,pack_document,inspect_package,load_document,validate_document,derive_index,image_size,main

SOURCE=ROOT/'examples/catalog/first-fold-catalog.fold.json'

def document():return loads(SOURCE.read_bytes())

class CatalogDocumentTests(unittest.TestCase):
    def test_example_validates_and_projects_an_index(self):
        d=document();validate_document(d);index=derive_index(d)
        self.assertEqual(index['slug'],'first-fold-catalog')
        self.assertEqual(index['stepCount'],3)
        self.assertEqual(index['thumbnail']['path'],'assets/gallery.webp')
        self.assertEqual(index['thumbnail']['sha256'],d['assets'][0]['sha256'])
    def test_catalog_is_optional(self):
        d=loads((ROOT/'examples/minimal-text/first-fold.fold.json').read_bytes());validate_document(d)
        self.assertNotIn('slug',derive_index(d));self.assertNotIn('thumbnail',derive_index(d))
    def test_thumbnail_asset_without_catalog(self):
        d=document();del d['catalog']
        with self.assertRaisesRegex(SpecError,'E_CATALOG'):validate_document(d)
    def test_catalog_must_reference_a_thumbnail_role_asset(self):
        d=document();d['assets'][0]['role']='background'
        with self.assertRaisesRegex(SpecError,'E_REFERENCE'):validate_document(d)
    def test_unknown_asset(self):
        d=document();d['catalog']['thumbnails'][0]['asset']='missing'
        with self.assertRaisesRegex(SpecError,'E_REFERENCE'):validate_document(d)
    def test_undescribed_thumbnail_asset(self):
        d=document();d['catalog']['thumbnails']=[]
        with self.assertRaisesRegex(SpecError,'E_CATALOG'):validate_document(d)
    def test_alt_text_is_required_and_localized(self):
        d=document();del d['catalog']['thumbnails'][0]['alt']
        with self.assertRaisesRegex(SpecError,'E_SCHEMA'):validate_document(d)
        d=document();d['catalog']['thumbnails'][0]['alt']={'fr':'Un carré plié'}
        with self.assertRaisesRegex(SpecError,'E_LOCALE'):validate_document(d)
    def test_one_thumbnail_per_purpose(self):
        d=document();second=copy.deepcopy(d['assets'][0]);second.update(id='thumb-two',path='assets/two.webp');d['assets'].append(second)
        t=copy.deepcopy(d['catalog']['thumbnails'][0]);t['asset']='thumb-two';d['catalog']['thumbnails'].append(t)
        with self.assertRaisesRegex(SpecError,'E_CATALOG'):validate_document(d)
    def test_step_pose_needs_a_real_step(self):
        d=document();d['catalog']['thumbnails'][0]['pose']='step'
        with self.assertRaisesRegex(SpecError,'E_CATALOG'):validate_document(d)
        d['catalog']['thumbnails'][0]['step']='nope'
        with self.assertRaisesRegex(SpecError,'E_REFERENCE'):validate_document(d)
        d['catalog']['thumbnails'][0]['step']='fold-center';validate_document(d)
    def test_slug_and_timestamp_shapes(self):
        for key,value in (('slug','Not A Slug'),('slug','double--hyphen'),('addedAt','2026-11-17'),('addedAt','yesterday')):
            d=document();d['catalog'][key]=value
            with self.assertRaisesRegex(SpecError,'E_SCHEMA'):validate_document(d)
    def test_thumbnail_media_type_and_budget(self):
        d=document();d['assets'][0]['mediaType']='audio/mpeg'
        with self.assertRaisesRegex(SpecError,'E_ASSET_ROLE'):validate_document(d)
        d=document();d['assets'][0]['byteLength']=1024*1024+1
        with self.assertRaisesRegex(SpecError,'E_THUMBNAIL'):validate_document(d)
    def test_declared_dimensions_must_match_the_image(self):
        with tempfile.TemporaryDirectory() as t:
            directory=Path(t);(directory/'assets').mkdir();(directory/'assets/gallery.webp').write_bytes((SOURCE.parent/'assets/gallery.webp').read_bytes())
            d=document();d['catalog']['thumbnails'][0]['widthPx']=361;(directory/'doc.fold.json').write_bytes(json_bytes(d))
            with self.assertRaisesRegex(SpecError,'E_THUMBNAIL'):load_document(directory/'doc.fold.json')

class ImageHeaderTests(unittest.TestCase):
    def test_png(self):
        import struct,zlib
        ihdr=struct.pack('>IIBBBBB',7,5,8,2,0,0,0);png=b'\x89PNG\r\n\x1a\n'+struct.pack('>I',13)+b'IHDR'+ihdr+struct.pack('>I',zlib.crc32(b'IHDR'+ihdr))
        self.assertEqual(image_size(png,'image/png'),(7,5))
    def test_webp_lossy_example(self):
        self.assertEqual(image_size((SOURCE.parent/'assets/gallery.webp').read_bytes(),'image/webp'),(360,270))
    def test_webp_extended_header(self):
        data=b'RIFF'+bytes(4)+b'WEBPVP8X'+bytes(4)+bytes(4)+(99).to_bytes(3,'little')+(49).to_bytes(3,'little')+bytes(8)
        self.assertEqual(image_size(data,'image/webp'),(100,50))
    def test_jpeg_frame_header(self):
        data=b'\xff\xd8\xff\xc0\x00\x0b\x08\x00\x20\x00\x30\x01\x01\x11\x00\xff\xd9'
        self.assertEqual(image_size(data,'image/jpeg'),(48,32))
    def test_rejects_wrong_container(self):
        with self.assertRaisesRegex(SpecError,'E_IMAGE'):image_size(b'not an image at all, long enough to test',  'image/png')

class CatalogPackageTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.directory=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def package(self):
        target=self.directory/'catalog.foldlab';pack_document(SOURCE,target);return target
    def files(self,path):
        with zipfile.ZipFile(path) as z:return {i.filename:z.read(i) for i in z.infolist()}
    def write(self,path,files):
        with zipfile.ZipFile(path,'w') as z:
            for name,data in files.items():z.writestr(name,data)
    def test_package_carries_index_and_thumbnail(self):
        path=self.package();files=self.files(path)
        self.assertEqual(sorted(files),['assets/gallery.webp','document.json','manifest.json'])
        manifest=loads(files['manifest.json']);self.assertEqual(manifest['index'],derive_index(loads(files['document.json'])))
        d,report=inspect_package(path);self.assertEqual(d,document());self.assertEqual(report['package']['entries'],3)
    def test_single_file_is_enough_to_browse(self):
        files=self.files(self.package());manifest=loads(files['manifest.json'])['index'];thumb=manifest['thumbnail']
        self.assertEqual(digest(files[thumb['path']]),thumb['sha256'])
        self.assertEqual(manifest['title']['en'],'Your first fold')
    def test_index_is_optional_for_older_packages(self):
        path=self.package();files=self.files(path);manifest=loads(files['manifest.json']);del manifest['index'];files['manifest.json']=json_bytes(manifest);self.write(path,files)
        inspect_package(path)
    def test_stale_index_is_rejected_even_when_hashes_agree(self):
        path=self.package();files=self.files(path);manifest=loads(files['manifest.json']);manifest['index']['title']={'en':'A different title'};files['manifest.json']=json_bytes(manifest);self.write(path,files)
        with self.assertRaisesRegex(SpecError,'E_INDEX'):inspect_package(path)
    def test_index_cannot_smuggle_unknown_fields(self):
        path=self.package();files=self.files(path);manifest=loads(files['manifest.json']);manifest['index']['downloads']=9;files['manifest.json']=json_bytes(manifest);self.write(path,files)
        with self.assertRaisesRegex(SpecError,'E_SCHEMA'):inspect_package(path)
    def test_tampered_thumbnail(self):
        path=self.package();files=self.files(path);files['assets/gallery.webp']+=b'\0';self.write(path,files)
        with self.assertRaisesRegex(SpecError,'E_PACKAGE_HASH'):inspect_package(path)
    def test_unlisted_preview_is_rejected(self):
        path=self.package();files=self.files(path);files['assets/extra.webp']=files['assets/gallery.webp'];self.write(path,files)
        with self.assertRaisesRegex(SpecError,'E_MANIFEST'):inspect_package(path)
    def test_packing_is_reproducible(self):
        a=self.package();b=self.directory/'again.foldlab';pack_document(SOURCE,b);self.assertEqual(a.read_bytes(),b.read_bytes())

class IndexCommandTests(unittest.TestCase):
    def run_cli(self,*args):
        import contextlib
        out=io.StringIO();err=io.StringIO()
        with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):code=main(list(args))
        return code,out.getvalue(),err.getvalue()
    def test_index_command_lists_each_document_once(self):
        code,out,_=self.run_cli('index',str(SOURCE),str(ROOT/'examples/minimal-text/first-fold.fold.json'))
        self.assertEqual(code,0);result=json.loads(out);self.assertEqual([e['index']['id'] for e in result['entries']],['first-fold','first-fold-catalog'])
    def test_duplicate_documents_are_rejected(self):
        code,_,err=self.run_cli('index',str(SOURCE),str(SOURCE));self.assertEqual(code,1);self.assertIn('E_DUPLICATE_ID',err)

if __name__=='__main__':unittest.main()
