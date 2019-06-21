import xml.etree.ElementTree as ET
from loxun import XmlWriter
from typing import NamedTuple, List, Tuple, Optional
import collections

Vector3 = Tuple[float, float, float]
Vector4 = Tuple[float, float, float, float]
IntVector6 = Tuple[int, int, int, int, int, int]

# From https://stackoverflow.com/a/18348004
# Use the defaults parameter when switching to Python 3.6
def NamedTupleWithDefaults(typename, field_names, default_values=()):
    T = NamedTuple(typename, field_names)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    if isinstance(default_values, collections.Mapping):
        prototype = T(**default_values)
    else:
        prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T

NMLParameters = NamedTupleWithDefaults(
  "NMLParameters",
  [
    ("name", str),
    ("scale", Vector3),
    ("offset", Optional[Vector3]),
    ("time", Optional[int]),
    ("editPosition", Optional[Vector3]),
    ("editRotation", Optional[Vector3]),
    ("zoomLevel", Optional[float]),
    ("taskBoundingBox", Optional[IntVector6]),
    ("userBoundingBox", Optional[IntVector6]),
  ],
  (None,) * 7
)
Node = NamedTupleWithDefaults(
  "Node",
  [
    ("id", int),
    ("position", Vector3),
    ("radius", Optional[float]),
    ("rotation", Optional[Vector3]),
    ("inVp", Optional[int]),
    ("inMag", Optional[int]),
    ("bitDepth", Optional[int]),
    ("interpolation", Optional[bool]),
    ("time", Optional[int]),
  ],
  (None,) * 7
)
Edge = NamedTuple(
  "Edge",
  [
    ("source", int),
    ("target", int),
  ],
)
Tree = NamedTupleWithDefaults(
  "Tree",
  [
    ("id", int),
    ("color", Vector4),
    ("name", str),
    ("nodes", List[Node]),
    ("edges", List[Edge]),
    ("groupId", Optional[int]),
  ],
  (None,) * 1
)
Branchpoint = NamedTuple(
  "Branchpoint",
  [
    ("id", int),
    ("time", int),
  ],
)
Group = NamedTuple(
  "Group",
  [
    ("id", int),
    ("name", str),
    ("children", List["Group"])
  ],
)
Comment = NamedTuple(
  "Comment",
  [
    ("node", int),
    ("content", str),
  ],
)

NML = NamedTuple(
  "NML",
  [
    ("parameters", NMLParameters),
    ("trees", List[Tree]),
    ("branchpoints", List[Branchpoint]),
    ("comments", List[Comment]),
    ("groups", List[Group]),
  ],
)

def parse_bounding_box(nml_parameters, prefix):
    boundingBox = None
    bboxName = prefix + "BoundingBox"
    if nml_parameters.find(bboxName) is not None:
      boundingBox = (
        int(nml_parameters.find(bboxName).get("topLeftX")),
        int(nml_parameters.find(bboxName).get("topLeftY")),
        int(nml_parameters.find(bboxName).get("topLeftZ")),
        int(nml_parameters.find(bboxName).get("width")),
        int(nml_parameters.find(bboxName).get("height")),
        int(nml_parameters.find(bboxName).get("depth")),
      )
    return boundingBox


def parse_parameters(nml_parameters):
    offset = (0, 0, 0)
    if nml_parameters.find("offset") is not None:
        offset = (
            float(nml_parameters.find("offset").get("x")),
            float(nml_parameters.find("offset").get("y")),
            float(nml_parameters.find("offset").get("z")),
        )

    editRotation = (0, 0, 0)
    if nml_parameters.find("editRotation") is not None:
        editRotation = (
            float(nml_parameters.find("editRotation").get("xRot")),
            float(nml_parameters.find("editRotation").get("yRot")),
            float(nml_parameters.find("editRotation").get("zRot")),
        )

    editPosition = (0, 0, 0)
    if nml_parameters.find("editPosition") is not None:
      editPosition = (
        float(nml_parameters.find("editPosition").get("x")),
        float(nml_parameters.find("editPosition").get("y")),
        float(nml_parameters.find("editPosition").get("z")),
      )

    time = 0
    if nml_parameters.find("time") is not None:
      time = int(nml_parameters.find("time").get("ms"))

    zoomLevel = 0
    if nml_parameters.find("zoomLevel") is not None:
        zoomLevel = nml_parameters.find("zoomLevel").get("zoom")

    taskBoundingBox = parse_bounding_box(nml_parameters, "task")
    userBoundingBox = parse_bounding_box(nml_parameters, "user")

    return NMLParameters(
        name=nml_parameters.find("experiment").get("name"),
        scale=(
            float(nml_parameters.find("scale").get("x")),
            float(nml_parameters.find("scale").get("y")),
            float(nml_parameters.find("scale").get("z")),
        ),
        offset=offset,
        time=time,
        editPosition=editPosition,
        editRotation=editRotation,
        zoomLevel=zoomLevel,
        taskBoundingBox=taskBoundingBox,
        userBoundingBox=userBoundingBox,
    )


