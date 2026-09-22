"""Small, non-executing Fold Source parser. Produces the normative document AST.
The declaration grammar is intentionally finite; it is not a scripting language.
"""
from __future__ import annotations
import json
import re
from dataclasses import dataclass
from foldspec import SpecError, VERSION, _pairs, _reject_constant, check_tree

@dataclass
class Number:
    value: float
    unit: str = ''

@dataclass
class Call:
    name: str
    args: list

class Parser:
    def __init__(self, text: str):
        self.text=text;self.pos=0
    def fail(self,msg):
        line=self.text.count('\n',0,self.pos)+1
        raise SpecError('E_SOURCE',msg,f'line {line}')
    def ws(self):
        while True:
            m=re.match(r'\s+|//[^\n]*(?:\n|$)',self.text[self.pos:])
            if not m:break
            self.pos+=len(m[0])
    def take(self,word):
        self.ws()
        if not self.text.startswith(word,self.pos):self.fail(f'Expected {word!r}.')
        end=self.pos+len(word)
        if re.fullmatch(r'[A-Za-z][A-Za-z-]*',word) and end<len(self.text) and re.match(r'[A-Za-z0-9_.:-]',self.text[end]):self.fail('Keyword must end at a token boundary.')
        self.pos=end
    def identifier(self):
        self.ws();m=re.match(r'[A-Za-z][A-Za-z0-9_.:-]*',self.text[self.pos:])
        if not m:self.fail('Expected an identifier.')
        self.pos+=len(m[0]);return m[0]
    def raw_json(self):
        self.ws()
        try:value,end=json.JSONDecoder(object_pairs_hook=_pairs,parse_constant=_reject_constant).raw_decode(self.text[self.pos:])
        except json.JSONDecodeError as exc:self.fail(str(exc))
        self.pos+=end;check_tree(value);return value
    def term(self):
        self.ws()
        if self.pos==len(self.text):self.fail('Unexpected end of source.')
        ch=self.text[self.pos]
        if ch in '[{"':return self.raw_json()
        m=re.match(r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?(?:mm|deg|ms)?',self.text[self.pos:])
        if m:
            self.pos+=len(m[0]);u=re.search(r'(mm|deg|ms)$',m[0]);unit=u[0] if u else '';n=m[0][:-len(unit)] if unit else m[0];return Number(float(n),unit)
        name=self.identifier();self.ws()
        if self.text[self.pos:self.pos+1]!='(':return name
        self.pos+=1;args=[];self.ws()
        if self.text[self.pos:self.pos+1]!=')':
            while True:
                args.append(self.term());self.ws()
                if self.text[self.pos:self.pos+1]!=',':break
                self.pos+=1
        self.take(')');return Call(name,args)
    def field_block(self,name):
        value=self.raw_json()
        if not isinstance(value,dict):self.fail('Declaration block must be a JSON object.')
        if 'id' in value:self.fail('A declaration block cannot override its declared id.')
        value={'id':name,**value};self.take(';');return value
    def parse(self):
        self.take('fold-source');version=self.raw_json();self.take(';')
        if version!=VERSION:self.fail('Unsupported Fold Source version.')
        self.take('document');d=self.raw_json();self.take(';')
        if not isinstance(d,dict):self.fail('document must be a JSON object.')
        if d.get('format')!='fold-spec' or d.get('specVersion')!=VERSION:self.fail('document format/version mismatch.')
        if 'authoring' in d:self.fail('Use authoring declarations, not an inline authoring field.')
        a={'frames':[],'points':[],'lines':[],'regions':[],'intents':[],'imports':[]}
        while True:
            self.ws()
            if self.pos==len(self.text):break
            kind=self.identifier();name=self.identifier()
            if kind=='frame':a['frames'].append(self.field_block(name))
            elif kind=='intent':a['intents'].append(self.field_block(name))
            elif kind=='use':a['imports'].append(self.field_block(name))
            elif kind=='step':d.setdefault('instructions',{'steps':[],'groups':[]})['steps'].append(self.field_block(name))
            elif kind in ('point','line'):
                self.take('in');frame=self.identifier();self.take('=');call=self.term();self.take(';');a[kind+'s'].append({'id':name,'frame':frame,'definition':definition(kind,call)})
            elif kind=='region':
                self.take('on');sheet=self.identifier();self.take('in');frame=self.identifier();self.take('=');call=self.term();self.take(';');a['regions'].append({'id':name,'sheet':sheet,'frame':frame,'definition':definition(kind,call)})
            else:self.fail('Unknown declaration kind '+kind)
        if any(a.values()):d['authoring']=a
        return d

def n(v,unit='',whole=False):
    if not isinstance(v,Number) or v.unit!=unit:raise SpecError('E_SOURCE_TYPE',f'Expected a number with {unit or "no"} unit.')
    if whole and not v.value.is_integer():raise SpecError('E_SOURCE_TYPE','Expected integer.')
    return int(v.value) if whole else v.value

def ident(v):
    if not isinstance(v,str):raise SpecError('E_SOURCE_TYPE','Expected a reference identifier.')
    return v

def count(call,lo,hi=None):
    if not isinstance(call,Call) or not lo<=len(call.args)<=(lo if hi is None else hi):raise SpecError('E_SOURCE_TYPE','Invalid function or argument count.')

def branch(v=None):
    if v is None:return {'mode':'unique'}
    count(v,3)
    if v.name!='witness':raise SpecError('E_SOURCE_TYPE','Expected witness(nx, ny, offsetMm).')
    return {'mode':'witness','normal':[n(v.args[0]),n(v.args[1])],'offsetMm':n(v.args[2],'mm')}

def definition(kind,call):
    if not isinstance(call,Call):raise SpecError('E_SOURCE_TYPE','A construction function is required.')
    f=call.name;a=call.args
    if kind=='point':
        if f=='material':count(call,3);return {'kind':'material','sheet':ident(a[0]),'uvMm':[n(a[1],'mm'),n(a[2],'mm')]}
        if f=='literal':count(call,2);return {'kind':'literal','xyMm':[n(a[0],'mm'),n(a[1],'mm')]}
        if f in ('midpoint','intersection'):count(call,2);return {'kind':f,'a':ident(a[0]),'b':ident(a[1])}
        if f=='ratio':count(call,4);return {'kind':'ratio','a':ident(a[0]),'b':ident(a[1]),'numerator':n(a[2],whole=True),'denominator':n(a[3],whole=True)}
    if kind=='line':
        if f=='through':count(call,2);return {'kind':'through','a':ident(a[0]),'b':ident(a[1])}
        if f=='perpendicular':count(call,2);return {'kind':'perpendicular','line':ident(a[0]),'point':ident(a[1])}
        if f=='angle':count(call,3);return {'kind':'angle','line':ident(a[0]),'point':ident(a[1]),'angleDeg':n(a[2],'deg')}
        functions={'align-points':('point-to-point',['a','b']),'align-lines':('line-to-line',['a','b']),'crease-through':('through-points',['a','b']),'crease-perpendicular':('perpendicular-through',['line','point']),'point-to-line-through':('point-to-line-through',['point','line','through']),'two-points-to-lines':('two-points-to-lines',['a','lineA','b','lineB']),'point-to-line-perpendicular':('point-to-line-perpendicular',['point','line','perpendicularTo'])}
        if f in functions:
            typ,fields=functions[f];count(call,len(fields),len(fields)+1)
            c={'kind':typ,**{k:ident(v) for k,v in zip(fields,a)}}
            return {'kind':'alignment','constraint':c,'branch':branch(a[-1] if len(a)>len(fields) else None)}
    if kind=='region':
        if f=='half-plane':count(call,2);return {'kind':'half-plane','line':ident(a[0]),'containsPoint':ident(a[1])}
        if f in ('union','intersection','difference','xor'):count(call,2);return {'kind':f,'a':ident(a[0]),'b':ident(a[1])}
        if f=='polygon':
            count(call,1)
            if not isinstance(a[0],list):raise SpecError('E_SOURCE_TYPE','polygon expects JSON coordinate pairs in millimeters.')
            return {'kind':'polygon','verticesMm':a[0]}
    raise SpecError('E_SOURCE_TYPE',f'Unknown {kind} construction {f}.')

def parse_source(text:str)->dict:
    if len(text.encode('utf-8'))>4*1024*1024:raise SpecError('E_LIMIT','Fold Source exceeds 4 MiB.')
    try:
        result = Parser(text).parse()
    except RecursionError as exc:
        raise SpecError('E_LIMIT', 'Fold Source nesting exceeds parser resource policy.') from exc
    check_tree(result)
    return result
