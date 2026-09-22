#!/usr/bin/env python3
"""Build a static, offline, script-free documentation site. Does not render 3D models."""
from __future__ import annotations
import argparse,html,json,re,shutil
from pathlib import Path
from urllib.parse import urlsplit
import mistune
ROOT=Path(__file__).resolve().parents[1]
CSS='''
:root{color-scheme:light;--ink:#233241;--muted:#5f6c76;--paper:#faf9f6;--line:#dedfdc;--accent:#ac392f;--code:#f0f2f4}*{box-sizing:border-box}html{scroll-behavior:auto}body{margin:0;color:var(--ink);background:var(--paper);font:16px/1.7 system-ui,-apple-system,sans-serif}a{color:#205992;text-underline-offset:3px}a:hover{color:var(--accent)}:focus-visible{outline:3px solid #bf4734;outline-offset:4px}.skip{position:absolute;left:10px;top:-100px}.skip:focus{top:8px;background:white;padding:8px;z-index:4}header{display:flex;align-items:center;justify-content:space-between;gap:20px;border-bottom:1px solid var(--line);padding:19px 5vw;background:#fff}header a{font-weight:720;color:var(--ink);text-decoration:none;font-size:22px}header small{color:var(--muted);font-size:13px}.layout{display:grid;grid-template-columns:265px minmax(0,980px);gap:38px;max-width:1360px;padding:28px;margin:auto}aside{font-size:13px;line-height:1.5}aside nav{position:sticky;top:24px;max-height:90vh;overflow:auto;padding:8px 10px 20px 0}aside a{display:block;text-decoration:none;color:#516171;padding:7px 12px;border-radius:6px}aside a:hover{background:#f1e9e1}aside strong{display:block;padding:14px 12px 4px;text-transform:uppercase;font-size:10px;letter-spacing:.1em;color:#8a6660}main{min-width:0;padding:8px 0 60px}h1{font-size:36px;line-height:1.18;letter-spacing:-1.3px;font-weight:690;border-bottom:2px solid var(--accent);padding-bottom:22px}h2{font-size:24px;line-height:1.35;margin-top:2.2em;letter-spacing:-.5px}h3{font-size:18px;margin-top:1.8em}p{max-width:84ch}pre{overflow:auto;border:1px solid #d8dde1;padding:18px 20px;background:var(--code);border-radius:9px;line-height:1.55;font-size:13px}code{font: .9em/1.5 ui-monospace,SFMono-Regular,Consolas,monospace;background:var(--code);border-radius:3px;padding:1px 4px}pre code{padding:0}blockquote{border-left:4px solid #b89b6e;margin:24px 0;padding:6px 20px;background:#f3eee5}table{display:block;overflow:auto;border-collapse:collapse;width:100%;font-size:14px;line-height:1.6;margin:24px 0}td,th{border:1px solid #dfe1df;padding:11px 13px;text-align:left;vertical-align:top;min-width:100px}th{background:#edf0ee;color:#293d4b}ul,ol{padding-left:24px}li{margin:.3em 0}.edition{padding:14px 0;color:var(--muted);font-size:12px}.doc-footer{border-top:1px solid var(--line);margin-top:44px;padding-top:16px;color:var(--muted);font-size:13px}img{max-width:100%;height:auto}@media(max-width:850px){.layout{grid-template-columns:1fr;padding:18px;gap:20px}aside nav{position:static;max-height:180px;border:1px solid var(--line);border-radius:8px;padding:8px}h1{font-size:28px}header{padding:16px 20px}header small{max-width:150px;text-align:right}td,th{font-size:13px;padding:8px}main{padding-top:0}}@media print{header,aside,.skip,.doc-footer{display:none}.layout{display:block;padding:0}body{color:black;background:white;font-size:11pt}pre,table{overflow:visible;white-space:pre-wrap}h1,h2,h3{break-after:avoid}a{color:inherit}}
'''
def slug(text):
    plain=re.sub('<[^>]+>','',html.unescape(text));return re.sub(r'[^\w\s-]','',plain).strip().lower().replace(' ','-')
