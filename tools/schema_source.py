"""Rebuild the versioned schemas from their source definitions. Python 3.10+."""
from pathlib import Path
import json
import argparse
_parser=argparse.ArgumentParser(description=__doc__)
_parser.add_argument('--output-root', type=Path, default=Path(__file__).resolve().parents[1])
R=_parser.parse_args().output_root
V='1.0.0-draft.1'
BASE=f'https://fold-spec.example/schemas/{V}/'
D={}
def ref(n):return {'$ref':'#/$defs/'+n}
def string(desc='',pattern=None,maxLength=4096,minLength=1):
 d={'type':'string','minLength':minLength,'maxLength':maxLength}
 if desc:d['description']=desc
 if pattern:d['pattern']=pattern
 return d
def num(a=None,b=None,desc=''):
 d={'type':'number'}
 if a is not None:d['minimum']=a
 if b is not None:d['maximum']=b
 if desc:d['description']=desc
 return d
def integer(a=0,b=1000000):return {'type':'integer','minimum':a,'maximum':b}
def enum(*values):return {'enum':list(values)}
def arr(item,mi=0,ma=4096,unique=False):
 d={'type':'array','items':item,'minItems':mi,'maxItems':ma}
 if unique:d['uniqueItems']=True
 return d
def vec(n,a=-1e6,b=1e6):return arr(num(a,b),n,n)
def obj(p,required=None,desc=''):
 d={'type':'object','properties':p,'required':list(p) if required is None else required,'additionalProperties':False}
 if desc:d['description']=desc
 return d
