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
