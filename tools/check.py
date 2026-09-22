#!/usr/bin/env python3
"""Run repository checks without downloading schemas or touching example source files."""
from __future__ import annotations
import argparse,hashlib,io,json,re,subprocess,sys,tempfile,time,unittest
from pathlib import Path
from urllib.parse import unquote,urlsplit
from jsonschema import Draft202012Validator
from foldspec import ROOT,SCHEMAS,SpecError,loads,load_document,schema_validate,asset_data,indexed,require,validate_camera
from source_parser import parse_source
from field_reference import render as field_reference

def markdown_files():
    return sorted(p for p in ROOT.rglob('*.md') if not any(x in p.relative_to(ROOT).parts for x in ('site','build','.venv','__pycache__')))

def check_links():
    problems=[];count=0
    for p in markdown_files():
        text=re.sub(r'```.*?```','',p.read_text(encoding='utf-8'),flags=re.S)
        links=re.findall(r'\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)',text)
        links+=re.findall(r'^\[[^\]]+\]:\s*(\S+)',text,flags=re.M)
        for link in links:
            u=urlsplit(link.strip('<>'))
            if u.scheme or u.netloc:continue
            target=(p.parent/unquote(u.path)).resolve() if u.path else p
            if not target.exists():problems.append(f'{p.relative_to(ROOT)} -> {link}')
            count+=1
    require(not problems,'E_DOC_LINK','Missing local targets: '+'; '.join(problems))
    return count

def check_special_examples():
    counts={'scenes':0,'libraries':0}
    for p in sorted((ROOT/'examples').rglob('*.foldscene')):
        d=loads(p.read_bytes());schema_validate(d,'scene.schema.json');assets=indexed(d['assets'],'asset');keys=d['stage']['keys']
        require(keys[0]['at']==0 and keys[-1]['at']==1 and all(a['at']<b['at'] for a,b in zip(keys,keys[1:])),'E_TIME','Invalid standalone scene path.')
        validate_camera(d['stage']['camera'])
        if 'backgroundAsset'in d['stage']:require(d['stage']['backgroundAsset']in assets and assets[d['stage']['backgroundAsset']]['role']=='background','E_REFERENCE','Scene background missing.')
        for a in assets.values():asset_data(p.parent,a)
        counts['scenes']+=1
    for p in sorted((ROOT/'examples').rglob('*.foldlib.json')):
        d=loads(p.read_bytes());schema_validate(d,'library.schema.json');indexed(d['parts'],'library part')
        for part in d['parts']:
            a=part['authoring'];names={x['id'] for key in ('points','lines','regions','intents') for x in a[key]}
            require(set(part['exports'])<=names,'E_REFERENCE','Library export not defined.')
            params=indexed(part['parameters'],'parameter');pointers=set()
            for v in params.values():require(v['minimum']<=v['default']<=v['maximum'],'E_LIBRARY','Parameter default outside bounds.')
            for bind in part['bindings']:
                require(bind['parameter']in params and bind['pointer']not in pointers,'E_LIBRARY','Invalid or conflicting parameter binding.');pointers.add(bind['pointer']);obj=a
                try:
                    for key in bind['pointer'].split('/')[1:]:obj=obj[int(key)] if isinstance(obj,list) else obj[key]
                except (ValueError,IndexError,KeyError,TypeError) as exc:raise SpecError('E_LIBRARY','Pointer target missing.') from exc
                require(type(obj)in (int,float),'E_LIBRARY','Parameter pointer must target a numeric leaf.')
        counts['libraries']+=1
    return counts

def run():
    start=time.monotonic();versions=[]
    for p in sorted(SCHEMAS.glob('*.json')):
        schema=loads(p.read_bytes());Draft202012Validator.check_schema(schema);versions.append(p.name)
    with tempfile.TemporaryDirectory() as temp:
        subprocess.run([sys.executable,str(ROOT/'tools/schema_source.py'),'--output-root',temp],check=True)
        for name in versions:
            require((Path(temp)/'schemas'/SCHEMAS.name/name).read_bytes()==(SCHEMAS/name).read_bytes(),'E_GENERATED','Generated schema is stale: '+name)
    require((ROOT/'docs/field-reference.md').read_text()==field_reference(),'E_GENERATED','Regenerate docs/field-reference.md.')
    documents=[];packages=0;source_pairs=0
    for p in sorted((ROOT/'examples').rglob('*.fold.json')):
        d,r=load_document(p);documents.append({'file':str(p.relative_to(ROOT)),**r})
    for p in sorted((ROOT/'examples').rglob('*.foldlab')):
        d,r=load_document(p);readable=p.with_suffix('.fold.json')
        require(readable.exists() and d==loads(readable.read_bytes()),'E_PACKAGE_SOURCE','Archive differs from readable source: '+str(p));packages+=1
    for p in sorted((ROOT/'examples').rglob('*.foldsrc')):
        require(parse_source(p.read_text())==loads(p.with_suffix('.fold.json').read_bytes()),'E_SOURCE_AST','Source and JSON examples disagree.');source_pairs+=1
    special=check_special_examples();links=check_links()
    require(not list((ROOT/'examples').rglob('*.woff*')) and not list((ROOT/'examples').rglob('*.ttf')),'E_CONTENT','Font binaries do not belong in this distribution.')
    buffer=io.StringIO();suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'));result=unittest.TextTestRunner(stream=buffer,verbosity=1).run(suite)
    if not result.wasSuccessful():print(buffer.getvalue(),file=sys.stderr)
    require(result.wasSuccessful(),'E_TEST','Unit test suite failed.')
    return {'status':'passed','specVersion':SCHEMAS.name,'python':sys.version.split()[0],'schemas':len(versions),'documentExamples':len(documents),'packageExamples':packages,'sourcePairs':source_pairs,**special,'localLinksChecked':links,'unitTests':result.testsRun,'testFailures':len(result.failures),'testErrors':len(result.errors),'seconds':round(time.monotonic()-start,3),'documents':documents,
            'notClaimed':['full symbolic compiler','full library expander','complete local overlap-order validator','real-time renderer','PDF generation','physical folding certification','assistive technology user testing']}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path);args=p.parse_args()
    try:
        result=run()
        if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k!='documents'},ensure_ascii=False,indent=2))
    except (SpecError,OSError,subprocess.CalledProcessError) as exc:
        print(str(exc),file=sys.stderr);sys.exit(1)
