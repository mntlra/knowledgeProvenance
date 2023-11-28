import re

from rdflib.graph import ConjunctiveGraph, Graph
from rdflib.term import BNode, URIRef
from rdflib.util import guess_format

from extended_nanopub.definitions import NP_PURL, NP_TEMP_PREFIX


def get_trustyuri(resource, baseuri, hashstr, bnodemap):
    """Most of the work done to normalize URIs happens here"""
    if resource is None:
        return None
    np_uri = get_str(baseuri).decode('utf-8')
    # baseuri passed is the np namespace, np_uri is the extended_nanopub URI without trailing # or /
    if np_uri.endswith('#') or np_uri.endswith('/'):
        np_uri = np_uri[:-1]
    # Extract the trusty artefact if present, or remove the trailing / if trusty not present
    prefix = "/".join(baseuri.split('/')[:-1]) + '/'
    if str(baseuri).startswith(NP_TEMP_PREFIX):
        prefix = NP_PURL
    if isinstance(resource, URIRef):
        suffix = get_suffix(resource, baseuri)
        if get_str(resource).decode('utf-8') == np_uri:
            return str(f"{prefix}{hashstr}")
        if suffix is None and not get_str(resource).decode('utf-8') == get_str(baseuri).decode('utf-8'):
            return str(resource)
        if suffix is None or suffix == "":
            return str(f"{prefix}{hashstr}")
        return str(f"{prefix}{hashstr}#{suffix}")
    if isinstance(resource, BNode):
        bnode_unnamed = re.match(r'^[a-zA-Z0-9]{33}$', str(resource))
        # Check if BNode in the form of N2b80343001e94f48bdee0901be566ebb
        # Which means it was automatically generated by rdflib: we use a number in this case
        if bnode_unnamed:
            n = get_bnode_number(resource, bnodemap)
            np_uri = str(f"{prefix}{hashstr}")
            return str(np_uri + "#_" + str(n))
        else:
            # If the user gave a specific name to the bnode with rdflib
            return str(f"{prefix}{hashstr}" + "#_" + str(resource))
    else:
        return None


def get_suffix(plainuri, baseuri):
    p = get_str(plainuri)
    b = get_str(baseuri)
    if (p == b):
        return None
    if (p.startswith(b)):
        return p[len(b):].decode('utf-8')
    return None


def normalize(uri, hashstr):
    if hashstr is None:
        return get_str(uri)
    try:
        return re.sub(hashstr, " ", str(uri))
    except Exception:
        return re.sub(hashstr.decode('utf-8'), " ", str(uri))


def get_bnode_number(bnode, bnodemap):
    i = get_str(bnode)
    if i not in bnodemap.keys():
        n = len(bnodemap) + 1
        bnodemap[i] = n
    return bnodemap[i]


def expand_baseuri(baseuri):
    s = get_str(baseuri).decode('utf-8')
    if re.match(r'.*[A-Za-z0-9\-_]', s):
        s = s + "."
    return s


def get_quads(conjunctivegraph):
    quads = []
    for s, p, o, c in conjunctivegraph.quads((None, None, None)):
        g = c.identifier
        if not isinstance(g, URIRef):
            g = None
        quads.append((g, s, p, o))
    quads.sort()
    return quads


def get_conjunctivegraph(quads):
    cg = ConjunctiveGraph()
#     for (c, s, p, o) in quads:
#         cg.default_context = Graph(store=cg.store, identifier=c)
#         cg.add((s, p, o))
    cg.addN([(s, p, o, Graph(store=cg.store, identifier=c)) for (c, s, p, o) in quads])
    return cg


def get_format(filename):
    return guess_format(filename, {'xml': 'trix', 'ttl': 'turtle', 'nq': 'nquads', 'nt': 'nt', 'rdf': 'xml'})


def get_str(s):
    return s.encode('utf-8')
