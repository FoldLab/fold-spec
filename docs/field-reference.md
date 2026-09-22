# Structural field reference

**Generated from `tools/schema_source.py` output.** Normative behavior and cross-field rules live in the [specification](../SPEC.md); this reference is not sufficient by itself to implement a player. Property names match JSON exactly. `Required` applies within its containing object, not to every document. No silent defaults are implied by optional properties. Referenced definitions and every discriminated variant are included below.

## Contents

- [document](#document)
- [localizedText](#localizedtext)
- [review](#review)
- [source](#source)
- [author](#author)
- [metadata](#metadata)
- [material](#material)
- [sheet](#sheet)
- [landmark](#landmark)
- [accessibility](#accessibility)
- [tactile](#tactile)
- [camera](#camera)
- [run](#run)
- [step](#step)
- [instructionGroup](#instructiongroup)
- [instructions](#instructions)
- [asset](#asset)
- [meshVertex](#meshvertex)
- [meshFace](#meshface)
- [mesh](#mesh)
- [layerHint](#layerhint)
- [localLayerRelation](#locallayerrelation)
- [keyframe](#keyframe)
- [crease](#crease)
- [sampledOperation](#sampledoperation)
- [hingeOperation](#hingeoperation)
- [rigidOperation](#rigidoperation)
- [operation](#operation)
- [geometry](#geometry)
- [constructionFrame](#constructionframe)
- [pointDefinition](#pointdefinition)
- [constraint](#constraint)
- [branch](#branch)
- [lineDefinition](#linedefinition)
- [point](#point)
- [line](#line)
- [regionDefinition](#regiondefinition)
- [region](#region)
- [intent](#intent)
- [partImport](#partimport)
- [authoring](#authoring)
- [cue](#cue)
- [rig](#rig)
- [flourish](#flourish)
- [stageKey](#stagekey)
- [paperResponse](#paperresponse)
- [stage](#stage)
- [presentation](#presentation)
- [narration](#narration)
- [history](#history)
- [print](#print)
- [extensionUse](#extensionuse)

## document

Structural validation only. Run the semantic validator; passing JSON Schema does not prove foldability.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `format` | yes | `"fold-spec"` |  |
| `specVersion` | yes | `"1.0.0-draft.1"` |  |
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `revision` | yes | `integer` | minimum: `1`; maximum: `2147483647` |
| `defaultLocale` | yes | `string` | minLength: `1`; maxLength: `64`; pattern: `^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$`; BCP 47 language tag, checked by the author; syntax subset enforced here. |
| `status` | yes | `"planned"`, `"instructions"`, `"partial"`, `"resolved"` |  |
| `metadata` | yes | `metadata` |  |
| `sheets` | yes | array of `sheet` | minItems: `1`; maxItems: `32` |
| `accessibility` | yes | `accessibility` |  |
| `instructions` | yes | `instructions` |  |
| `geometry` | no | `geometry` |  |
| `authoring` | no | `authoring` |  |
| `assets` | yes | array of `asset` | minItems: `0`; maxItems: `256` |
| `presentation` | no | `presentation` |  |
| `narration` | yes | array of `narration` | minItems: `0`; maxItems: `8192` |
| `history` | yes | array of `history` | minItems: `0`; maxItems: `32` |
| `print` | no | `print` |  |
| `extensions` | yes | array of `extensionUse` | minItems: `0`; maxItems: `64` |

Unlisted properties are rejected within this object.

## localizedText

Localized plain text. The document defaultLocale entry is required by semantic validation.

**Type:** localized string map.

minProperties: `1`; maxProperties: `64`; Localized plain text. The document defaultLocale entry is required by semantic validation.

Each member value: `string`. minLength: `1`; maxLength: `12000`

Member names: minLength: `1`; maxLength: `64`; pattern: `^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$`; BCP 47 language tag, checked by the author; syntax subset enforced here.

## review

A claim by an author, not a certification by the parser.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `status` | yes | `"draft"`, `"authored"`, `"tested"` |  |
| `evidence` | no | array of `string` | minItems: `0`; maxItems: `32` |

Unlisted properties are rejected within this object.

## source

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `title` | yes | `string` | minLength: `1`; maxLength: `300` |
| `url` | yes | `string` | minLength: `1`; maxLength: `2048`; pattern: `^https://[^\s]+$` |
| `accessed` | no | `string` | minLength: `1`; maxLength: `4096`; pattern: `^\d{4}-\d{2}-\d{2}$` |
| `rightsNote` | no | `string` | minLength: `1`; maxLength: `3000` |

Unlisted properties are rejected within this object.

## author

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `name` | yes | `string` | minLength: `1`; maxLength: `200` |
| `roles` | yes | array of `"design"`, `"instructions"`, `"geometry"`, `"translation"`, `"review"`, `"assets"` | minItems: `1`; maxItems: `6`; uniqueItems: `True` |

Unlisted properties are rejected within this object.

## metadata

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `title` | yes | `localizedText` |  |
| `summary` | yes | `localizedText` |  |
| `authors` | yes | array of `author` | minItems: `1`; maxItems: `32` |
| `license` | yes | `string` | minLength: `1`; maxLength: `160` |
| `rightsNote` | no | `localizedText` |  |
| `tags` | no | array of `string` | minItems: `0`; maxItems: `64`; uniqueItems: `True` |
| `categories` | no | array of `string` | minItems: `0`; maxItems: `16`; uniqueItems: `True` |
| `difficulty` | no | `"beginner"`, `"intermediate"`, `"advanced"`, `"unspecified"` |  |
| `sources` | yes | array of `source` | minItems: `0`; maxItems: `128` |

Unlisted properties are rejected within this object.

## material

Image UVs and patterns are anchored to original material coordinates, not generated faces.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `color` | yes | `string` | minLength: `1`; maxLength: `7`; pattern: `^#[0-9A-Fa-f]{6}$` |
| `roughness` | yes | `number` | minimum: `0`; maximum: `1` |
| `texture` | yes | `object` |  |
| `pattern` | no | `object` |  |
| `imageAsset` | no | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `uvTransform` | no | array of `number` | minItems: `6`; maxItems: `6` |

Unlisted properties are rejected within this object.

## sheet

One rectangular connected sheet. Centered material XY, +Z is original front.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `widthMm` | yes | `number` | minimum: `0.1`; maximum: `10000` |
| `heightMm` | yes | `number` | minimum: `0.1`; maximum: `10000` |
| `thicknessMm` | yes | `number` | minimum: `0`; maximum: `10` |
| `front` | yes | `material` |  |
| `back` | yes | `material` |  |

Unlisted properties are rejected within this object.

## landmark

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `sheet` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `name` | yes | `localizedText` |  |
| `description` | yes | `localizedText` |  |
| `uvMm` | no | array of `number` | minItems: `2`; maxItems: `2` |

Unlisted properties are rejected within this object.

## accessibility

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `referenceFrame` | yes | `"folder-table"` |  |
| `setup` | yes | array of `localizedText` | minItems: `1`; maxItems: `64` |
| `landmarks` | yes | array of `landmark` | minItems: `0`; maxItems: `1024` |
| `review` | yes | `review` |  |
| `limitations` | yes | array of `localizedText` | minItems: `0`; maxItems: `32` |

Unlisted properties are rejected within this object.

## tactile

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `orientation` | yes | `localizedText` |  |
| `locate` | yes | array of `localizedText` | minItems: `0`; maxItems: `32` |
| `check` | yes | array of `localizedText` | minItems: `0`; maxItems: `32` |
| `recovery` | yes | array of `localizedText` | minItems: `0`; maxItems: `32` |
| `landmarkIds` | yes | array of `string` | minItems: `0`; maxItems: `64`; uniqueItems: `True` |
| `review` | yes | `review` |  |

Unlisted properties are rejected within this object.

## camera

Vectors use the containing pose or stage frame; semantic validation rejects collinear view/up.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `projection` | yes | `"orthographic"`, `"perspective"` |  |
| `positionMm` | yes | array of `number` | minItems: `3`; maxItems: `3` |
| `targetMm` | yes | array of `number` | minItems: `3`; maxItems: `3` |
| `up` | yes | array of `number` | minItems: `3`; maxItems: `3` |
| `verticalSpanMm` | no | `number` | minimum: `0.1`; maximum: `100000` |
| `verticalFovDeg` | no | `number` | minimum: `1`; maximum: `170` |
| `transitionMs` | no | `integer` | minimum: `0`; maximum: `10000` |

Unlisted properties are rejected within this object.

## run

An increasing normalized interval of one geometric operation; ranges form a continuous partition.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `operation` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `from` | yes | `number` | minimum: `0`; maximum: `1` |
| `to` | yes | `number` | minimum: `0`; maximum: `1` |

Unlisted properties are rejected within this object.

## step

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `title` | yes | `localizedText` |  |
| `body` | yes | `localizedText` |  |
| `kind` | yes | `"setup"`, `"fold"`, `"unfold"`, `"turn-over"`, `"rotate"`, `"shape"`, `"check"`, `"decorate"`, `"assemble"` |  |
| `animation` | yes | `"resolved"`, `"not-authored"`, `"not-applicable"` |  |
| `runs` | yes | array of `run` | minItems: `0`; maxItems: `32` |
| `pauseAfterMs` | yes | `integer` | minimum: `0`; maximum: `600000` |
| `tactile` | yes | `tactile` |  |
| `sourceSteps` | no | array of `string` | minItems: `0`; maxItems: `64` |
| `camera` | no | `camera` |  |
| `narrationIds` | no | array of `string` | minItems: `0`; maxItems: `16`; uniqueItems: `True` |

Unlisted properties are rejected within this object.

## instructionGroup

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `title` | yes | `localizedText` |  |
| `stepIds` | yes | array of `string` | minItems: `1`; maxItems: `4096`; uniqueItems: `True` |

Unlisted properties are rejected within this object.

## instructions

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `steps` | yes | array of `step` | minItems: `0`; maxItems: `4096` |
| `groups` | yes | array of `instructionGroup` | minItems: `0`; maxItems: `512` |

Unlisted properties are rejected within this object.

## asset

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `path` | yes | `string` | minLength: `1`; maxLength: `240`; pattern: `^(?!/)(?!.*(?:^\|/)\.\.(?:/\|$))[A-Za-z0-9][A-Za-z0-9_./-]{0,239}$` |
| `mediaType` | yes | `"image/png"`, `"image/jpeg"`, `"image/webp"`, `"audio/mpeg"`, `"audio/ogg"`, `"audio/wav"`, `"application/json"`, `"text/plain"` |  |
| `byteLength` | yes | `integer` | minimum: `0`; maximum: `33554432` |
| `sha256` | yes | `string` | minLength: `1`; maxLength: `64`; pattern: `^[a-f0-9]{64}$`; Lowercase SHA-256 of the exact stored bytes. |
| `required` | yes | `boolean` |  |
| `role` | yes | `"background"`, `"paper-image"`, `"narration"`, `"library"`, `"evidence"`, `"source"` |  |
| `license` | yes | `string` | minLength: `1`; maxLength: `160` |
| `description` | no | `localizedText` |  |

Unlisted properties are rejected within this object.

## meshVertex

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `uvMm` | yes | array of `number` | minItems: `2`; maxItems: `2` |

Unlisted properties are rejected within this object.

## meshFace

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `vertices` | yes | array of `integer` | minItems: `3`; maxItems: `3`; uniqueItems: `True` |

Unlisted properties are rejected within this object.

## mesh

CCW triangles in material space covering the rectangle once; no cuts or disconnected patches in the core.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `sheet` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `vertices` | yes | array of `meshVertex` | minItems: `3`; maxItems: `65536` |
| `faces` | yes | array of `meshFace` | minItems: `1`; maxItems: `131072` |

Unlisted properties are rejected within this object.

## layerHint

Rendering-only coplanar priority, not a physical stacking certificate.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `axis` | yes | array of `number` | minItems: `3`; maxItems: `3` |
| `ranks` | yes | array of `integer` | minItems: `1`; maxItems: `131072` |

Unlisted properties are rejected within this object.

## localLayerRelation

First face is above second in +normal within the stated coplanar overlap patch at operation progress at.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `firstFace` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `secondFace` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `normal` | yes | array of `number` | minItems: `3`; maxItems: `3` |
| `planeOffsetMm` | yes | `number` | minimum: `-1000000.0`; maximum: `1000000.0` |
| `overlapMm` | yes | array of array of `number` | minItems: `3`; maxItems: `128` |
| `at` | yes | `number` | minimum: `0`; maximum: `1` |

Unlisted properties are rejected within this object.

## keyframe

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `at` | yes | `number` | minimum: `0`; maximum: `1` |
| `positionsMm` | yes | array of array of `number` | minItems: `3`; maxItems: `65536` |
| `layerHint` | no | `layerHint` |  |

Unlisted properties are rejected within this object.

## crease

Persistent material crease event. State bend angle and historical assignment are different data.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `sheet` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `segmentMm` | yes | array of array of `number` | minItems: `2`; maxItems: `2` |
| `assignment` | yes | `"mountain"`, `"valley"`, `"unassigned"`, `"reference"` |  |
| `establishedAt` | yes | `number` | minimum: `0`; maximum: `1` |

Unlisted properties are rejected within this object.

## sampledOperation

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `sheet` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `mesh` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `durationMs` | yes | `integer` | minimum: `1`; maximum: `600000` |
| `creases` | yes | array of `crease` | minItems: `0`; maxItems: `4096` |
| `layers` | yes | array of `localLayerRelation` | minItems: `0`; maxItems: `4096` |
| `kind` | yes | `"sampled"` |  |
| `keys` | yes | array of `keyframe` | minItems: `2`; maxItems: `4096` |
| `interpolation` | yes | `"linear"` |  |
| `maxRelativeEdgeError` | yes | `number` | minimum: `0`; maximum: `0.005` |

Unlisted properties are rejected within this object.

## hingeOperation

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `sheet` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `mesh` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `durationMs` | yes | `integer` | minimum: `1`; maximum: `600000` |
| `creases` | yes | array of `crease` | minItems: `0`; maxItems: `4096` |
| `layers` | yes | array of `localLayerRelation` | minItems: `0`; maxItems: `4096` |
| `kind` | yes | `"hinge"` |  |
| `startPositionsMm` | yes | array of array of `number` | minItems: `3`; maxItems: `65536` |
| `axisMm` | yes | array of array of `number` | minItems: `2`; maxItems: `2` |
| `movingFaces` | yes | array of `string` | minItems: `1`; maxItems: `131072`; uniqueItems: `True` |
| `angleDeg` | yes | `number` | minimum: `-180`; maximum: `180` |
| `easing` | yes | `"linear"`, `"smoothstep"` |  |
| `startLayerHint` | no | `layerHint` |  |
| `endLayerHint` | no | `layerHint` |  |

Unlisted properties are rejected within this object.

## rigidOperation

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `sheet` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `mesh` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `durationMs` | yes | `integer` | minimum: `1`; maximum: `600000` |
| `creases` | yes | array of `crease` | minItems: `0`; maxItems: `4096` |
| `layers` | yes | array of `localLayerRelation` | minItems: `0`; maxItems: `4096` |
| `kind` | yes | `"rigid"` |  |
| `startPositionsMm` | yes | array of array of `number` | minItems: `3`; maxItems: `65536` |
| `axisMm` | yes | array of array of `number` | minItems: `2`; maxItems: `2` |
| `angleDeg` | yes | `number` | minimum: `-360`; maximum: `360` |
| `translationMm` | yes | array of `number` | minItems: `3`; maxItems: `3` |
| `liftMm` | yes | `number` | minimum: `0`; maximum: `10000` |
| `easing` | yes | `"linear"`, `"smoothstep"` |  |

Unlisted properties are rejected within this object.

## operation

Exactly one of the following variants must match.

### operation — variant 1

`sampledOperation`


### operation — variant 2

`hingeOperation`


### operation — variant 3

`rigidOperation`



## geometry

Ordered resolved geometry. The reference validator checks continuity/topology/strain, not collision or physical usability.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `status` | yes | `"partial"`, `"complete"` |  |
| `meshes` | yes | array of `mesh` | minItems: `1`; maxItems: `4096` |
| `operations` | yes | array of `operation` | minItems: `1`; maxItems: `4096` |
| `tolerances` | yes | `object` |  |
| `review` | yes | `review` |  |
| `limitations` | yes | array of `localizedText` | minItems: `0`; maxItems: `64` |

Unlisted properties are rejected within this object.

## constructionFrame

Explicit coplanar construction frame after a named operation or initially. u and v are unit perpendicular vectors.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `sheet` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `afterOperation` | yes | `JSON value` |  |
| `originMm` | yes | array of `number` | minItems: `3`; maxItems: `3` |
| `u` | yes | array of `number` | minItems: `3`; maxItems: `3` |
| `v` | yes | array of `number` | minItems: `3`; maxItems: `3` |

Unlisted properties are rejected within this object.

## pointDefinition

Exactly one of the following variants must match.

### pointDefinition — material

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"material"` |  |
| `sheet` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `uvMm` | yes | array of `number` | minItems: `2`; maxItems: `2` |

Unlisted properties are rejected within this object.

### pointDefinition — literal

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"literal"` |  |
| `xyMm` | yes | array of `number` | minItems: `2`; maxItems: `2` |

Unlisted properties are rejected within this object.

### pointDefinition — midpoint

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"midpoint"` |  |
| `a` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `b` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.

### pointDefinition — ratio

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"ratio"` |  |
| `a` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `b` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `numerator` | yes | `integer` | minimum: `0`; maximum: `1000000` |
| `denominator` | yes | `integer` | minimum: `1`; maximum: `1000000` |

Unlisted properties are rejected within this object.

### pointDefinition — intersection

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"intersection"` |  |
| `a` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `b` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.


## constraint

Exactly one of the following variants must match.

### constraint — through-points

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"through-points"` |  |
| `a` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `b` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.

### constraint — point-to-point

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"point-to-point"` |  |
| `a` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `b` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.

### constraint — line-to-line

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"line-to-line"` |  |
| `a` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `b` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.

### constraint — perpendicular-through

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"perpendicular-through"` |  |
| `line` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `point` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.

### constraint — point-to-line-through

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"point-to-line-through"` |  |
| `point` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `line` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `through` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.

### constraint — two-points-to-lines

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"two-points-to-lines"` |  |
| `a` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `lineA` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `b` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `lineB` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.

### constraint — point-to-line-perpendicular

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"point-to-line-perpendicular"` |  |
| `point` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `line` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `perpendicularTo` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.


## branch

Exactly one of the following variants must match.

### branch — unique

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `mode` | yes | `"unique"` |  |

Unlisted properties are rejected within this object.

### branch — witness

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `mode` | yes | `"witness"` |  |
| `normal` | yes | array of `number` | minItems: `2`; maxItems: `2` |
| `offsetMm` | yes | `number` | minimum: `-1000000.0`; maximum: `1000000.0` |

Unlisted properties are rejected within this object.


## lineDefinition

Exactly one of the following variants must match.

### lineDefinition — through

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"through"` |  |
| `a` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `b` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.

### lineDefinition — perpendicular

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"perpendicular"` |  |
| `line` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `point` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.

### lineDefinition — angle

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"angle"` |  |
| `line` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `point` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `angleDeg` | yes | `number` | minimum: `-360`; maximum: `360` |

Unlisted properties are rejected within this object.

### lineDefinition — alignment

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"alignment"` |  |
| `constraint` | yes | `constraint` |  |
| `branch` | yes | `branch` |  |

Unlisted properties are rejected within this object.


## point

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `frame` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `definition` | yes | `pointDefinition` |  |

Unlisted properties are rejected within this object.

## line

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `frame` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `definition` | yes | `lineDefinition` |  |

Unlisted properties are rejected within this object.

## regionDefinition

Exactly one of the following variants must match.

### regionDefinition — polygon

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"polygon"` |  |
| `verticesMm` | yes | array of array of `number` | minItems: `3`; maxItems: `4096` |

Unlisted properties are rejected within this object.

### regionDefinition — half-plane

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"half-plane"` |  |
| `line` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `containsPoint` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.

### regionDefinition — union / intersection / difference / xor

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `kind` | yes | `"union"`, `"intersection"`, `"difference"`, `"xor"` |  |
| `a` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `b` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |

Unlisted properties are rejected within this object.


## region

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `sheet` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `frame` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `definition` | yes | `regionDefinition` |  |

Unlisted properties are rejected within this object.

## intent

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `sheet` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `crease` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `movingRegion` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `materialFilter` | no | array of array of array of `number` | minItems: `1`; maxItems: `128` |
| `rotationDeg` | yes | `number` | minimum: `-180`; maximum: `180` |
| `durationMs` | yes | `integer` | minimum: `1`; maximum: `600000` |
| `resolvedOperations` | yes | array of `string` | minItems: `0`; maxItems: `4096`; uniqueItems: `True` |
| `note` | no | `localizedText` |  |

Unlisted properties are rejected within this object.

## partImport

Pinned data-only library dependency. Expansion occurs before playback; no runtime imports.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `asset` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `part` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `sheet` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `parameters` | yes | object map |  |
| `expandedOperationIds` | yes | array of `string` | minItems: `0`; maxItems: `4096`; uniqueItems: `True` |

Unlisted properties are rejected within this object.

## authoring

Typed construction graph. No loops, network execution, or arbitrary expressions.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `frames` | yes | array of `constructionFrame` | minItems: `1`; maxItems: `4096` |
| `points` | yes | array of `point` | minItems: `0`; maxItems: `65536` |
| `lines` | yes | array of `line` | minItems: `0`; maxItems: `65536` |
| `regions` | yes | array of `region` | minItems: `0`; maxItems: `4096` |
| `intents` | yes | array of `intent` | minItems: `0`; maxItems: `4096` |
| `imports` | yes | array of `partImport` | minItems: `0`; maxItems: `256` |

Unlisted properties are rejected within this object.

## cue

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `operation` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `at` | yes | `number` | minimum: `0`; maximum: `1` |
| `label` | yes | `localizedText` |  |

Unlisted properties are rejected within this object.

## rig

A validated final-pose hinge with no face crossing the partition off its axis.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `kind` | yes | `"bilateral-hinge"` |  |
| `sheet` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `afterOperation` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `axisMm` | yes | array of array of `number` | minItems: `2`; maxItems: `2` |
| `partitionNormal` | yes | array of `number` | minItems: `3`; maxItems: `3` |

Unlisted properties are rejected within this object.

## flourish

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `status` | yes | `"proposed"`, `"resolved"` |  |
| `kind` | yes | `"none"`, `"tip"`, `"bow"`, `"turn"`, `"flutter"` |  |
| `durationMs` | yes | `integer` | minimum: `1`; maximum: `30000` |
| `cycles` | yes | `integer` | minimum: `1`; maximum: `12` |
| `amplitudeDeg` | yes | `number` | minimum: `0`; maximum: `45` |
| `axisMm` | no | array of array of `number` | minItems: `2`; maxItems: `2` |
| `rig` | no | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `description` | yes | `localizedText` |  |

Unlisted properties are rejected within this object.

## stageKey

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `at` | yes | `number` | minimum: `0`; maximum: `1` |
| `positionMm` | yes | array of `number` | minItems: `3`; maxItems: `3` |
| `rotationDeg` | yes | array of `number` | minItems: `3`; maxItems: `3` |

Unlisted properties are rejected within this object.

## paperResponse

Art-directed presentation only; never changes canonical endpoints or implies calibrated elasticity.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `enabled` | yes | `boolean` |  |
| `bendWidthMm` | yes | `number` | minimum: `0`; maximum: `8` |
| `settleDeg` | yes | `number` | minimum: `0`; maximum: `4` |
| `damping` | yes | `number` | minimum: `2`; maximum: `12` |
| `cycles` | yes | `number` | minimum: `1`; maximum: `3` |

Unlisted properties are rejected within this object.

## stage

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `backgroundAsset` | no | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `keys` | yes | array of `stageKey` | minItems: `2`; maxItems: `256` |
| `modelScale` | yes | `number` | minimum: `0.1`; maximum: `3` |
| `camera` | yes | `camera` |  |
| `paperResponse` | no | `paperResponse` |  |

Unlisted properties are rejected within this object.

## presentation

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `status` | yes | `"proposed"`, `"resolved"` |  |
| `finishingStepIds` | yes | array of `string` | minItems: `0`; maxItems: `128`; uniqueItems: `True` |
| `display` | yes | `object` |  |
| `flourish` | yes | `flourish` |  |
| `rigs` | yes | array of `rig` | minItems: `0`; maxItems: `32` |
| `stage` | no | `stage` |  |

Unlisted properties are rejected within this object.

## narration

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `step` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `locale` | yes | `string` | minLength: `1`; maxLength: `64`; pattern: `^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$`; BCP 47 language tag, checked by the author; syntax subset enforced here. |
| `variant` | yes | `"primary"`, `"descriptive"` |  |
| `status` | yes | `"missing"`, `"ready"`, `"stale"` |  |
| `transcript` | yes | `string` | minLength: `1`; maxLength: `24000` |
| `textSha256` | yes | `string` | minLength: `1`; maxLength: `64`; pattern: `^[a-f0-9]{64}$`; Lowercase SHA-256 of the exact stored bytes. |
| `asset` | no | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `url` | no | `string` | minLength: `1`; maxLength: `2048`; pattern: `^https://[^\s]+$` |
| `durationMs` | no | `integer` | minimum: `1`; maximum: `3600000` |
| `pronunciations` | no | array of `object` | minItems: `0`; maxItems: `128` |

Unlisted properties are rejected within this object.

## history

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `128`; pattern: `^[A-Za-z][A-Za-z0-9_.:-]{0,127}$`; Case-sensitive identifier; stable within this document. |
| `scope` | yes | `"model"`, `"symbol"`, `"tradition"` |  |
| `title` | yes | `localizedText` |  |
| `summary` | yes | `localizedText` |  |
| `sourceIds` | yes | array of `string` | minItems: `1`; maxItems: `32`; uniqueItems: `True` |
| `review` | yes | `review` |  |
| `qualifications` | yes | array of `localizedText` | minItems: `0`; maxItems: `32` |

Unlisted properties are rejected within this object.

## print

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `includeFinalPanel` | yes | `boolean` |  |
| `includeHistory` | yes | `boolean` |  |
| `template` | no | `object` |  |
| `panels` | yes | array of `object` | minItems: `0`; maxItems: `4096` |

Unlisted properties are rejected within this object.

## extensionUse

Unknown required capabilities fail at the relevant profile boundary; no plugin code.

| Field | Required | Structural type | Bounds / description |
|---|---|---|---|
| `id` | yes | `string` | minLength: `1`; maxLength: `200`; pattern: `^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+:[a-z][a-z0-9-]*$` |
| `version` | yes | `string` | minLength: `1`; maxLength: `40`; pattern: `^\d+\.\d+\.\d+$` |
| `requiredFor` | yes | array of `"text"`, `"authoring"`, `"playback"`, `"presentation"`, `"print"` | minItems: `0`; maxItems: `5`; uniqueItems: `True` |
| `data` | yes | `object` |  |

Unlisted properties are rejected within this object.

## Cross-field checks

Refer to [conformance](../spec/00-status-and-conformance.md), [resolved geometry](../spec/06-resolved-geometry.md), [accessibility](../spec/09-accessibility-and-text-only.md), and [security](../spec/18-security-resource-policy-and-privacy.md) for rules a structural schema cannot prove.
