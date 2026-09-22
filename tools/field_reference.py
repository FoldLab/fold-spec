#!/usr/bin/env python3
"""Generate structural documentation from the same schemas used by the validator.

This reference includes primitive definitions and discriminated variants, not just
objects with top-level properties. Cross-field interpretation remains in spec/.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def type_label(schema):
    if '$ref' in schema:
        return '`' + schema['$ref'].split('/')[-1] + '`'
    if 'const' in schema:
        return '`' + json.dumps(schema['const']) + '`'
    if 'enum' in schema:
        return ', '.join('`' + json.dumps(x) + '`' for x in schema['enum'])
    if 'oneOf' in schema:
        return 'one of: ' + ' / '.join(type_label(v) for v in schema['oneOf'])
    if schema.get('type') == 'array':
        return 'array of ' + type_label(schema.get('items', {}))
    if schema.get('type') == 'object' and ('propertyNames' in schema or 'patternProperties' in schema):
        return 'localized string map' if schema.get('additionalProperties', {}).get('type') == 'string' else 'object map'
    return '`' + str(schema.get('type', 'JSON value')) + '`'


def details(schema):
    limits = []
    for bound in ('minimum', 'exclusiveMinimum', 'maximum', 'exclusiveMaximum', 'minItems', 'maxItems',
                  'minLength', 'maxLength', 'minProperties', 'maxProperties', 'pattern', 'uniqueItems'):
        if bound in schema:
            limits.append(f'{bound}: `{schema[bound]}`')
    return '; '.join([*limits, schema.get('description', '')]).strip('; ')


def cell(text):
    return str(text).replace('|', '\\|').replace('\n', ' ')


def object_table(obj):
    out = ['| Field | Required | Structural type | Bounds / description |',
           '|---|---|---|---|']
    for name, value in obj['properties'].items():
        out.append('| `' + name + '` | ' + ('yes' if name in obj.get('required', []) else 'no') +
                   ' | ' + cell(type_label(value)) + ' | ' + cell(details(value)) + ' |')
    if obj.get('additionalProperties') is False:
        out += ['', 'Unlisted properties are rejected within this object.']
    return out


def render():
    schema = json.loads((ROOT / 'schemas/1.0.0-draft.1/document.schema.json').read_text())
    out = ['# Structural field reference', '',
           '**Generated from `tools/schema_source.py` output.** Normative behavior and cross-field rules '
           'live in the [specification](../SPEC.md); this reference is not sufficient by itself to '
           'implement a player. Property names match JSON exactly. `Required` applies within its '
           'containing object, not to every document. No silent defaults are implied by optional '
           'properties. Referenced definitions and every discriminated variant are included below.',
           '', '## Contents', '']
    definitions = {'document': schema, **schema['$defs']}
    for name in definitions:
        out.append(f'- [{name}](#{name.lower()})')
    for name, obj in definitions.items():
        out += ['', f'## {name}', '']
        if obj.get('description'):
            out += [obj['description'], '']
        if 'properties' in obj:
            out += object_table(obj)
        elif 'oneOf' in obj:
            out += ['Exactly one of the following variants must match.', '']
            for number, variant in enumerate(obj['oneOf'], 1):
                props = variant.get('properties', {})
                kind = props.get('kind', props.get('mode', {}))
                label = kind.get('const', kind.get('enum', f'variant {number}'))
                if isinstance(label, list):
                    label = ' / '.join(label)
                out += [f'### {name} — {label}', '']
                if variant.get('description'):
                    out += [variant['description'], '']
                if 'properties' in variant:
                    out += object_table(variant)
                else:
                    out += [type_label(variant), details(variant)]
                out.append('')
        else:
            out += [f'**Type:** {type_label(obj)}.', '', details(obj)]
            if 'additionalProperties' in obj:
                value = obj['additionalProperties']
                if isinstance(value, dict):
                    out += ['', f'Each member value: {type_label(value)}. {details(value)}']
            if 'propertyNames' in obj:
                out += ['', 'Member names: ' + details(obj['propertyNames'])]
    out += ['', '## Cross-field checks', '',
            'Refer to [conformance](../spec/00-status-and-conformance.md), '
            '[resolved geometry](../spec/06-resolved-geometry.md), '
            '[accessibility](../spec/09-accessibility-and-text-only.md), and '
            '[security](../spec/18-security-resource-policy-and-privacy.md) for rules a structural '
            'schema cannot prove.', '']
    return '\n'.join(out)


if __name__ == '__main__':
    target = ROOT / 'docs/field-reference.md'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(), encoding='utf-8')
    print(target)