def parse_node(nml_node):
    return Node(
        id=int(nml_node.get("id")),
        radius=float(nml_node.get("radius", default=None)),
        position=(
            float(nml_node.get("x")),
            float(nml_node.get("y")),
            float(nml_node.get("z")),
        ),
        rotation=(
            float(nml_node.get("rotX", default=0)),
            float(nml_node.get("rotY", default=0)),
            float(nml_node.get("rotZ", default=0)),
        ),
        inVp=int(nml_node.get("inVp", default=0)),
        inMag=int(nml_node.get("inMag", default=0)),
        bitDepth=int(nml_node.get("bitDepth", default=8)),
        interpolation=bool(nml_node.get("interpolation", default=True)),
        time=int(nml_node.get("time", default=0)),
    )


def parse_edge(nml_edge):
    return Edge(source=int(nml_edge.get("source")), target=int(nml_edge.get("target")))


def parse_tree(nml_tree):
    name = ""
    if "comment" in nml_tree.attrib:
        name = nml_tree.get("comment")
    if "name" in nml_tree.attrib:
        name = nml_tree.get("name")

    color = (1, 0, 0, 1)
    if "color.r" in nml_tree.attrib:
        color = (
            float(nml_tree.get("color.r")),
            float(nml_tree.get("color.g")),
            float(nml_tree.get("color.b")),
            float(nml_tree.get("color.a")),
        )
    if "colorr" in nml_tree.attrib:
        color = (
            float(nml_tree.get("colorr")),
            float(nml_tree.get("colorg")),
            float(nml_tree.get("colorb")),
            float(nml_tree.get("colora")),
        )
    groupId = int(nml_tree.get("groupId", default=-1))

    return Tree(
        nodes=[],
        edges=[],
        id=int(nml_tree.get("id")),
        name=name,
        groupId=groupId if groupId >= 0 else None,
        color=color,
    )


def parse_branchpoint(nml_branchpoint):
    return Branchpoint(int(nml_branchpoint.get("id")), int(nml_branchpoint.get("time", 0)))


def parse_comment(nml_comment):
    return Comment(int(nml_comment.get("node")), nml_comment.get("content", default=""))


def parse_group(nml_group):
    return Group(int(nml_group.get("id")), nml_group.get("name", default=""), [])


def parse_nml(file):
    parameters = None
    trees = []
    branchpoints = []
    comments = []
    current_tree = None
    root_group = Group(-1, "", [])
    group_stack = [root_group]
    element_stack = []

    for event, elem in ET.iterparse(file, events=("start", "end")):
        if event == "start":
            element_stack.append(elem)
            if elem.tag == "thing":
                current_tree = parse_tree(elem)
                trees.append(current_tree)
            elif elem.tag == "node":
                assert current_tree is not None, "<node ...> tag needs to be child of a <thing ...> tag."
                current_tree.nodes.append(parse_node(elem))
            elif elem.tag == "edge":
                assert current_tree is not None, "<edge ...> tag needs to be child of a <thing ...> tag."
                current_tree.edges.append(parse_edge(elem))
            elif elem.tag == "branchpoint":
                branchpoints.append(parse_branchpoint(elem))
            elif elem.tag == "comment":
                comments.append(parse_comment(elem))
            elif elem.tag == "group":
                group = parse_group(elem)
                group_stack[-1].children.append(group)
                group_stack.append(group)
        elif event == "end":
            if elem.tag == "parameters":
                parameters = parse_parameters(elem)
            elif elem.tag == "thing":
                current_tree = None
            elif elem.tag == "group":
                group_stack.pop()

            element_stack.pop()
            # Do not clear the elements of the parameters tag as we want to parse those all at once
            # when the closing parameters tag is parsed
            if len(element_stack) and element_stack[-1].tag != "parameters":
                # Discard the element to save memory
                elem.clear()

    return NML(
        parameters=parameters,
        trees=trees,
        branchpoints=branchpoints,
        comments=comments,
        groups=root_group.children,
    )

