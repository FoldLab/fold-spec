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


def derive_overlap_patches(start, stop, polygons, witnesses):
    """Exact positive-length path partition for strict-convex coplanar fixtures.

    Points are integer (x,y,z) in one orthographic frame. Witnesses are
    (above, below, begin_t, end_t) for explicit rational path intervals.
    Not a geometric proof of physical order or material lineage.
    """
    from fractions import Fraction
    from itertools import pairwise

    def integer_point(p):
        if len(p) != 3 or any(type(n) is not int for n in p):
            raise ValueError('expected integer xyz coordinates')
    def orient(a, b, p):
        return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])

    integer_point(start)
    integer_point(stop)
    if start[2] != stop[2] or start == stop or not polygons:
        raise ValueError('invalid slit or plane')
    limits = {Fraction(0), Fraction(1)}
    coverage = {}
    for region, vertices in polygons.items():
        if len(vertices) < 3 or len(set(vertices)) != len(vertices):
            raise ValueError('invalid polygon')
        for p in vertices:
            integer_point(p)
        if any(p[2] != start[2] for p in vertices):
            raise ValueError('noncoplanar region')
        edges = list(zip(vertices, vertices[1:]+vertices[:1]))
        sign = 1 if orient(*edges[0], vertices[2]) > 0 else -1
        if any(sign*orient(a,b,p) <= 0 for a,b in edges for p in vertices if p not in (a,b)):
            raise ValueError('polygon must be strictly convex and ordered')
        lo, hi = Fraction(0), Fraction(1)
        on_edge_line = False
        for a,b in edges:
            v = sign*orient(a,b,start)
            d = sign*orient(a,b,stop) - v
            if d > 0:
                lo = max(lo, Fraction(-v,d))
            elif d < 0:
                hi = min(hi, Fraction(-v,d))
            elif v < 0:
                hi = Fraction(-1)
            elif v == 0:
                on_edge_line = True
        if lo > hi:
            continue
        if lo == hi or on_edge_line:
            raise ValueError('ambiguous boundary contact')
        coverage[region] = lo, hi
        limits.update((lo,hi))

    orders = []
    for a,b,lo,hi in witnesses:
        if any(type(t) not in (int,Fraction) for t in (lo,hi)) or not 0 <= lo < hi <= 1:
            raise ValueError('invalid witness interval')
        if any(region not in coverage or not coverage[region][0] <= lo < hi <= coverage[region][1]
               for region in (a,b)) or a == b:
            raise ValueError('witness outside geometric co-coverage')
        orders.append((a,b,lo,hi))
        limits.update((lo,hi))

    patches = []
    for lo,hi in pairwise(sorted(limits)):
        covering = {region for region,(a,b) in coverage.items() if a <= lo < hi <= b}
        above = [(a,b) for a,b,s,t in orders if s <= lo < hi <= t]
        patches.append((covering, above))
    return patches