ID=string('Case-sensitive identifier; stable within this document.',r'^[A-Za-z][A-Za-z0-9_.:-]{0,127}$',128)
LOC=string('BCP 47 language tag, checked by the author; syntax subset enforced here.',r'^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$',64)
SHA=string('Lowercase SHA-256 of the exact stored bytes.',r'^[a-f0-9]{64}$',64)
TEXT={'type':'object','minProperties':1,'maxProperties':64,'propertyNames':LOC,'additionalProperties':string(maxLength=12000),'description':'Localized plain text. The document defaultLocale entry is required by semantic validation.'}
D['localizedText']=TEXT
D['review']=obj({'status':enum('draft','authored','tested'),'evidence':arr(string(maxLength=2000),0,32)},['status'], 'A claim by an author, not a certification by the parser.')
D['source']=obj({'id':ID,'title':string(maxLength=300),'url':string(pattern=r'^https://[^\s]+$',maxLength=2048),'accessed':string(pattern=r'^\d{4}-\d{2}-\d{2}$'),'rightsNote':string(maxLength=3000)},['id','title','url'])
D['author']=obj({'name':string(maxLength=200),'roles':arr(enum('design','instructions','geometry','translation','review','assets'),1,6,True)},['name','roles'])
D['metadata']=obj({'title':ref('localizedText'),'summary':ref('localizedText'),'authors':arr(ref('author'),1,32),'license':string(maxLength=160),'rightsNote':ref('localizedText'),'tags':arr(string(maxLength=60),0,64,True),'categories':arr(string(maxLength=80),0,16,True),'difficulty':enum('beginner','intermediate','advanced','unspecified'),'sources':arr(ref('source'),0,128)},['title','summary','authors','license','sources'])
D['material']=obj({'color':string(pattern=r'^#[0-9A-Fa-f]{6}$',maxLength=7),'roughness':num(0,1),'texture':obj({'kind':enum('smooth','washi','kraft'),'strength':num(0,1),'seed':integer(0,4294967295),'scaleMm':num(.01,100)}),'pattern':obj({'kind':enum('none','waves','hemp-leaf','checks','linked-circles'),'ink':string(pattern=r'^#[0-9A-Fa-f]{6}$',maxLength=7),'opacity':num(0,1),'tileMm':num(.1,1000)}),'imageAsset':ID,'uvTransform':arr(num(-1e6,1e6),6,6)},['color','roughness','texture'], 'Image UVs and patterns are anchored to original material coordinates, not generated faces.')
D['sheet']=obj({'id':ID,'widthMm':num(.1,10000),'heightMm':num(.1,10000),'thicknessMm':num(0,10),'front':ref('material'),'back':ref('material')},desc='One rectangular connected sheet. Centered material XY, +Z is original front.')
D['landmark']=obj({'id':ID,'sheet':ID,'name':ref('localizedText'),'description':ref('localizedText'),'uvMm':vec(2)},['id','sheet','name','description'])
D['accessibility']=obj({'referenceFrame':{'const':'folder-table'},'setup':arr(ref('localizedText'),1,64),'landmarks':arr(ref('landmark'),0,1024),'review':ref('review'),'limitations':arr(ref('localizedText'),0,32)},['referenceFrame','setup','landmarks','review','limitations'])
D['tactile']=obj({'orientation':ref('localizedText'),'locate':arr(ref('localizedText'),0,32),'check':arr(ref('localizedText'),0,32),'recovery':arr(ref('localizedText'),0,32),'landmarkIds':arr(ID,0,64,True),'review':ref('review')},['orientation','locate','check','recovery','landmarkIds','review'])
D['camera']=obj({'projection':enum('orthographic','perspective'),'positionMm':vec(3),'targetMm':vec(3),'up':vec(3,-1,1),'verticalSpanMm':num(.1,100000),'verticalFovDeg':num(1,170),'transitionMs':integer(0,10000)},['projection','positionMm','targetMm','up'], 'Vectors use the containing pose or stage frame; semantic validation rejects collinear view/up.')
D['run']=obj({'operation':ID,'from':num(0,1),'to':num(0,1)},desc='An increasing normalized interval of one geometric operation; ranges form a continuous partition.')
D['step']=obj({'id':ID,'title':ref('localizedText'),'body':ref('localizedText'),'kind':enum('setup','fold','unfold','turn-over','rotate','shape','check','decorate','assemble'),'animation':enum('resolved','not-authored','not-applicable'),'runs':arr(ref('run'),0,32),'pauseAfterMs':integer(0,600000),'tactile':ref('tactile'),'sourceSteps':arr(string(maxLength=100),0,64),'camera':ref('camera'),'narrationIds':arr(ID,0,16,True)},['id','title','body','kind','animation','runs','pauseAfterMs','tactile'])
D['instructionGroup']=obj({'id':ID,'title':ref('localizedText'),'stepIds':arr(ID,1,4096,True)})
D['instructions']=obj({'steps':arr(ref('step'),0,4096),'groups':arr(ref('instructionGroup'),0,512)},['steps','groups'])
D['asset']=obj({'id':ID,'path':string(pattern=r'^(?!/)(?!.*(?:^|/)\.\.(?:/|$))[A-Za-z0-9][A-Za-z0-9_./-]{0,239}$',maxLength=240),'mediaType':enum('image/png','image/jpeg','image/webp','audio/mpeg','audio/ogg','audio/wav','application/json','text/plain'),'byteLength':integer(0,33554432),'sha256':SHA,'required':{'type':'boolean'},'role':enum('background','paper-image','narration','library','evidence','source'),'license':string(maxLength=160),'description':ref('localizedText')},['id','path','mediaType','byteLength','sha256','required','role','license'])
D['meshVertex']=obj({'id':ID,'uvMm':vec(2)})
D['meshFace']=obj({'id':ID,'vertices':arr(integer(0,65535),3,3,True)})
D['mesh']=obj({'id':ID,'sheet':ID,'vertices':arr(ref('meshVertex'),3,65536),'faces':arr(ref('meshFace'),1,131072)},desc='CCW triangles in material space covering the rectangle once; no cuts or disconnected patches in the core.')
D['layerHint']=obj({'axis':vec(3,-1,1),'ranks':arr(integer(-1000000,1000000),1,131072)},desc='Rendering-only coplanar priority, not a physical stacking certificate.')
D['localLayerRelation']=obj({'firstFace':ID,'secondFace':ID,'normal':vec(3,-1,1),'planeOffsetMm':num(-1e6,1e6),'overlapMm':arr(vec(2),3,128),'at':num(0,1)},desc='First face is above second in +normal within the stated coplanar overlap patch at operation progress at.')
D['keyframe']=obj({'at':num(0,1),'positionsMm':arr(vec(3),3,65536),'layerHint':ref('layerHint')},['at','positionsMm'])
D['crease']=obj({'id':ID,'sheet':ID,'segmentMm':arr(vec(2),2,2),'assignment':enum('mountain','valley','unassigned','reference'),'establishedAt':num(0,1)},desc='Persistent material crease event. State bend angle and historical assignment are different data.')
common={'id':ID,'sheet':ID,'mesh':ID,'durationMs':integer(1,600000),'creases':arr(ref('crease'),0,4096),'layers':arr(ref('localLayerRelation'),0,4096)}
D['sampledOperation']=obj({**common,'kind':{'const':'sampled'},'keys':arr(ref('keyframe'),2,4096),'interpolation':{'const':'linear'},'maxRelativeEdgeError':num(0,.005)},list(common)+['kind','keys','interpolation','maxRelativeEdgeError'])
D['hingeOperation']=obj({**common,'kind':{'const':'hinge'},'startPositionsMm':arr(vec(3),3,65536),'axisMm':arr(vec(3),2,2),'movingFaces':arr(ID,1,131072,True),'angleDeg':num(-180,180),'easing':enum('linear','smoothstep'),'startLayerHint':ref('layerHint'),'endLayerHint':ref('layerHint')},list(common)+['kind','startPositionsMm','axisMm','movingFaces','angleDeg','easing'])
D['rigidOperation']=obj({**common,'kind':{'const':'rigid'},'startPositionsMm':arr(vec(3),3,65536),'axisMm':arr(vec(3),2,2),'angleDeg':num(-360,360),'translationMm':vec(3),'liftMm':num(0,10000),'easing':enum('linear','smoothstep')},list(common)+['kind','startPositionsMm','axisMm','angleDeg','translationMm','liftMm','easing'])
D['operation']={'oneOf':[ref('sampledOperation'),ref('hingeOperation'),ref('rigidOperation')]}
D['geometry']=obj({'status':enum('partial','complete'),'meshes':arr(ref('mesh'),1,4096),'operations':arr(ref('operation'),1,4096),'tolerances':obj({'positionMm':num(1e-9,.01),'relativeEdge':num(0,.005),'angularDeg':num(1e-9,.01)}),'review':ref('review'),'limitations':arr(ref('localizedText'),0,64)},desc='Ordered resolved geometry. The reference validator checks continuity/topology/strain, not collision or physical usability.')
D['constructionFrame']=obj({'id':ID,'sheet':ID,'afterOperation':{'anyOf':[ID,{'type':'null'}]},'originMm':vec(3),'u':vec(3,-1,1),'v':vec(3,-1,1)},desc='Explicit coplanar construction frame after a named operation or initially. u and v are unit perpendicular vectors.')
D['pointDefinition']={'oneOf':[
 obj({'kind':{'const':'material'},'sheet':ID,'uvMm':vec(2)}),
 obj({'kind':{'const':'literal'},'xyMm':vec(2)}),
 obj({'kind':{'const':'midpoint'},'a':ID,'b':ID}),
 obj({'kind':{'const':'ratio'},'a':ID,'b':ID,'numerator':integer(0,1000000),'denominator':integer(1,1000000)}),
 obj({'kind':{'const':'intersection'},'a':ID,'b':ID})]}
