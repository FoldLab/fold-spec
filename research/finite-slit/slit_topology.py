"""Exploratory connectivity proof for an already conforming triangle mesh.
Not an authoring/compiler/renderer feature. Uses exact integer material IDs.
"""
from collections import defaultdict

def welded_corners(faces, slit):
    """Map (face, material point) to a deterministically chosen corner ID."""
    incident = defaultdict(list)
    parent = {(i, p): (i, p) for i, tri in enumerate(faces) for p in tri}
    for i, tri in enumerate(faces):
        for a,b in zip(tri, tri[1:]+tri[:1]):
            incident[frozenset((a,b))].append(i)
    if any(len(fs)>2 for fs in incident.values()):
        raise ValueError('non-manifold mesh')
    if not slit or any(len(incident[e]) != 2 for e in slit):
        raise ValueError('cut must follow internal edges')
    def root(k):
        while parent[k] != k:
            k = parent[k]
        return k
    for edge, fs in incident.items():
        if len(fs) != 2 or edge in slit:
            continue
        for p in edge:
            a,b = sorted(root((f, p)) for f in fs)
            parent[b] = a
    return {k: root(k) for k in parent}


def resolve_frontmost_layer(intended, patches):
    """Resolve one explicit material-layer ID across certified overlap patches.

    Each patch is (covering_ids, above_pairs), where (a, b) means a is
    above b in the same already-specified view direction. The caller must
    supply complete positive-length path coverage, split at order changes.
    This function does not derive or certify the patches from geometry.
    """
    seen = False
    for covering, above in patches:
        seen = True
        covering = set(covering)
        if intended not in covering:
            raise ValueError('selected layer does not cover the full path')
        edges = {layer: set() for layer in covering}
        for a, b in above:
            if a not in covering or b not in covering or a == b:
                raise ValueError('invalid local ordering witness')
            edges[a].add(b)
        # Check cycles everywhere, including below the intended layer.
        def reachable(start):
            pending = list(edges[start])
            visited = set()
            while pending:
                layer = pending.pop()
                if layer not in visited:
                    visited.add(layer)
                    pending.extend(edges[layer] - visited)
            return visited
        reach = {layer: reachable(layer) for layer in covering}
        if any(layer in reachable_layers for layer, reachable_layers in reach.items()):
            raise ValueError('cyclic local layer order')
        if any(intended in reach[layer] for layer in covering):
            raise ValueError('selected layer is hidden')
        if reach[intended] != covering - {intended}:
            raise ValueError('frontmost layer is ambiguous')
    if not seen:
        raise ValueError('missing overlap patches')
    return intended
