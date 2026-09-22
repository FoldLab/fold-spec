"""Reference final-pose and flourish sampling; no renderer or paper-physics claims."""
from __future__ import annotations
import math
from foldspec import require, indexed, positions_at, add, sub, dot, rotate

def final_state(document: dict) -> dict:
    require(document['status']=='resolved','E_PRESENTATION','A complete resolved document is required.')
    require(not any('presentation' in x['requiredFor'] or 'playback' in x['requiredFor'] for x in document['extensions']), 'E_UNSUPPORTED','Unknown required presentation/playback extension.')
    meshes=indexed(document['geometry']['meshes'],'mesh');last={}
    for mesh in meshes.values():
        if mesh['sheet'] not in last:last[mesh['sheet']]={'mesh':mesh,'positionsMm':[[*v['uvMm'],0] for v in mesh['vertices']]}
    for op in document['geometry']['operations']:
        last[op['sheet']]={'mesh':meshes[op['mesh']], 'positionsMm':positions_at(op,meshes,1)}
    return last

def flourish_angle(flourish: dict, progress: float, reduced_motion: bool=False) -> float:
    require(math.isfinite(progress) and 0<=progress<=1,'E_TIME','Presentation progress is outside [0,1].')
    if reduced_motion or progress in (0,1) or flourish['kind']=='none':return 0.
    return flourish['amplitudeDeg']*math.sin(math.pi*progress)**2*math.sin(2*math.pi*flourish['cycles']*progress)

def sample_flourish(document: dict, progress: float, reduced_motion: bool=False) -> dict:
    """Returns final source pose with only the declared tip/bow/turn/flutter applied.
    Does not include optional stage travel, paper response or camera transforms.
    Call load_document/validate_document first when accepting untrusted data.
    """
    p=document['presentation'];require(p['status']=='resolved' and p['flourish']['status']=='resolved','E_PRESENTATION','Only a resolved presentation can be sampled.')
    state=final_state(document);f=p['flourish'];angle=math.radians(flourish_angle(f,progress,reduced_motion))
    if angle==0:return state
    if f['kind']=='flutter':
        rig=indexed(p['rigs'],'rig')[f['rig']];a,b=rig['axisMm'];normal=rig['partitionNormal'];target=state[rig['sheet']]
        def deform(point):
            side=dot(sub(point,a),normal)
            return rotate(point,a,b,angle if side>0 else -angle if side<0 else 0)
        target['positionsMm']=[deform(point) for point in target['positionsMm']]
    else:
        a,b=f['axisMm']
        for target in state.values():target['positionsMm']=[rotate(point,a,b,angle) for point in target['positionsMm']]
    return state

def sample_step(document: dict, step_id: str, progress: float) -> dict:
    """Duration-weighted physical run sampling. Reading waits are deliberately excluded.
    A step with no run returns an empty sample list rather than invented geometry.
    """
    require(math.isfinite(progress) and 0<=progress<=1,'E_TIME','Step progress is outside [0,1].')
    step=indexed(document['instructions']['steps'],'step')[step_id]
    if not step['runs']:return {'step':step_id,'samples':[],'animation':step['animation']}
    g=document['geometry'];ops=indexed(g['operations'],'operation');meshes=indexed(g['meshes'],'mesh')
    lengths=[ops[r['operation']]['durationMs']*(r['to']-r['from']) for r in step['runs']];remaining=progress*sum(lengths)
    selected=step['runs'][-1];t=selected['to']
    for run,length in zip(step['runs'],lengths):
        if remaining<length:
            selected=run;t=run['from']+(run['to']-run['from'])*remaining/length;break
        remaining-=length
    op=ops[selected['operation']]
    return {'step':step_id,'operation':op['id'],'progress':t,'positionsMm':positions_at(op,meshes,t),'mesh':meshes[op['mesh']]}