D['constraint']={'oneOf':[
 obj({'kind':{'const':'through-points'},'a':ID,'b':ID}),
 obj({'kind':{'const':'point-to-point'},'a':ID,'b':ID}),
 obj({'kind':{'const':'line-to-line'},'a':ID,'b':ID}),
 obj({'kind':{'const':'perpendicular-through'},'line':ID,'point':ID}),
 obj({'kind':{'const':'point-to-line-through'},'point':ID,'line':ID,'through':ID}),
 obj({'kind':{'const':'two-points-to-lines'},'a':ID,'lineA':ID,'b':ID,'lineB':ID}),
 obj({'kind':{'const':'point-to-line-perpendicular'},'point':ID,'line':ID,'perpendicularTo':ID})]}
D['branch']={'oneOf':[obj({'mode':{'const':'unique'}}),obj({'mode':{'const':'witness'},'normal':vec(2,-1,1),'offsetMm':num(-1e6,1e6)})]}
D['lineDefinition']={'oneOf':[
 obj({'kind':{'const':'through'},'a':ID,'b':ID}),
 obj({'kind':{'const':'perpendicular'},'line':ID,'point':ID}),
 obj({'kind':{'const':'angle'},'line':ID,'point':ID,'angleDeg':num(-360,360)}),
 obj({'kind':{'const':'alignment'},'constraint':ref('constraint'),'branch':ref('branch')})]}
D['point']=obj({'id':ID,'frame':ID,'definition':ref('pointDefinition')})
D['line']=obj({'id':ID,'frame':ID,'definition':ref('lineDefinition')})
D['regionDefinition']={'oneOf':[
 obj({'kind':{'const':'polygon'},'verticesMm':arr(vec(2),3,4096)}),
 obj({'kind':{'const':'half-plane'},'line':ID,'containsPoint':ID}),
 obj({'kind':enum('union','intersection','difference','xor'),'a':ID,'b':ID})]}
