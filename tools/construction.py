"""Planar construction helpers. Four families are enumerated; all seven witnesses can be checked.
This is a demonstration solver, not a complete symbolic compiler. Unsupported enumeration
raises E_SOLVER_UNSUPPORTED and never picks a guessed crease.
"""
from __future__ import annotations
import math
from foldspec import SpecError, require, norm, sub, add, dot, scale, unit

def canonical(n,d):
    size=norm(n);require(size>1e-12,'E_DEGENERATE','Undefined line normal.')
    n=scale(n,1/size);d/=size
    if n[1]<-1e-12 or (abs(n[1])<=1e-12 and n[0]<0):n=scale(n,-1);d=-d
    return {'normal':n,'offsetMm':d}

def through(a,b):
    v=sub(b,a);require(norm(v)>1e-10,'E_DEGENERATE','Two distinct points required.')
    n=[-v[1],v[0]];return canonical(n,dot(n,a))

def reflect_point(p,line):
    n=line['normal'];return sub(p,scale(n,2*(dot(n,p)-line['offsetMm'])))

def point_line_residual(p,line):return abs(dot(line['normal'],p)-line['offsetMm'])

def intersect(a,b):
    x,y=a['normal'];u,v=b['normal'];det=x*v-y*u
    require(abs(det)>1e-12,'E_DEGENERATE','Parallel/coincident lines have no unique intersection.')
    d,e=a['offsetMm'],b['offsetMm'];return [(d*v-y*e)/det,(x*e-d*u)/det]

def enumerate_solutions(c,points,lines):
    k=c['kind']
    if k=='through-points':return [through(points[c['a']],points[c['b']])]
    if k=='point-to-point':
        a,b=points[c['a']],points[c['b']];n=sub(b,a);require(norm(n)>1e-10,'E_DEGENERATE','Coincident alignment points underdetermine the crease.');return [canonical(n,dot(n,scale(add(a,b),.5)))]
    if k=='perpendicular-through':
        n=lines[c['line']]['normal'];nf=[-n[1],n[0]];return [canonical(nf,dot(nf,points[c['point']]))]
    if k=='line-to-line':
        a,b=lines[c['a']],lines[c['b']];answers=[]
        if norm(sub(a['normal'],b['normal']))<1e-10:
            require(abs(a['offsetMm']-b['offsetMm'])>1e-10,'E_DEGENERATE','Coincident lines do not define a unique fold.')
            return [canonical(a['normal'],(a['offsetMm']+b['offsetMm'])/2)]
        for sign in (1,-1):
            n=add(a['normal'],scale(b['normal'],sign));d=a['offsetMm']+sign*b['offsetMm']
            if norm(n)>1e-12:answers.append(canonical(n,d))
        return answers
    raise SpecError('E_SOLVER_UNSUPPORTED',f'Enumeration for {k} is not implemented by this reference helper. Supply and check a witness.')

def witness_residuals(c,w,points,lines):
    """Returns separate metric and angular residuals, never mixes millimeters and angles."""
    k=c['kind'];n=w['normal'];d=w['offsetMm'];r=lambda p:reflect_point(p,w)
    length=0.;angle=0.
    if k=='through-points':length=max(abs(dot(n,points[c[x]])-d) for x in ('a','b'))
    elif k=='point-to-point':length=norm(sub(r(points[c['a']]),points[c['b']]))
    elif k=='line-to-line':
        a,b=lines[c['a']],lines[c['b']];p=scale(a['normal'],a['offsetMm'])
        reflected_n=sub(a['normal'],scale(n,2*dot(n,a['normal'])))
        length=point_line_residual(r(p),b)
        angle=math.degrees(math.acos(min(1.,max(-1.,abs(dot(reflected_n,b['normal']))))))
    elif k=='perpendicular-through':
        length=abs(dot(n,points[c['point']])-d)
        angle=math.degrees(math.asin(min(1.,abs(dot(n,lines[c['line']]['normal'])))))
    elif k=='point-to-line-through':length=max(point_line_residual(r(points[c['point']]),lines[c['line']]),abs(dot(n,points[c['through']])-d))
    elif k=='two-points-to-lines':length=max(point_line_residual(r(points[c['a']]),lines[c['lineA']]),point_line_residual(r(points[c['b']]),lines[c['lineB']]))
    elif k=='point-to-line-perpendicular':
        length=point_line_residual(r(points[c['point']]),lines[c['line']])
        angle=math.degrees(math.asin(min(1.,abs(dot(n,lines[c['perpendicularTo']]['normal'])))))
    else:raise SpecError('E_SOLVER_UNSUPPORTED','Unknown constraint.')
    return {'positionMm':length,'angularDeg':angle}

def choose(c,branch,points,lines,position_tolerance=1e-7,angle_tolerance=1e-5):
    if branch['mode']=='witness':
        w=canonical(branch['normal'],branch['offsetMm'])
        residual=witness_residuals(c,w,points,lines)
        require(residual['positionMm']<=position_tolerance and residual['angularDeg']<=angle_tolerance,
                'E_CONSTRAINT','Supplied crease does not satisfy alignment: '+str(residual))
        return w
    solutions=enumerate_solutions(c,points,lines)
    require(len(solutions)==1,'E_AMBIGUOUS','More than one crease satisfies the alignment; supply a witness.')
    return solutions[0]