def remesh_single_triangle_slit(faces, points, selected, mouth_edge, mouth, tip):
    """Insert a real edge-chain for one slit contained in one triangle.

    Points map material IDs to exact 2D coordinates. Input is assumed to
    be a conforming consistently wound coplanar material mesh. Returns
    copied mesh, copied coordinates and the internal cut-edge set.
    """
    from fractions import Fraction

    def orient(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

    def valid_point(p):
        return len(p) == 2 and all(type(v) in (int,Fraction) for v in p)

    if type(selected) is not int or not 0 <= selected < len(faces):
        raise ValueError('invalid selected triangle')
    f = tuple(faces[selected])
    if len(f) != 3 or len(set(f)) != 3 or not all(v in points for v in f):
        raise ValueError('invalid selected triangle')
    if any(not valid_point(p) for p in (*[points[v] for v in f], mouth, tip)):
        raise ValueError('expected exact material coordinates')
    edges = list(zip(f,f[1:]+f[:1]))
    key = frozenset(mouth_edge)
    matches = [i for i, edge in enumerate(edges) if frozenset(edge) == key]
    if len(matches) != 1 or sum(key <= set(tri) for tri in faces) != 1:
        raise ValueError('mouth edge must be free in the complete mesh')

    i = matches[0]
    a,b,c = f[i:]+f[:i]
    pa,pb,pc = (points[v] for v in (a,b,c))
    parent_area = orient(pa,pb,pc)
    if not parent_area or orient(pa,pb,mouth) or sum((v-x)*(v-y) for v,x,y in zip(mouth,pa,pb)) >= 0:
        raise ValueError('mouth must lie strictly within the free edge')
    if any(parent_area*orient(points[x],points[y],tip) <= 0 for x,y in edges):
        raise ValueError('tip must lie strictly inside the selected triangle')

    if any(type(v) is not int for v in points):
        raise ValueError('expected integer material IDs')
    m = max(points)+1
    t = m+1
    coords = {**points, m:tuple(mouth), t:tuple(tip)}
    replacement = [(a,m,t),(m,b,t),(b,c,t),(c,a,t)]
    areas = [orient(*(coords[v] for v in tri)) for tri in replacement]
    if sum(areas) != parent_area or any(x*parent_area <= 0 for x in areas):
        raise ValueError('remesh failed signed-area invariant')
    new_faces = list(faces[:selected]) + replacement + list(faces[selected+1:])
    cut = {frozenset((m,t))}
    # Exercise the connectivity contract, including the two banks and tip.
    welds = welded_corners(new_faces, cut)
    if welds[selected,m] == welds[selected+1,m] or len({welds[i,t] for i in range(selected,selected+4)}) != 1:
        raise ValueError('remesh failed slit connectivity invariant')
    return new_faces, coords, cut


def remesh_triangle_chain_slit(faces, points, chain, mouth_edge, mouth, tip):
    """Remesh a declared simple triangle chain in one material plane.

    Only transverse interior-of-edge crossings are accepted. Layer
    resolution and global mesh conformance remain caller obligations.
    Returns (faces, coordinates, cut edges, source triangle indices).
    """
    from fractions import Fraction
    from itertools import pairwise

    def valid_point(p):
        return len(p) == 2 and all(type(x) in (int, Fraction) for x in p)

    def minus(a,b):
        return a[0]-b[0], a[1]-b[1]

    def cross(a,b):
        return a[0]*b[1]-a[1]*b[0]

    def orient(a,b,c):
        return cross(minus(b,a),minus(c,a))

    def edges(face):
        return list(zip(face,face[1:]+face[:1]))

    if (not chain or any(type(i) is not int or not 0 <= i < len(faces) for i in chain)
            or len(set(chain)) != len(chain)):
        raise ValueError('invalid triangle chain')
    if (any(type(v) is not int or not valid_point(p) for v,p in points.items())
            or not valid_point(mouth) or not valid_point(tip) or mouth == tip):
        raise ValueError('invalid exact material coordinates')

    incident = defaultdict(list)
    for i, f in enumerate(faces):
        if len(f) != 3 or len(set(f)) != 3 or any(v not in points for v in f):
            raise ValueError('invalid triangular mesh')
        if not orient(*(points[v] for v in f)):
            raise ValueError('degenerate triangle')
        for a,b in edges(f):
            incident[frozenset((a,b))].append((i,a,b))
    if any(len(v)>2 or (len(v)==2 and v[0][1:] != v[1][1:][::-1])
           for v in incident.values()):
        raise ValueError('non-manifold or inconsistent mesh winding')

    def interior_of_edge(p, a, b):
        return not orient(a,b,p) and sum(x*y for x,y in zip(minus(p,a),minus(p,b))) < 0

    mouth_key = frozenset(mouth_edge)
    first = incident.get(mouth_key, [])
    if len(first)!=1 or first[0][0]!=chain[0] or not interior_of_edge(mouth,*(points[v] for v in first[0][1:])):
        raise ValueError('mouth must enter a free edge interior')
    last = faces[chain[-1]]
    area = orient(*(points[v] for v in last))
    if any(area * orient(points[a],points[b],tip) <= 0 for a,b in edges(last)):
        raise ValueError('tip must lie strictly inside terminal triangle')

    coords = dict(points)
    next_id = max(coords)+1
    coords[next_id] = tuple(mouth)
    junctions = [(mouth_key,next_id)]
    direction = minus(tip,mouth)
    last_t = Fraction(0)
    for i,j in pairwise(chain):
        shared = frozenset(set(faces[i]) & set(faces[j]))
        if len(shared)!=2 or len(incident.get(shared,[]))!=2 or shared==junctions[-1][0]:
            raise ValueError('chain must cross a shared edge once')
        a,b = [points[v] for v in sorted(shared)]
        e = minus(b,a)
        den = cross(direction,e)
        if not den:
            raise ValueError('shared edge must be crossed transversely')
        t = Fraction(cross(minus(a,mouth),e),den)
        u = Fraction(cross(minus(a,mouth),direction),den)
        if not (last_t < t < 1 and 0 < u < 1):
            raise ValueError('shared-edge crossing must be ordered and interior')
        last_t = t
        next_id += 1
        coords[next_id] = tuple(x+t*d for x,d in zip(mouth,direction))
        junctions.append((shared,next_id))
    next_id += 1
    coords[next_id] = tuple(tip)
    junctions.append((None,next_id))

    replacement = {}
    cut = set()
    for k,i in enumerate(chain):
        entry,a = junctions[k]
        exit,b = junctions[k+1]
        cut.add(frozenset((a,b)))
        boundary = []
        for x,y in edges(faces[i]):
            boundary.append(x)
            edge = frozenset((x,y))
            if edge==entry:
                boundary.append(a)
            if edge==exit:
                boundary.append(b)
        if exit is None:
            tris = [(x,y,b) for x,y in edges(boundary)]
        else:
            # Build each bank polygon in the original winding; the inserted
            # vertices on distinct edges make each bank strictly convex.
            s = boundary.index(a)
            boundary = boundary[s:]+boundary[:s]
            t = boundary.index(b)
            banks = (boundary[:t+1],[*boundary[t:],a])
            tris = [(bank[0],x,y) for bank in banks for x,y in pairwise(bank[1:])]
        before = orient(*(coords[v] for v in faces[i]))
        after = [orient(*(coords[v] for v in f)) for f in tris]
        if sum(after)!=before or any(v*before <= 0 for v in after):
            raise ValueError('chain remesh violated signed area')
        replacement[i] = tris

    output, lineage = [], []
    for i,f in enumerate(faces):
        part = replacement.get(i,[f])
        output.extend(part)
        lineage.extend([i]*len(part))
    # Compare incidence globally: only mouth/chain crossing edges were split;
    # every new interior edge must have two incident triangles.
    counts = defaultdict(int)
    for f in output:
        for a,b in edges(f):
            counts[frozenset((a,b))] += 1
    expected_boundary = {e for e,uses in incident.items() if len(uses)==1}
    expected_boundary.remove(mouth_key)
    expected_boundary.update(frozenset((v,junctions[0][1])) for v in mouth_key)
    if {e for e,n in counts.items() if n==1} != expected_boundary or any(n>2 for n in counts.values()):
        raise ValueError('chain remesh violated edge incidence')
    weld = welded_corners(output,cut)
    for _, v in junctions[:-1]:
        if len({weld[i,v] for i,f in enumerate(output) if v in f}) != 2:
            raise ValueError('chain remesh did not create separate slit banks')
    if len({weld[i,next_id] for i,f in enumerate(output) if next_id in f}) != 1:
        raise ValueError('chain remesh did not preserve a welded tip')
    return output,coords,cut,lineage