def dump_bounding_box(xf, parameters, prefix):
    bboxName = prefix + "BoundingBox"
    parametersBox = getattr(parameters, bboxName)

    if parametersBox is not None:
        xf.tag(bboxName, {
            "topLeftX": str(parametersBox[0]),
            "topLeftY": str(parametersBox[1]),
            "topLeftZ": str(parametersBox[2]),
            "width": str(parametersBox[3]),
            "height": str(parametersBox[4]),
            "depth": str(parametersBox[5]),
        })


def dump_parameters(xf, parameters):
    xf.startTag("parameters")
    xf.tag("experiment", {"name": parameters.name})
    xf.tag("scale", {
        "x": str(parameters.scale[0]),
        "y": str(parameters.scale[1]),
        "z": str(parameters.scale[2]),
    })

    if parameters.offset is not None:
        xf.tag("offset", {
            "x": str(parameters.offset[0]),
            "y": str(parameters.offset[1]),
            "z": str(parameters.offset[2]),
        })

    if parameters.time is not None:
        xf.tag("time", {"ms": str(parameters.time)})
    if parameters.editPosition is not None:
        xf.tag("editPosition", {
            "x": str(parameters.editPosition[0]),
            "y": str(parameters.editPosition[1]),
            "z": str(parameters.editPosition[2]),
        })
    if parameters.editRotation is not None:
        xf.tag("editRotation", {
            "xRot": str(parameters.editRotation[0]),
            "yRot": str(parameters.editRotation[1]),
            "zRot": str(parameters.editRotation[2]),
        })
    if parameters.zoomLevel is not None:
        xf.tag("zoomLevel", {"zoom": str(parameters.zoomLevel)})

    dump_bounding_box(xf, parameters, "task")
    dump_bounding_box(xf, parameters, "user")

    xf.endTag() # parameters


def dump_node(xf, node):

    attributes = {
        "id": str(node.id),
        "x": str(node.position[0]),
        "y": str(node.position[1]),
        "z": str(node.position[2]),
    }

    attributes["radius"] = str(node.radius) if node.radius else 1.0

    if node.rotation is not None:
        attributes["rotX"] = str(node.rotation[0])
        attributes["rotY"] = str(node.rotation[1])
        attributes["rotZ"] = str(node.rotation[2])

    if node.inVp is not None:
        attributes["inVp"] = str(node.inVp)

    if node.inMag is not None:
        attributes["inMag"] = str(node.inMag)

    if node.bitDepth is not None:
        attributes["bitDepth"] = str(node.bitDepth)

    if node.interpolation is not None:
        attributes["interpolation"] = str(node.interpolation)

    if node.time is not None:
        attributes["time"] = str(node.time)

    xf.tag("node", attributes)


def dump_edge(xf, edge):
    xf.tag("edge", {"source": str(edge.source), "target": str(edge.target)})


def dump_tree(xf, tree):
    attributes = {
        "id": str(tree.id),
        "color.r": str(tree.color[0]),
        "color.g": str(tree.color[1]),
        "color.b": str(tree.color[2]),
        "color.a": str(tree.color[3]),
        "name": tree.name,
    }
    
    if tree.groupId is not None:
        attributes["groupId"] = str(tree.groupId)
    
    xf.startTag("thing", attributes)
    xf.startTag("nodes")
    for n in tree.nodes: dump_node(xf, n)
    xf.endTag() # nodes
    xf.startTag("edges")
    for e in tree.edges: dump_edge(xf, e)
    xf.endTag() # edges
    xf.endTag() # thing


def dump_branchpoint(xf, branchpoint):
    xf.tag(
        "branchpoint", {"id": str(branchpoint.id), "time": str(branchpoint.time)}
    )


def dump_comment(xf, comment):
    xf.tag(
        "comment", {"node": str(comment.node), "content": comment.content}
    )


def dump_group(xf, group):
    xf.startTag("group", {"id": str(group.id), "name": group.name})
    for g in group.children: dump_group(xf, g)
    xf.endTag() # group


