#!/usr/bin/env python3
"""Fold Spec reference utilities. Not a cloth solver or a physical-foldability certifier.

Python 3.10+. `python tools/foldspec.py --help` lists public commands.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile
from urllib.parse import urlsplit
from collections import Counter, defaultdict
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.0.0-draft.1'
SCHEMAS = ROOT / 'schemas' / VERSION
MAX_ENTRY = 32 * 1024 * 1024
MAX_TOTAL = 128 * 1024 * 1024
MAX_ARCHIVE = 64 * 1024 * 1024
MAX_ENTRIES = 258
MAX_DEPTH = 96

class SpecError(ValueError):
    def __init__(self, code: str, message: str, path: str = ''):
        self.code, self.message, self.path = code, message, path
        super().__init__(f'{code} {path}: {message}')

def require(ok: bool, code: str, message: str, path: str = '') -> None:
    if not ok:
        raise SpecError(code, message, path)

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def json_bytes(value: Any) -> bytes:
    """Readable deterministic writer, NOT RFC 8785 canonical JSON."""
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')

def _pairs(items: list[tuple[str, Any]]) -> dict:
    out = {}
    for key, value in items:
        require(key not in out, 'E_DUPLICATE_KEY', f'Duplicate member {key!r}.')
        out[key] = value
    return out

def _reject_constant(value: str) -> None:
    raise SpecError('E_NUMBER', f'Non-JSON numeric constant {value}.')

def check_tree(value: Any, depth: int = 0) -> None:
    require(depth <= MAX_DEPTH, 'E_LIMIT', 'JSON nesting exceeds reference resource policy.')
    if isinstance(value, float):
        require(math.isfinite(value), 'E_NUMBER', 'Nonfinite or overflowed number.')
    elif isinstance(value, str):
        require(not any(0xD800 <= ord(c) <= 0xDFFF for c in value), 'E_UNICODE', 'Unpaired UTF-16 surrogate.')
        require('\0' not in value, 'E_UNICODE', 'NUL is not permitted in text.')
    elif isinstance(value, dict):
        for k, v in value.items():
            check_tree(k, depth + 1); check_tree(v, depth + 1)
    elif isinstance(value, list):
        for item in value: check_tree(item, depth + 1)

def loads(data: bytes | str) -> Any:
    if isinstance(data, bytes):
        require(len(data) <= MAX_ENTRY, 'E_LIMIT', 'JSON entry exceeds 32 MiB.')
        try: data = data.decode('utf-8', errors='strict')
        except UnicodeDecodeError as exc: raise SpecError('E_ENCODING', 'Input is not UTF-8.') from exc
    require(not data.startswith('\ufeff'), 'E_ENCODING', 'UTF-8 BOM is not permitted.')
    require(len(data.encode('utf-8')) <= MAX_ENTRY, 'E_LIMIT', 'JSON entry exceeds 32 MiB.')
    try: value = json.loads(data, object_pairs_hook=_pairs, parse_constant=_reject_constant)
    except (json.JSONDecodeError, RecursionError) as exc: raise SpecError('E_JSON', str(exc)) from exc
    check_tree(value)
    return value

def schema_validate(value: dict, filename: str = 'document.schema.json') -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise SpecError('E_DEPENDENCY', 'Install requirements.txt; jsonschema is required.') from exc
    schema = loads((SCHEMAS / filename).read_bytes())
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: str(list(e.absolute_path)))
    if errors:
        e = errors[0]
        raise SpecError('E_SCHEMA', e.message, '/' + '/'.join(str(x) for x in e.absolute_path))

def indexed(items: list[dict], kind: str) -> dict[str, dict]:
    out = {}
    for item in items:
        require(item['id'] not in out, 'E_DUPLICATE_ID', f'Duplicate {kind} ID {item["id"]}.')
        out[item['id']] = item
    return out

def safe_path(name: str) -> str:
    require(bool(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_./-]{0,239}', name)), 'E_PATH', f'Unsafe package path {name!r}.')
    segments = name.split('/')
    require(all(s not in ('', '.', '..') and not s.endswith(('.', ' ')) for s in segments), 'E_PATH', 'Empty, traversal, or ambiguous path segment.')
    devices = {'con','prn','aux','nul'} | {f'{p}{i}' for p in ('com','lpt') for i in range(1,10)}
    require(all(s.split('.')[0].lower() not in devices for s in segments), 'E_PATH', 'Reserved platform device name.')
    return name

def safe_https(url: str) -> None:
    try:
        u = urlsplit(url)
        port = u.port
    except ValueError as exc:
        raise SpecError('E_URL', 'Malformed HTTPS reference.') from exc
    require(u.scheme == 'https' and bool(u.hostname) and not u.username and not u.password,
            'E_URL', 'HTTPS references require a host and prohibit credentials.')
    require(not any(ord(c) < 33 or c == '\\' for c in url), 'E_URL', 'URL contains whitespace, control, or backslash.')

def norm(v: list | tuple) -> float: return math.sqrt(sum(x*x for x in v))
def sub(a, b): return [x-y for x,y in zip(a,b)]
def add(a, b): return [x+y for x,y in zip(a,b)]
def scale(a, s): return [x*s for x in a]
def dot(a, b): return sum(x*y for x,y in zip(a,b))
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def unit(v):
    n = norm(v); require(n > 1e-12, 'E_AXIS', 'Zero-length direction.'); return scale(v, 1/n)
def rotate(p, a, b, angle):
    k = unit(sub(b,a)); q = sub(p,a); c,s = math.cos(angle),math.sin(angle)
    return add(a, add(add(scale(q,c),scale(cross(k,q),s)),scale(k,dot(k,q)*(1-c))))
def triangle_area2(a,b,c):return ((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/2

def validate_camera(c: dict) -> None:
    view=sub(c['targetMm'],c['positionMm'])
    require(norm(view)>1e-8 and norm(cross(view,c['up']))>1e-8, 'E_CAMERA', 'Camera view and up must define an orientation.')
    require(abs(norm(c['up'])-1)<1e-6,'E_CAMERA','Camera up must be unit length.')
    field='verticalSpanMm' if c['projection']=='orthographic' else 'verticalFovDeg'
    require(field in c,'E_CAMERA',f'{field} is required for this projection.')
    other='verticalFovDeg' if field=='verticalSpanMm' else 'verticalSpanMm'
    require(other not in c,'E_CAMERA',f'{other} is not used by this projection.')

def validate_locales(d: dict) -> None:
    locale=d['defaultLocale']
    singular={'title','summary','body','name','description','orientation','rightsNote'}
    plural={'setup','locate','check','recovery','limitations','checks','qualifications'}
    def text(value):
        require(len({k.lower() for k in value})==len(value),'E_LOCALE','Case-colliding locale tags.')
        require(isinstance(value,dict) and isinstance(value.get(locale),str),'E_LOCALE',f'Localized text lacks default locale {locale}.')
    def visit(x):
        if isinstance(x,dict):
            for k,v in x.items():
                if k=='extensions':continue
                if k in singular and isinstance(v,dict):text(v)
                elif k in plural and isinstance(v,list):
                    for item in v:
                        if isinstance(item,dict):text(item)
                if k=='camera' and isinstance(v,dict):validate_camera(v)
                if k=='review' and isinstance(v,dict) and v.get('status')=='tested':
                    require(bool(v.get('evidence')) and all(s.strip() for s in v['evidence']),'E_REVIEW','Tested review requires nonblank evidence.')
                visit(v)
        elif isinstance(x,list):
            for v in x:visit(v)
    visit(d)

def mesh_edges(mesh):
    return sorted({tuple(sorted((v[i],v[(i+1)%3]))) for f in mesh['faces'] for v in [f['vertices']] for i in range(3)})

def validate_mesh(mesh: dict, sheet: dict, tolerance: float) -> None:
    vs=mesh['vertices'];fs=mesh['faces'];indexed(vs,'vertex');indexed(fs,'face')
    uv=[v['uvMm'] for v in vs]; w,h=sheet['widthMm'],sheet['heightMm']
    for p in uv:require(abs(p[0])<=w/2+tolerance and abs(p[1])<=h/2+tolerance,'E_MATERIAL','Vertex outside original rectangle.')
    # Distinct source material identities may not occupy the same position in this core disk.
    seen=set()
    for p in uv:
        key=tuple(round(x,9) for x in p)
        require(key not in seen,'E_TOPOLOGY','Duplicate material-coordinate vertex.');seen.add(key)
    edge_use=defaultdict(list);area=0.; used=set(); adj=defaultdict(set)
    for fi,f in enumerate(fs):
        v=f['vertices'];require(max(v)<len(vs),'E_REFERENCE','Face vertex index is out of range.')
        a=triangle_area2(*(uv[i] for i in v));require(a>1e-12,'E_TOPOLOGY','Material faces must be nondegenerate and counterclockwise.')
        area+=a;used.update(v)
        for i in range(3):
            a,b=v[i],v[(i+1)%3];edge_use[tuple(sorted((a,b)))].append((a,b,fi));adj[a].add(b);adj[b].add(a)
    require(len(used)==len(vs),'E_TOPOLOGY','Unused material vertices.')
    require(abs(area-w*h)<=max(1e-6,w*h*1e-8),'E_COVERAGE','Material triangle area does not equal original sheet area.')
    for edge, use in edge_use.items():
        require(len(use) in (1,2),'E_TOPOLOGY','Nonmanifold edge.')
        if len(use)==2:
            require(use[0][:2]==tuple(reversed(use[1][:2])),'E_TOPOLOGY','Inconsistent adjacent material winding.')
        else:
            a,b=[uv[i] for i in edge]
            boundary=any(abs(a[j]-val)<=tolerance and abs(b[j]-val)<=tolerance for j,size in [(0,w),(1,h)] for val in [-size/2,size/2])
            require(boundary,'E_TOPOLOGY','Interior boundary, slit, or nonconforming T-junction.')
    visited=set();stack=[0]
    while stack:
        v=stack.pop()
        if v in visited:continue
        visited.add(v);stack.extend(adj[v]-visited)
    require(len(visited)==len(vs),'E_TOPOLOGY','Disconnected paper mesh.')
    require(len(vs)-len(edge_use)+len(fs)==1,'E_TOPOLOGY','Core topology must be a disk.')

def positions_at(op: dict, meshes: dict, t: float) -> list[list[float]]:
    require(math.isfinite(t) and 0<=t<=1,'E_TIME','Progress is outside [0,1].')
    if op['kind']=='sampled':
        keys=op['keys']
        if t==1:return [p[:] for p in keys[-1]['positionsMm']]
        for a,b in zip(keys,keys[1:]):
            if a['at']<=t<=b['at']:
                k=(t-a['at'])/(b['at']-a['at'])
                return [[x+(y-x)*k for x,y in zip(p,q)] for p,q in zip(a['positionsMm'],b['positionsMm'])]
        raise SpecError('E_TIME','No keyframe interval contains progress.')
    s=t*t*(3-2*t) if op['easing']=='smoothstep' else t
    start=op['startPositionsMm']; a,b=op['axisMm'];angle=math.radians(op['angleDeg'])*s
    if op['kind']=='rigid':
        move=scale(op['translationMm'],s);move[2]+=op['liftMm']*math.sin(math.pi*s)
        return [add(rotate(p,a,b,angle),move) for p in start]
    moving=set(op['movingFaces']);mesh=meshes[op['mesh']]
    ids={i for f in mesh['faces'] if f['id'] in moving for i in f['vertices']}
    return [rotate(p,a,b,angle) if i in ids else p[:] for i,p in enumerate(start)]

def material_position(mesh: dict, positions: list, p: list, eps=1e-7):
    uv=[v['uvMm'] for v in mesh['vertices']]
    for f in mesh['faces']:
        i,j,k=f['vertices'];a,b,c=uv[i],uv[j],uv[k];den=2*triangle_area2(a,b,c)
        vb=((p[0]-a[0])*(c[1]-a[1])-(p[1]-a[1])*(c[0]-a[0]))/den
        vc=((b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]))/den;va=1-vb-vc
        if min(va,vb,vc)>=-eps:
            return [va*positions[i][x]+vb*positions[j][x]+vc*positions[k][x] for x in range(3)]
    raise SpecError('E_COVERAGE','Material sample is not covered by previous mesh.')

def continuity(prev_mesh,prev_positions,mesh,positions,eps):
    # Both directions, plus edge midpoints and centroids: vertex-only checks miss lost bends.
    for a,ap,b,bp in [(prev_mesh,prev_positions,mesh,positions),(mesh,positions,prev_mesh,prev_positions)]:
        uv=[v['uvMm'] for v in a['vertices']]
        samples=[(p,ap[i]) for i,p in enumerate(uv)]
        for i,j in mesh_edges(a):samples.append((scale(add(uv[i],uv[j]),.5),scale(add(ap[i],ap[j]),.5)))
        for f in a['faces']:
            ids=f['vertices'];samples.append(([sum(uv[i][x] for i in ids)/3 for x in range(2)],[sum(ap[i][x] for i in ids)/3 for x in range(3)]))
        for p,pos in samples:
            require(norm(sub(pos,material_position(b,bp,p)))<=eps,'E_CONTINUITY','Geometry teleports or loses a bend at an operation boundary.')

def _hint(h,nfaces):
    require(len(h['ranks'])==nfaces and abs(norm(h['axis'])-1)<1e-6,'E_LAYER','Layer hint dimensions or unit axis invalid.')

def validate_geometry(d: dict) -> dict:
    g=d.get('geometry')
    if not g:return {'operations':0,'triangles':0,'maxMeasuredRelativeEdgeError':0.0,'checks':'no-geometry'}
    sheets=indexed(d['sheets'],'sheet');meshes=indexed(g['meshes'],'mesh');ops=indexed(g['operations'],'operation');tol=g['tolerances'];eps=tol['positionMm']
    for m in meshes.values():
        require(m['sheet'] in sheets,'E_REFERENCE','Mesh sheet is missing.');validate_mesh(m,sheets[m['sheet']],eps)
    require({m['sheet'] for m in meshes.values()}==set(sheets),'E_REFERENCE','Resolved geometry must include a mesh for every declared sheet.')
    last={}; maximum=0.;intervals=0; crease_identities={}
    for op in ops.values():
        require(op['mesh'] in meshes and op['sheet'] in sheets,'E_REFERENCE','Missing operation mesh or sheet.')
        mesh=meshes[op['mesh']];require(mesh['sheet']==op['sheet'],'E_REFERENCE','Operation mesh is on a different sheet.')
        count=len(mesh['vertices']);fids={f['id'] for f in mesh['faces']}
        uv=[v['uvMm'] for v in mesh['vertices']];edges=mesh_edges(mesh)
        for c in op['creases']:
            identity=(c['sheet'], sorted(tuple(x) for x in c['segmentMm']))
            if c['id'] in crease_identities:require(identity==crease_identities[c['id']], 'E_CREASE', 'A persistent crease ID changed material location.')
            crease_identities[c['id']]=identity
            require(c['sheet']==op['sheet'],'E_REFERENCE','Crease sheet mismatch.')
            require(norm(sub(*c['segmentMm']))>1e-8,'E_CREASE','Zero-length crease.')
            w,h=sheets[op['sheet']]['widthMm'],sheets[op['sheet']]['heightMm']
            require(all(abs(p[0])<=w/2+eps and abs(p[1])<=h/2+eps for p in c['segmentMm']),'E_CREASE','Crease endpoint outside sheet.')
        for layer in op['layers']:
            require(layer['firstFace'] in fids and layer['secondFace'] in fids and layer['firstFace']!=layer['secondFace'],'E_LAYER','Missing or identical faces in layer relation.')
            require(abs(norm(layer['normal'])-1)<1e-6,'E_LAYER','Layer normal must be unit length.')
        if op['kind']=='sampled':
            keys=op['keys'];require(keys[0]['at']==0 and keys[-1]['at']==1 and all(a['at']<b['at'] for a,b in zip(keys,keys[1:])),'E_TIME','Key times must strictly increase from 0 to 1.')
            require(all(len(k['positionsMm'])==count for k in keys),'E_DIMENSION','Keyframe vertex count differs from mesh.')
            require(op['maxRelativeEdgeError']<=tol['relativeEdge'],'E_STRAIN','Operation budget exceeds document budget.')
            for key in keys:
                if 'layerHint' in key:_hint(key['layerHint'],len(mesh['faces']))
            for ka,kb in zip(keys,keys[1:]):
                intervals+=1
                for i,j in edges:
                    rest=norm(sub(uv[i],uv[j]));a=sub(ka['positionsMm'][i],ka['positionsMm'][j]);b=sub(sub(kb['positionsMm'][i],kb['positionsMm'][j]),a)
                    bb=dot(b,b);s=max(0.,min(1.,-dot(a,b)/bb)) if bb>1e-24 else 0.
                    vals=[norm(a),norm(add(a,b)),norm(add(a,scale(b,s)))]
                    e=max(abs(x/rest-1) for x in vals);maximum=max(maximum,e)
                    require(e<=op['maxRelativeEdgeError']+2e-8,'E_STRAIN',f'Continuous interval edge error {e:.8g} exceeds declared budget in {op["id"]}.')
        else:
            require(len(op['startPositionsMm'])==count,'E_DIMENSION','Start vertex count differs from mesh.')
            a,b=op['axisMm'];axis=unit(sub(b,a))
            if op['kind']=='hinge':
                require(abs(op['angleDeg'])>1e-10,'E_AXIS','Hinge rotation cannot be zero.')
                moving=set(op['movingFaces']);require(moving<=fids and moving!=fids,'E_SELECTION','Hinge needs known moving faces and stationary paper.')
                incidence=defaultdict(set)
                for f in mesh['faces']:
                    for i in f['vertices']:incidence[i].add(f['id'] in moving)
                for i,kinds in incidence.items():
                    if len(kinds)==2:require(norm(cross(sub(op['startPositionsMm'][i],a),axis))<=eps,'E_TEAR','Moving/stationary shared vertex is off the hinge.')
                for field in ('startLayerHint','endLayerHint'):
                    if field in op:_hint(op[field],len(mesh['faces']))
            for i,j in edges:
                e=abs(norm(sub(op['startPositionsMm'][i],op['startPositionsMm'][j]))/norm(sub(uv[i],uv[j]))-1)
                maximum=max(maximum,e);require(e<=tol['relativeEdge']+2e-8,'E_STRAIN','Initial operation edge error exceeds document budget.')
        start=positions_at(op,meshes,0);end=positions_at(op,meshes,1)
        if op['sheet'] in last:
            pm,pp=last[op['sheet']];continuity(pm,pp,mesh,start,eps)
        else:require(all(norm(sub(p,[*v['uvMm'],0]))<=eps for p,v in zip(start,mesh['vertices'])),'E_INITIAL','First operation must begin with the original flat sheet.')
        last[op['sheet']]=(mesh,end)
    return {'operations':len(ops),'triangles':sum(len(m['faces']) for m in meshes.values()),'sampledIntervals':intervals,'maxMeasuredRelativeEdgeError':maximum,'checks':'disk-topology,material-coverage,boundary-samples,analytic-edge-intervals'}

def validate_authoring(d: dict) -> None:
    a=d.get('authoring')
    if not a:return
    frames=indexed(a['frames'],'construction frame');points=indexed(a['points'],'point');lines=indexed(a['lines'],'line');regions=indexed(a['regions'],'region');intents=indexed(a['intents'],'intent')
    require(len(set(points)|set(lines)|set(regions)|set(intents))==len(points)+len(lines)+len(regions)+len(intents),'E_DUPLICATE_ID','Authoring names must be distinct across geometric types.')
    sheets={s['id'] for s in d['sheets']}; opmap={o['id']:o for o in d.get('geometry',{}).get('operations',[])};ops=set(opmap)
    for f in frames.values():
        require(f['sheet'] in sheets,'E_REFERENCE','Frame sheet is missing.')
        require(f['afterOperation'] is None or f['afterOperation'] in ops,'E_REFERENCE','Frame operation is missing.')
        require(f['afterOperation'] is None or opmap[f['afterOperation']]['sheet']==f['sheet'],'E_FRAME','Frame operation belongs to a different sheet.')
        require(abs(norm(f['u'])-1)<1e-6 and abs(norm(f['v'])-1)<1e-6 and abs(dot(f['u'],f['v']))<1e-6,'E_FRAME','Construction basis is not orthonormal.')
    deps={k:set() for k in list(points)+list(lines)+list(regions)}
    def dependency(owner,name,table):
        require(name in table,'E_REFERENCE',f'{owner} refers to missing/wrong-typed {name}.');deps[owner].add(name)
    for p in points.values():
        require(p['frame'] in frames,'E_REFERENCE','Point frame missing.'); x=p['definition'];k=x['kind']
        if k=='material':
            require(x['sheet'] in sheets and x['sheet']==frames[p['frame']]['sheet'],'E_REFERENCE','Material point sheet/frame mismatch.')
            source_sheet=next(sh for sh in d['sheets'] if sh['id']==x['sheet'])
            require(abs(x['uvMm'][0])<=source_sheet['widthMm']/2 and abs(x['uvMm'][1])<=source_sheet['heightMm']/2,'E_MATERIAL','Named material point lies outside its sheet.')
        elif k in ('midpoint','ratio','intersection'):
            table=lines if k=='intersection' else points
            for field in ('a','b'):dependency(p['id'],x[field],table)
            if k=='ratio':require(x['numerator']<=x['denominator'],'E_RATIO','Ratio point must lie on its segment.')
    for l in lines.values():
        require(l['frame'] in frames,'E_REFERENCE','Line frame missing.');x=l['definition'];k=x['kind']
        if k=='through':
            for field in ('a','b'):dependency(l['id'],x[field],points)
        elif k in ('perpendicular','angle'):
            dependency(l['id'],x['line'],lines);dependency(l['id'],x['point'],points)
        else:
            c=x['constraint'];ck=c['kind']
            mappings={'through-points':{'a':points,'b':points},'point-to-point':{'a':points,'b':points},'line-to-line':{'a':lines,'b':lines},'perpendicular-through':{'line':lines,'point':points},'point-to-line-through':{'point':points,'line':lines,'through':points},'two-points-to-lines':{'a':points,'lineA':lines,'b':points,'lineB':lines},'point-to-line-perpendicular':{'point':points,'line':lines,'perpendicularTo':lines}}
            for field,table in mappings[ck].items():dependency(l['id'],c[field],table)
            if x['branch']['mode']=='witness':require(abs(norm(x['branch']['normal'])-1)<1e-6,'E_BRANCH','Witness normal must be unit length.')
    for r in regions.values():
        require(r['sheet'] in sheets and r['frame'] in frames,'E_REFERENCE','Region frame or sheet missing.')
        require(frames[r['frame']]['sheet']==r['sheet'],'E_FRAME','Region and frame sheets differ.');x=r['definition'];k=x['kind']
        if k=='half-plane':dependency(r['id'],x['line'],lines);dependency(r['id'],x['containsPoint'],points)
        elif k!='polygon':
            for field in ('a','b'):dependency(r['id'],x[field],regions)
    allnodes={**points,**lines,**regions}
    for k,v in deps.items():
        require(all(allnodes[k]['frame']==allnodes[x]['frame'] for x in v),'E_FRAME','Construction dependencies cross coordinate frames without an explicit conversion.')
    visiting=set();done=set()
    def visit(n):
        require(n not in visiting,'E_CYCLE','Construction dependency cycle.')
        if n in done:return
        visiting.add(n)
        for nxt in deps[n]:visit(nxt)
        visiting.remove(n);done.add(n)
    for n in deps:visit(n)
    for i in intents.values():
        require(i['sheet'] in sheets and i['crease'] in lines and i['movingRegion'] in regions,'E_REFERENCE','Intent references missing geometry.')
        if 'materialFilter'in i:
            sh=next(sh for sh in d['sheets'] if sh['id']==i['sheet'])
            require(all(abs(p[0])<=sh['widthMm']/2 and abs(p[1])<=sh['heightMm']/2 for polygon in i['materialFilter'] for p in polygon),'E_MATERIAL','Intent material filter lies outside the original sheet.')
        require(all(o in ops for o in i['resolvedOperations']),'E_REFERENCE','Intent compiled-operation reference missing.')
        require(regions[i['movingRegion']]['sheet']==i['sheet'] and frames[lines[i['crease']]['frame']]['sheet']==i['sheet'],'E_FRAME','Intent crease and selection must belong to its sheet.')
        require(lines[i['crease']]['frame']==regions[i['movingRegion']]['frame'],'E_FRAME','Intent crease and selection must use one frame.')
        require(all(opmap[o]['sheet']==i['sheet'] for o in i['resolvedOperations']),'E_REFERENCE','Intent cannot bind another sheet operation.')
    assets={a['id']:a for a in d['assets']}
    indexed(a['imports'],'library instance')
    for instance in a['imports']:
        require(instance['asset'] in assets and assets[instance['asset']]['role']=='library' and instance['sheet'] in sheets,'E_REFERENCE','Library asset/sheet missing.')
        require(all(o in ops for o in instance['expandedOperationIds']),'E_REFERENCE','Expanded operation missing.')

def validate_document(d: dict, *, geometry=True) -> dict:
    schema_validate(d);check_tree(d);validate_locales(d)
    sheets=indexed(d['sheets'],'sheet');steps=indexed(d['instructions']['steps'],'step');assets=indexed(d['assets'],'asset');sources=indexed(d['metadata']['sources'],'source');landmarks=indexed(d['accessibility']['landmarks'],'landmark');narration=indexed(d['narration'],'narration')
    indexed(d['history'],'history');indexed(d['extensions'],'extension');paths=set()
    for a in assets.values():
        expected={'background':('image/png','image/jpeg','image/webp'),'paper-image':('image/png','image/jpeg','image/webp'),'narration':('audio/mpeg','audio/ogg','audio/wav'),'library':('application/json',)}
        require(a['role'] not in expected or a['mediaType'] in expected[a['role']],'E_ASSET_ROLE','Asset media type disagrees with its role.')
        path=safe_path(a['path']);key=path.casefold()
        require(key not in paths and key not in ('manifest.json','document.json'),'E_PATH','Duplicate, case-colliding, or reserved asset path.');paths.add(key)
    for s in sheets.values():
        for face in ('front','back'):
            m=s[face]
            if 'imageAsset' in m:require(m['imageAsset'] in assets and assets[m['imageAsset']]['role']=='paper-image','E_REFERENCE','Paper-image asset missing.')
    for l in landmarks.values():
        require(l['sheet'] in sheets,'E_REFERENCE','Landmark sheet missing.')
        if 'uvMm' in l:
            s=sheets[l['sheet']];require(abs(l['uvMm'][0])<=s['widthMm']/2 and abs(l['uvMm'][1])<=s['heightMm']/2,'E_MATERIAL','Landmark outside sheet.')
    for s in steps.values():
        require(set(s['tactile']['landmarkIds'])<=set(landmarks),'E_REFERENCE','Step tactile landmark missing.')
        require(set(s.get('narrationIds',[]))<=set(narration),'E_REFERENCE','Step narration missing.')
        require(all(narration[n]['step']==s['id'] for n in s.get('narrationIds',[])), 'E_REFERENCE', 'Narration belongs to a different step.')
        require(bool(s['runs'])==(s['animation']=='resolved'),'E_STATUS','Resolved steps need runs; unanimated steps must not contain runs.')
        require(not(s['kind']in ('fold','unfold','turn-over','rotate','shape','assemble') and s['animation']=='not-applicable'),'E_STATUS','Physical action cannot be marked animation-not-applicable.')
        for r in s['runs']:require(r['from']<r['to'],'E_TIME','Step run must have positive length.')
    groups=indexed(d['instructions']['groups'],'instruction group')
    for g in groups.values():require(set(g['stepIds'])<=set(steps),'E_REFERENCE','Group step missing.')
    ops=d.get('geometry',{}).get('operations',[]);opmap=indexed(ops,'operation')
    flat=[r for s in steps.values() for r in s['runs']]
    oi=0;progress=0.
    for r in flat:
        require(oi<len(ops) and r['operation']==ops[oi]['id'] and abs(r['from']-progress)<=1e-10,'E_RUN_COVERAGE','Instruction runs must cover operations in order without gaps, overlap, or reorder.')
        progress=r['to']
        if progress==1:oi+=1;progress=0.
    require(oi==len(ops) and progress==0,'E_RUN_COVERAGE','Some geometry is not represented in instruction runs.')
    if d['status']=='partial':
        require(any(x['animation']=='not-authored' for x in steps.values()),'E_STATUS','Partial geometry must disclose at least one unauthored instruction.')
        gap=False
        for x in steps.values():
            if x['animation']=='not-authored':gap=True
            require(not(gap and x['runs']),'E_RUN_COVERAGE','Partial geometry is a prefix; playback cannot resume beyond an unresolved physical action.')
    if d['status']=='resolved':require(all(s['animation']!='not-authored' for s in steps.values()),'E_STATUS','Resolved document contains an unanimated physical instruction.')
    for n in narration.values():
        if 'url' in n:safe_https(n['url'])
        require(n['step'] in steps,'E_REFERENCE','Narration step missing.')
        require(digest(n['transcript'].encode('utf-8'))==n['textSha256'],'E_NARRATION_HASH','Narration transcript digest mismatch.')
        if n['status']=='ready':require(('asset' in n)^('url' in n),'E_NARRATION','Ready narration requires exactly one asset or URL.')
        else:require('asset' not in n and 'url' not in n,'E_NARRATION','Missing/stale narration must not auto-reference playable content.')
        if 'asset' in n:require(n['asset'] in assets and assets[n['asset']]['role']=='narration','E_REFERENCE','Narration asset missing.')
        if n['variant']=='primary' and n['status']=='ready':require(steps[n['step']]['body'].get(n['locale'])==n['transcript'],'E_NARRATION_STALE','Primary narration text differs from instruction locale.')
    for source in sources.values():safe_https(source['url'])
    for h in d['history']:require(set(h['sourceIds'])<=set(sources),'E_REFERENCE','Historical source missing.')
    p=d.get('presentation')
    if p:
        require(set(p['finishingStepIds'])<=set(steps),'E_REFERENCE','Finishing step missing.')
        if p['status']=='resolved':
            require(d['status']=='resolved' and p['display'].get('afterOperation')==ops[-1]['id'],'E_PRESENTATION','Resolved display must follow the last operation of a fully resolved document.')
        if 'afterOperation' in p['display']:require(p['display']['afterOperation'] in opmap,'E_REFERENCE','Display operation missing.')
        rigs=indexed(p['rigs'],'rig');fl=p['flourish']
        if fl['status']=='resolved':
            require(p['status']=='resolved','E_PRESENTATION','Resolved flourish requires resolved display.')
            if fl['kind']=='flutter':require(fl.get('rig') in rigs,'E_RIG','Flutter requires an authored rig.')
            elif fl['kind']!='none':require('axisMm' in fl and norm(sub(*fl['axisMm']))>1e-8,'E_AXIS','Root flourish requires a nonzero axis.')
        for rig in rigs.values():
            require(rig['afterOperation'] in opmap and rig['sheet'] in sheets,'E_REFERENCE','Rig operation/sheet missing.')
            require(opmap[rig['afterOperation']]['sheet']==rig['sheet'],'E_RIG','Rig pose belongs to another sheet.')
            require(rig['afterOperation']==[o['id'] for o in ops if o['sheet']==rig['sheet']][-1], 'E_RIG','Rig must refer to its sheet final operation.')
            axis=unit(sub(rig['axisMm'][1],rig['axisMm'][0]));normal=rig['partitionNormal']
            require(abs(norm(normal)-1)<1e-6 and abs(dot(axis,normal))<1e-6,'E_RIG','Rig plane is not perpendicular to its hinge.')
            if geometry:
                op=opmap[rig['afterOperation']];meshes=indexed(d['geometry']['meshes'],'mesh');m=meshes[op['mesh']];positions=positions_at(op,meshes,1);a=rig['axisMm'][0];eps=d['geometry']['tolerances']['positionMm'];sides=set();inc=defaultdict(set)
                for f in m['faces']:
                    values=[dot(sub(positions[i],a),normal) for i in f['vertices']]
                    require(not(min(values)<-eps and max(values)>eps),'E_RIG','Face straddles the wing partition.')
                    side=1 if max(values)>eps else -1 if min(values)<-eps else 0
                    if side:sides.add(side)
                    for i in f['vertices']:inc[i].add(side)
                require(sides=={-1,1},'E_RIG','Rig needs paper on both sides.')
                for i,ss in inc.items():
                    if -1 in ss and 1 in ss:require(norm(cross(sub(positions[i],a),axis))<=eps,'E_RIG','Wing seam is off its hinge.')
        if 'stage' in p:
            st=p['stage'];keys=st['keys'];require(keys[0]['at']==0 and keys[-1]['at']==1 and all(a['at']<b['at'] for a,b in zip(keys,keys[1:])),'E_TIME','Stage keys must increase from 0 to 1.')
            if 'backgroundAsset' in st:require(st['backgroundAsset'] in assets and assets[st['backgroundAsset']]['role']=='background','E_REFERENCE','Stage background missing.')
    if 'print' in d:
        require(all(panel['step'] in steps for panel in d['print']['panels']),'E_REFERENCE','Print panel step missing.')
    validate_authoring(d)
    stats=validate_geometry(d) if geometry else {'checks':'geometry-not-run'}
    return {'format':d['format'],'specVersion':d['specVersion'],'id':d['id'],'status':d['status'],'steps':len(steps),'assets':len(assets),'geometry':stats,'requiredExtensions':{scope:[x['id'] for x in d['extensions'] if scope in x['requiredFor']] for scope in ('text','authoring','playback','presentation','print')},'notChecked':['self-collision','finite-thickness feasibility','physical folding','assistive-technology usability','pixel-equivalent rendering','all symbolic alignment solving']}

def asset_data(directory: Path, asset: dict) -> bytes:
    relative=safe_path(asset['path']);candidate=directory / relative
    current=directory
    for segment in relative.split('/'):
        current=current/segment;require(not current.is_symlink(),'E_PATH','Asset symlink rejected.')
    require(candidate.is_file(),'E_ASSET',f'Missing asset {relative}.')
    require(candidate.resolve().is_relative_to(directory.resolve()),'E_PATH','Asset escaped source directory.')
    require(candidate.stat().st_size<=MAX_ENTRY,'E_LIMIT','Asset exceeds reference entry limit.')
    data=candidate.read_bytes();check_asset_bytes(data,asset);return data

def check_asset_bytes(data: bytes, asset: dict) -> None:
    require(len(data)==asset['byteLength'],'E_ASSET_SIZE','Asset byte length mismatch.')
    require(digest(data)==asset['sha256'],'E_ASSET_HASH','Asset digest mismatch.')
    mt=asset['mediaType']
    if mt=='image/png':
        import struct,zlib
        require(data.startswith(b'\x89PNG\r\n\x1a\n'),'E_IMAGE','PNG signature missing.')
        at=8;chunks=[]
        while at<len(data):
            require(at+12<=len(data),'E_IMAGE','Truncated PNG chunk.')
            size=int.from_bytes(data[at:at+4],'big');kind=data[at+4:at+8];end=at+12+size
            require(end<=len(data),'E_IMAGE','PNG chunk exceeds entry.')
            payload=data[at+8:at+8+size];crc=int.from_bytes(data[at+8+size:end],'big')
            require(zlib.crc32(kind+payload)&0xffffffff==crc,'E_IMAGE','PNG chunk CRC mismatch.')
            if not chunks:
                require(kind==b'IHDR' and size==13,'E_IMAGE','PNG must begin with IHDR.')
                w,h=struct.unpack('>II',payload[:8]);require(0<w<=8192 and 0<h<=8192 and w*h<=16777216,'E_IMAGE','Image pixel budget exceeded.')
            require(kind!=b'acTL','E_IMAGE','Animated PNG not part of static image profile.')
            chunks.append(kind);at=end
            if kind==b'IEND':require(size==0 and at==len(data),'E_IMAGE','Invalid IEND or trailing bytes.')
        require(chunks and chunks[-1]==b'IEND' and b'IDAT' in chunks,'E_IMAGE','PNG lacks IDAT/IEND.')
    elif mt=='image/jpeg':require(data.startswith(b'\xff\xd8') and data.endswith(b'\xff\xd9'),'E_IMAGE','JPEG signature mismatch.')
    elif mt=='image/webp':require(data[:4]==b'RIFF' and data[8:12]==b'WEBP','E_IMAGE','WebP signature mismatch.')
    elif mt=='application/json':loads(data)
    elif mt=='text/plain':check_tree(data.decode('utf-8'))
    # Media decode remains the responsibility of a sandboxed platform decoder.

def load_document(path: Path, *, geometry=True) -> tuple[dict, dict]:
    if path.suffix=='.foldlab':return inspect_package(path,geometry=geometry)
    require(path.stat().st_size<=MAX_ENTRY,'E_LIMIT','Document too large.')
    d=loads(path.read_bytes());report=validate_document(d,geometry=geometry)
    for a in d['assets']:asset_data(path.parent,a)
    return d,report

def pack_document(path: Path, destination: Path) -> dict:
    d,_=load_document(path);document=json_bytes(d);payloads={'document.json':document}
    for a in d['assets']:payloads[a['path']]=asset_data(path.parent,a)
    require(sum(map(len,payloads.values()))<=MAX_TOTAL,'E_LIMIT','Expanded package exceeds policy.')
    manifest={'format':'fold-spec-package','specVersion':VERSION,'document':'document.json','entries':[{'path':p,'byteLength':len(b),'sha256':digest(b)} for p,b in sorted(payloads.items())]}
    destination.parent.mkdir(parents=True,exist_ok=True)
    require(not destination.exists(),'E_EXISTS','Refusing to overwrite an existing package.')
    try:
        with zipfile.ZipFile(destination,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for name,data in [('manifest.json',json_bytes(manifest)),*sorted(payloads.items())]:
                info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(stat.S_IFREG|0o644)<<16;info.create_system=3
                z.writestr(info,data)
        require(destination.stat().st_size<=MAX_ARCHIVE,'E_LIMIT','Compressed archive exceeds policy.')
        _,report=inspect_package(destination)
        return {'path':str(destination),'bytes':destination.stat().st_size,'sha256':digest(destination.read_bytes()),'document':report}
    except Exception:
        destination.unlink(missing_ok=True);raise

def inspect_package(path: Path, *, geometry=True) -> tuple[dict,dict]:
    require(path.is_file() and path.stat().st_size<=MAX_ARCHIVE,'E_LIMIT','Package missing or too large.')
    try:
        with zipfile.ZipFile(path) as z:
            infos=z.infolist();require(1<len(infos)<=MAX_ENTRIES,'E_LIMIT','Invalid entry count.');names=set();folded=set();total=0
            for i in infos:
                safe_path(i.filename);require(i.filename not in names and i.filename.casefold() not in folded,'E_PATH','Duplicate/case-colliding package entry.');names.add(i.filename);folded.add(i.filename.casefold())
                mode=(i.external_attr>>16)&0xffff
                require(not stat.S_ISLNK(mode) and (stat.S_IFMT(mode) in (0,stat.S_IFREG)) and not i.is_dir() and not (mode & 0o111),'E_PATH','Only non-executable regular files are allowed.')
                require(i.extract_version < 45,'E_ZIP','ZIP64 and newer ZIP extensions are not supported by this package profile.')
                require(not(i.flag_bits&1) and i.compress_type in (zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED),'E_ZIP','Encrypted or unsupported compression.')
                extra=0
                while extra<len(i.extra):
                    require(extra+4<=len(i.extra),'E_ZIP','Truncated extra field.')
                    tag=int.from_bytes(i.extra[extra:extra+2],'little');size=int.from_bytes(i.extra[extra+2:extra+4],'little')
                    require(tag!=1 and extra+4+size<=len(i.extra),'E_ZIP','ZIP64 or invalid extra field.')
                    extra+=4+size
                require(i.file_size<=MAX_ENTRY,'E_LIMIT','Expanded entry too large.');total+=i.file_size
            require(total<=MAX_TOTAL and 'manifest.json' in names and 'document.json' in names,'E_LIMIT','Missing required entries or expanded budget exceeded.')
            def read(name):
                data=bytearray()
                with z.open(name) as f:
                    while chunk:=f.read(65536):
                        data.extend(chunk);require(len(data)<=MAX_ENTRY,'E_LIMIT','Actual expansion exceeds limit.')
                return bytes(data)
            manifest=loads(read('manifest.json'));schema_validate(manifest,'manifest.schema.json');entries=manifest['entries'];en={}
            for e in entries:
                p=safe_path(e['path']);require(p not in en and p!='manifest.json','E_MANIFEST','Duplicate/self manifest entry.');en[p]=e
            require(set(en)==names-{'manifest.json'},'E_MANIFEST','Manifest must declare exactly every payload.')
            payloads={p:read(p) for p in en}
            for p,data in payloads.items():require(len(data)==en[p]['byteLength'] and digest(data)==en[p]['sha256'],'E_PACKAGE_HASH',f'Payload integrity mismatch: {p}.')
            d=loads(payloads['document.json']);require(d.get('specVersion')==manifest['specVersion'],'E_VERSION','Manifest/document version mismatch.')
            report=validate_document(d,geometry=geometry)
            require(set(payloads)=={'document.json'}|{a['path'] for a in d['assets']},'E_MANIFEST','Unreferenced or absent document asset.')
            for a in d['assets']:check_asset_bytes(payloads[a['path']],a)
            report['package']={'entries':len(infos),'expandedBytes':total,'sha256':digest(path.read_bytes())}
            return d,report
    except (zipfile.BadZipFile,RuntimeError,EOFError) as exc:raise SpecError('E_ZIP',str(exc)) from exc

def resolve_locale(value:dict,locale:str,default:str)->tuple[str,str]:
    candidates=[locale,*['-'.join(locale.split('-')[:i]) for i in range(len(locale.split('-'))-1,0,-1)],default]
    lookup={k.lower():k for k in value}
    for key in candidates:
        actual=lookup.get(key.lower())
        if actual is not None:return actual,value[actual]
    raise SpecError('E_LOCALE','No default-locale text.')

def get_text(value:dict,locale:str,default:str)->str:
    return resolve_locale(value,locale,default)[1]

def text_export(d:dict,locale:str|None=None,descriptive:bool=False)->str:
    require(not any('text'in x['requiredFor'] for x in d['extensions']),'E_UNSUPPORTED','Unknown required text extension.')
    loc=locale or d['defaultLocale'];t=lambda v:get_text(v,loc,d['defaultLocale']);lines=[t(d['metadata']['title']),f"Document: {d['id']} / revision {d['revision']}",f"Status: {d['status']}",'',t(d['metadata']['summary']),'','SETUP']
    lines += [t(v) for v in d['accessibility']['setup']]
    lines += ['', 'AUTHORS']+[a['name']+' — '+', '.join(a['roles']) for a in d['metadata']['authors']]
    if 'rightsNote' in d['metadata']:lines += ['RIGHTS: '+t(d['metadata']['rightsNote'])]
    for i,s in enumerate(d['instructions']['steps'],1):
        lines+=['',f"{i}. {t(s['title'])}",t(s['body'])]
        if s['animation']=='not-authored':lines+=['Animation not authored for this step.']
        if descriptive:
            a=s['tactile'];lines+=['Orientation: '+t(a['orientation'])]
            for field,label in [('locate','Locate'),('check','Check by touch'),('recovery','Recovery')]:lines += [label+': '+t(v) for v in a[field]]
    if 'presentation' in d:
        p=d['presentation'];lines+=['','FINAL PRESENTATION',t(p['display']['orientation'])];lines += [t(c) for c in p['display']['checks']]
        lines+=['Presentation status: '+p['status']+'. Decorative animation is not a folding instruction.']
    for h in d['history']:lines+=['','CONTEXT: '+t(h['title']),t(h['summary']), *[t(v) for v in h['qualifications']], 'Sources: '+', '.join(h['sourceIds'])]
    lines+=['','LIMITATIONS']+[t(v) for v in d['accessibility']['limitations']]
    if 'geometry' in d:lines += [t(v) for v in d['geometry']['limitations']]
    lines+=['','SOURCES']+[f"{s['id']}: {s['title']} — {s['url']}"+(' — Rights: '+s['rightsNote'] if 'rightsNote' in s else '') for s in d['metadata']['sources']]
    lines+=['','LICENSE: '+d['metadata']['license']]
    return '\n'.join(lines)+'\n'

def html_export(d:dict,locale:str|None=None,descriptive:bool=False)->str:
    # A semantic text view, not a 3D visualizer. Escapes all author strings.
    require(not any('text'in x['requiredFor'] for x in d['extensions']),'E_UNSUPPORTED','Unknown required text extension.')
    for source in d['metadata']['sources']:safe_https(source['url'])
    loc=locale or d['defaultLocale']; t=lambda v:html.escape(get_text(v,loc,d['defaultLocale'])); esc=html.escape
    def localized(v,tag='p'):
        actual,_=resolve_locale(v,loc,d['defaultLocale'])
        return f'<{tag} lang="{esc(actual)}">{t(v)}</{tag}>'
    parts=[f'<!doctype html><html lang="{esc(d["defaultLocale"])}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t(d["metadata"]["title"])}</title><style>body{{max-width:72ch;margin:auto;padding:2rem;font:1.05rem/1.75 system-ui,sans-serif;color:#182734;background:#faf9f5}}section{{margin-block:2rem}}:focus-visible{{outline:3px solid #245ab5}}@media(prefers-color-scheme:dark){{body{{color:#eee;background:#18212a}}a{{color:#afd6ff}}}}@media print{{body{{color:#111;background:white}}}}</style><main>',localized(d['metadata']['title'],'h1'),localized(d['metadata']['summary']),'<p>Status: '+esc(d['status'])+'</p>', '<h2>Setup</h2>']
    parts += [localized(v) for v in d['accessibility']['setup']]
    parts += ['<p>Authors: '+esc('; '.join(a['name']+' ('+', '.join(a['roles'])+')' for a in d['metadata']['authors']))+'</p>']
    if 'rightsNote' in d['metadata']:parts += ['<h2>Rights</h2>',localized(d['metadata']['rightsNote'])]
    for i,s in enumerate(d['instructions']['steps'],1):
        parts += [f'<section id="{esc(s["id"])}"><h2 lang="{esc(resolve_locale(s["title"],loc,d["defaultLocale"])[0])}">{i}. {t(s["title"])}</h2>',localized(s['body'])]
        if s['animation']=='not-authored':parts+=['<p>Animation not authored for this step.</p>']
        if descriptive:
            a=s['tactile'];parts += ['<h3>Orientation</h3>',localized(a['orientation'])]
            for key,label in [('locate','Locate'),('check','Check by touch'),('recovery','Recovery')]:
                if a[key]:parts+=['<h3>'+label+'</h3>']+[localized(v) for v in a[key]]
        parts += ['</section>']
    if 'presentation' in d:
        p=d['presentation'];parts+=['<section><h2>Final presentation</h2>',localized(p['display']['orientation'])]+[localized(v) for v in p['display']['checks']]+[f'<p>Presentation status: {esc(p["status"])}. Flourish playback is not a folding instruction.</p></section>']
    for h in d['history']:
        parts+=['<section><h2>'+t(h['title'])+'</h2>',localized(h['summary']),*[localized(v) for v in h['qualifications']],'<p>Sources: '+esc(', '.join(h['sourceIds']))+'</p></section>']
    parts+=['<section><h2>Limitations</h2>']+[localized(v) for v in d['accessibility']['limitations']]
    if 'geometry' in d:parts += [localized(v) for v in d['geometry']['limitations']]
    parts+=['</section><section><h2>Sources</h2><ul>']+[f'<li><a rel="noreferrer" href="{esc(s["url"],quote=True)}">{esc(s["title"])}</a>'+(' — Rights: '+esc(s['rightsNote']) if 'rightsNote' in s else '')+'</li>' for s in d['metadata']['sources']]+['</ul></section><p>License: '+esc(d['metadata']['license'])+'</p></main></html>']
    return '\n'.join(parts)

def main(argv=None)->int:
    p=argparse.ArgumentParser(description=__doc__);commands=p.add_subparsers(dest='command',required=True)
    for name in ('validate','inspect'):
        sp=commands.add_parser(name);sp.add_argument('file',type=Path);sp.add_argument('--schema-only',action='store_true')
    sp=commands.add_parser('pack');sp.add_argument('file',type=Path);sp.add_argument('-o','--output',type=Path,required=True)
    sp=commands.add_parser('text');sp.add_argument('file',type=Path);sp.add_argument('-o','--output',type=Path);sp.add_argument('--locale');sp.add_argument('--descriptive',action='store_true');sp.add_argument('--html',action='store_true')
    sp=commands.add_parser('sample');sp.add_argument('file',type=Path);sp.add_argument('--operation',required=True);sp.add_argument('--progress',type=float,required=True);sp.add_argument('-o','--output',type=Path)
    sp=commands.add_parser('parse-source');sp.add_argument('file',type=Path);sp.add_argument('-o','--output',type=Path,required=True)
    args=p.parse_args(argv)
    try:
        if args.command=='pack':result=pack_document(args.file,args.output)
        elif args.command=='parse-source':
            from source_parser import parse_source
            doc=parse_source(args.file.read_text(encoding='utf-8'));validate_document(doc);args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(json_bytes(doc));result={'output':str(args.output),'interpretation':'authoring AST only; no symbolic compilation claimed'}
        elif args.command in ('validate','inspect'):
            if args.schema_only:
                if args.file.suffix=='.foldlab':raise SpecError('E_COMMAND','--schema-only expects readable document JSON, not an archive.')
                d=loads(args.file.read_bytes());schema_validate(d);result={'id':d['id'],'checks':'schema-only; references/geometry/assets not checked'}
            else:_,result=load_document(args.file)
        else:
            d,report=load_document(args.file)
            if args.command=='text':
                text=(html_export if args.html else text_export)(d,args.locale,args.descriptive)
                if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text,encoding='utf-8');result={'output':str(args.output)}
                else:print(text);return 0
            else:
                require('geometry' in d,'E_UNSUPPORTED','This document has no resolved geometry.')
                require(not any('playback' in x['requiredFor'] for x in d['extensions']),'E_UNSUPPORTED','Unknown required playback extension.')
                meshes=indexed(d['geometry']['meshes'],'mesh');ops=indexed(d['geometry']['operations'],'operation');require(args.operation in ops,'E_REFERENCE','Unknown operation.')
                op=ops[args.operation];result={'operation':op['id'],'progress':args.progress,'mesh':meshes[op['mesh']],'positionsMm':positions_at(op,meshes,args.progress)}
                if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(json_bytes(result));result={'output':str(args.output)}
        print(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False));return 0
    except (SpecError,OSError,UnicodeError,ValueError) as exc:
        if isinstance(exc,SpecError):out={'error':exc.code,'message':exc.message,'path':exc.path}
        else:out={'error':'E_IO','message':str(exc)}
        print(json.dumps(out,ensure_ascii=False),file=sys.stderr);return 1

if __name__=='__main__':sys.exit(main())