class Renderer(mistune.HTMLRenderer):
    def __init__(self):super().__init__(escape=True);self.slugs={}
    def heading(self,text,level,**attrs):
        anchor=slug(text);n=self.slugs.get(anchor,0);self.slugs[anchor]=n+1
        if n:anchor+=f'-{n}'
        return f'<h{level} id="{html.escape(anchor)}">{text}</h{level}>\n'
    def link(self,text,url,title=None):
        u=urlsplit(url)
        if not u.scheme and not u.netloc and u.path.endswith('.md'):
            url=u.path[:-3]+'.html'+(('?'+u.query)if u.query else'')+(('#'+u.fragment)if u.fragment else'')
        return super().link(text,url,title)

def build(destination:Path):
    destination=destination.resolve();destination.mkdir(parents=True,exist_ok=True)
    (destination/'assets').mkdir(exist_ok=True);(destination/'assets/site.css').write_text(CSS)
    excluded={'.venv','__pycache__','.git','site','build'}
    docs=[p for p in ROOT.rglob('*.md') if not any(x in excluded for x in p.relative_to(ROOT).parts)]
    chapters=sorted((ROOT/'spec').glob('*.md'))
    for p in docs:
        rel=p.relative_to(ROOT);target=destination/rel.with_suffix('.html');target.parent.mkdir(parents=True,exist_ok=True);prefix='../'*len(rel.parent.parts)
        renderer=Renderer();md=mistune.create_markdown(renderer=renderer,plugins=['table','url']);text=p.read_text();title=text.splitlines()[0].lstrip('# ').strip();content=md(text)
        nav=f'<strong>Overview</strong><a href="{prefix}README.html">Read me</a><a href="{prefix}SPEC.html">Specification index</a><a href="{prefix}docs/quickstart.html">Quick start</a><a href="{prefix}examples/crane/README.html">Crane example</a><a href="{prefix}IMPLEMENTATION-STATUS.html">Implementation coverage</a><strong>Normative chapters</strong>'
        for chapter in chapters:nav+=f'<a href="{prefix}spec/{chapter.stem}.html">{html.escape(chapter.read_text().splitlines()[0][2:])}</a>'
        nav+=f'<strong>Reference</strong><a href="{prefix}docs/field-reference.html">Field reference</a><a href="{prefix}docs/glossary.html">Glossary</a><a href="{prefix}VERIFICATION.html">Verification</a>'
        page=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · fold-spec</title><link rel="stylesheet" href="{prefix}assets/site.css"></head><body><a class="skip" href="#main">Skip to content</a><header><a href="{prefix}README.html">fold-spec</a><small>1.0.0-draft.1<br>Implementer draft</small></header><div class="layout"><aside><nav aria-label="Documentation">{nav}</nav></aside><main id="main">{content}<footer class="doc-footer">Fold Spec · Normative requirements are identified in their chapters. Read implementation coverage before making conformance claims.</footer></main></div></body></html>'
        target.write_text(page,encoding='utf-8')
    # Linked data, code and grammar are copied as data. No external resources or fonts.
    for dirname in ('schemas','examples','grammar','tools','tests','conformance','docs'):
        for p in (ROOT/dirname).rglob('*'):
            if not p.is_file() or p.suffix in ('.md','.pyc') or '__pycache__'in p.parts:continue
            target=destination/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
            # Do not overwrite semantic HTML generated from Markdown.
            if p.suffix=='.html'and target.exists():continue
            shutil.copyfile(p,target)
    for name in ('requirements.txt','LICENSE','VERSION'):shutil.copyfile(ROOT/name,destination/name)
    shutil.copyfile(destination/'README.html',destination/'index.html')
    return {'pages':len(docs)+1,'destination':str(destination),'externalResources':0}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'build/site');args=p.parse_args();print(json.dumps(build(args.output),indent=2))