def dump_nml(xf, nml: NML):
    xf.startTag("things")
    dump_parameters(xf, nml.parameters)
    for t in nml.trees: dump_tree(xf, t)

    xf.startTag("branchpoints")
    for b in nml.branchpoints: dump_branchpoint(xf, b)
    xf.endTag() # branchpoints

    xf.startTag("comments")
    for c in nml.comments: dump_comment(xf, c)
    xf.endTag() # comments

    xf.startTag("groups")
    for g in nml.groups: dump_group(xf, g)
    xf.endTag() # groups
    xf.endTag() # things

def write_nml(file, nml: NML):
    with XmlWriter(file) as xf:
        dump_nml(xf, nml)


def compare_parameters(parameters1: NMLParameters, parameters2: NMLParameters) -> bool:
    if parameters1.name != parameters2.name:
        return False
    if parameters1.scale != parameters2.scale:
        return False
    if parameters1.offset != parameters2.offset:
        return False
    if parameters1.time != parameters2.time:
        return False
    if parameters1.editPosition != parameters2.editPosition:
        return False
    if parameters1.editRotation != parameters2.editRotation:
        return False
    if parameters1.zoomLevel != parameters2.zoomLevel:
        return False
    if parameters1.taskBoundingBox != parameters2.taskBoundingBox:
        return False
    if parameters1.userBoundingBox != parameters2.userBoundingBox:
        return False
    return True


def compare_nodes(nodes1: List[Node], nodes2: List[Node]) -> bool:
    if len(nodes1) != len(nodes2):
        return False
    for i in range(len(nodes1)):
        if nodes1[i].id != nodes2[i].id:
            return False
        if nodes1[i].position != nodes2[i].position:
            return False
        if nodes1[i].radius != nodes2[i].radius:
            return False
        if nodes1[i].rotation != nodes2[i].rotation:
            return False
        if nodes1[i].inVp != nodes2[i].inVp:
            return False
        if nodes1[i].inMag != nodes2[i].inMag:
            return False
        if nodes1[i].bitDepth != nodes2[i].bitDepth:
            return False
        if nodes1[i].interpolation != nodes2[i].interpolation:
            return False
        if nodes1[i].time != nodes2[i].time:
            return False
    return True


def compare_edges(edges1: List[Edge], edges2: List[Edge]) -> bool:
    if len(edges1) != len(edges2):
        return False
    for i in range(len(edges1)):
        if edges1[i].source != edges2[i].source:
            return False
        if edges1[i].target != edges2[i].target:
            return False
    return True


def compare_trees(trees1: List[Tree], trees2: List[Tree]) -> bool:
    if len(trees1) != len(trees2):
        return False
    for i in range(len(trees1)):

        if trees1[i].id != trees2[i].id:
            return False
        if trees1[i].color != trees2[i].color:
            return False
        if trees1[i].name != trees2[i].name:
            return False
        if trees1[i].groupId != trees2[i].groupId:
            return False
        if not compare_nodes(trees1[i].nodes, trees2[i].nodes):
            return False
        if not compare_edges(trees1[i].edges, trees2[i].edges):
            return False
    return True


def compare_branchpoints(branchpoints1: List[Branchpoint], branchpoints2: List[Branchpoint]) -> bool:
    if len(branchpoints1) != len(branchpoints2):
        return False
    for i in range(len(branchpoints1)):
        if branchpoints1[i].id != branchpoints2[i].id:
            return False
        if branchpoints1[i].time != branchpoints2[i].time:
            return False
    return True


def compare_comments(comments1: List[Comment], comments2: List[Comment]) -> bool:
    if len(comments1) != len(comments2):
        return False
    for i in range(len(comments1)):
        if comments1[i].node != comments2[i].node:
            return False
        if comments1[i].content != comments2[i].content:
            return False
    return True


def compare_groups(groups1: List[Group], groups2: List[Group]) -> bool:
    if len(groups1) != len(groups2):
        return False
    for i in range(len(groups1)):
        if groups1[i].id != groups2[i].id:
            return False
        if groups1[i].name != groups2[i].name:
            return False
        if not compare_groups(groups1[i].children, groups1[i].children):
            return False
    return True


def compare_nml(nml1: NML, nml2: NML) -> bool:
    if not compare_parameters(nml1.parameters, nml2.parameters):
        return False
    if not compare_trees(nml1.trees, nml2.trees):
        return False
    if not compare_branchpoints(nml1.branchpoints, nml2.branchpoints):
        return False
    if not compare_comments(nml1.comments, nml2.comments):
        return False
    if not compare_groups(nml1.groups, nml2.groups):
        return False
    return True