D['region']=obj({'id':ID,'sheet':ID,'frame':ID,'definition':ref('regionDefinition')})
D['intent']=obj({'id':ID,'sheet':ID,'crease':ID,'movingRegion':ID,'materialFilter':arr(arr(vec(2),3,4096),1,128),'rotationDeg':num(-180,180),'durationMs':integer(1,600000),'resolvedOperations':arr(ID,0,4096,True),'note':ref('localizedText')},['id','sheet','crease','movingRegion','rotationDeg','durationMs','resolvedOperations'])
D['partImport']=obj({'id':ID,'asset':ID,'part':ID,'sheet':ID,'parameters':{'type':'object','propertyNames':ID,'additionalProperties':num(-1e6,1e6)},'expandedOperationIds':arr(ID,0,4096,True)},desc='Pinned data-only library dependency. Expansion occurs before playback; no runtime imports.')
D['authoring']=obj({'frames':arr(ref('constructionFrame'),1,4096),'points':arr(ref('point'),0,65536),'lines':arr(ref('line'),0,65536),'regions':arr(ref('region'),0,4096),'intents':arr(ref('intent'),0,4096),'imports':arr(ref('partImport'),0,256)},desc='Typed construction graph. No loops, network execution, or arbitrary expressions.')
D['cue']=obj({'operation':ID,'at':num(0,1),'label':ref('localizedText')})
D['rig']=obj({'id':ID,'kind':{'const':'bilateral-hinge'},'sheet':ID,'afterOperation':ID,'axisMm':arr(vec(3),2,2),'partitionNormal':vec(3,-1,1)},desc='A validated final-pose hinge with no face crossing the partition off its axis.')
D['flourish']=obj({'status':enum('proposed','resolved'),'kind':enum('none','tip','bow','turn','flutter'),'durationMs':integer(1,30000),'cycles':integer(1,12),'amplitudeDeg':num(0,45),'axisMm':arr(vec(3),2,2),'rig':ID,'description':ref('localizedText')},['status','kind','durationMs','cycles','amplitudeDeg','description'])
D['stageKey']=obj({'at':num(0,1),'positionMm':vec(3),'rotationDeg':vec(3,-360,360)})
D['paperResponse']=obj({'enabled':{'type':'boolean'},'bendWidthMm':num(0,8),'settleDeg':num(0,4),'damping':num(2,12),'cycles':num(1,3)},desc='Art-directed presentation only; never changes canonical endpoints or implies calibrated elasticity.')
D['stage']=obj({'backgroundAsset':ID,'keys':arr(ref('stageKey'),2,256),'modelScale':num(.1,3),'camera':ref('camera'),'paperResponse':ref('paperResponse')},['keys','modelScale','camera'])
D['presentation']=obj({'status':enum('proposed','resolved'),'finishingStepIds':arr(ID,0,128,True),'display':obj({'afterOperation':ID,'camera':ref('camera'),'orientation':ref('localizedText'),'checks':arr(ref('localizedText'),0,32)},['orientation','checks']),'flourish':ref('flourish'),'rigs':arr(ref('rig'),0,32),'stage':ref('stage')},['status','finishingStepIds','display','flourish','rigs'])
D['narration']=obj({'id':ID,'step':ID,'locale':LOC,'variant':enum('primary','descriptive'),'status':enum('missing','ready','stale'),'transcript':string(maxLength=24000),'textSha256':SHA,'asset':ID,'url':string(pattern=r'^https://[^\s]+$',maxLength=2048),'durationMs':integer(1,3600000),'pronunciations':arr(obj({'written':string(maxLength=200),'spoken':string(maxLength=300)}),0,128)},['id','step','locale','variant','status','transcript','textSha256'])
D['history']=obj({'id':ID,'scope':enum('model','symbol','tradition'),'title':ref('localizedText'),'summary':ref('localizedText'),'sourceIds':arr(ID,1,32,True),'review':ref('review'),'qualifications':arr(ref('localizedText'),0,32)},['id','scope','title','summary','sourceIds','review','qualifications'])
D['print']=obj({'includeFinalPanel':{'type':'boolean'},'includeHistory':{'type':'boolean'},'template':obj({'sizeMm':vec(2,.1,10000),'sides':enum('front','back','both'),'includePattern':{'type':'boolean'},'includeGuides':{'type':'boolean'},'guideConvention':{'const':'mountain-solid-valley-dashed'}}),'panels':arr(obj({'step':ID,'samples':arr(num(0,1),1,16,True),'camera':ref('camera')} ,['step','samples']),0,4096)},['includeFinalPanel','includeHistory','panels'])
D['extensionUse']=obj({'id':string(pattern=r'^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+:[a-z][a-z0-9-]*$',maxLength=200),'version':string(pattern=r'^\d+\.\d+\.\d+$',maxLength=40),'requiredFor':arr(enum('text','authoring','playback','presentation','print'),0,5,True),'data':{'type':'object'}},desc='Unknown required capabilities fail at the relevant profile boundary; no plugin code.')
props={'format':{'const':'fold-spec'},'specVersion':{'const':V},'id':ID,'revision':integer(1,2147483647),'defaultLocale':LOC,'status':enum('planned','instructions','partial','resolved'),'metadata':ref('metadata'),'sheets':arr(ref('sheet'),1,32),'accessibility':ref('accessibility'),'instructions':ref('instructions'),'geometry':ref('geometry'),'authoring':ref('authoring'),'assets':arr(ref('asset'),0,256),'presentation':ref('presentation'),'narration':arr(ref('narration'),0,8192),'history':arr(ref('history'),0,32),'print':ref('print'),'extensions':arr(ref('extensionUse'),0,64)}
root=obj(props,['format','specVersion','id','revision','defaultLocale','status','metadata','sheets','accessibility','instructions','assets','narration','history','extensions'])
root={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':BASE+'document.schema.json','title':'Fold Spec document — '+V,'description':'Structural validation only. Run the semantic validator; passing JSON Schema does not prove foldability.',**root,'$defs':D}
root['allOf']=[
 {'if':{'properties':{'status':{'const':'resolved'}}},'then':{'required':['geometry'],'properties':{'geometry':{'properties':{'status':{'const':'complete'}}}}}},
 {'if':{'properties':{'status':{'const':'partial'}}},'then':{'required':['geometry'],'properties':{'geometry':{'properties':{'status':{'const':'partial'}}}}}},
 {'if':{'properties':{'status':{'enum':['planned','instructions']}}},'then':{'not':{'required':['geometry']}}},
 {'if':{'properties':{'status':{'const':'planned'}}},'then':{'properties':{'instructions':{'properties':{'steps':{'maxItems':0}}}}},'else':{'properties':{'instructions':{'properties':{'steps':{'minItems':1}}}}}}
]
p=R/'schemas'/V;p.mkdir(parents=True,exist_ok=True)
def write(name,d): (p/name).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
write('document.schema.json',root)
entry=obj({'path':string(pattern=r'^[A-Za-z0-9][A-Za-z0-9_./-]{0,239}$',maxLength=240),'byteLength':integer(0,33554432),'sha256':SHA})
manifest={'$schema':root['$schema'],'$id':BASE+'manifest.schema.json','title':'Fold Spec package manifest',**obj({'format':{'const':'fold-spec-package'},'specVersion':{'const':V},'document':{'const':'document.json'},'entries':arr(entry,1,257)})}
write('manifest.schema.json',manifest)
scene={'$schema':root['$schema'],'$id':BASE+'scene.schema.json','title':'Fold Spec reusable presentation scene',**obj({'format':{'const':'fold-spec-scene'},'specVersion':{'const':V},'id':ID,'stage':ref('stage'),'assets':arr(ref('asset'),0,256),'license':string(maxLength=160)}),'$defs':D}
write('scene.schema.json',scene)
part=obj({'id':ID,'description':ref('localizedText'),'sheetSlot':ID,'bindings':arr(obj({'parameter':ID,'pointer':string(pattern=r'^/(?:[A-Za-z0-9_.:-]+/)*[A-Za-z0-9_.:-]+$',maxLength=500),'factor':num(-1000,1000)}),0,1024),'parameters':arr(obj({'id':ID,'minimum':num(-1e6,1e6),'maximum':num(-1e6,1e6),'default':num(-1e6,1e6)}),0,32),'authoring':ref('authoring'),'exports':arr(ID,1,128,True)})
library={'$schema':root['$schema'],'$id':BASE+'library.schema.json','title':'Fold Spec authoring library',**obj({'format':{'const':'fold-spec-library'},'specVersion':{'const':V},'id':ID,'revision':integer(1,2147483647),'license':string(maxLength=160),'parts':arr(part,1,128)}),'$defs':D}
write('library.schema.json',library)
