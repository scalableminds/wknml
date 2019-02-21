import xml.etree.ElementTree as ET
from typing import NamedTuple, List, Tuple, Optional

Vector3 = Tuple[float, float, float]
Vector4 = Tuple[float, float, float, float]

NMLParameters = NamedTuple(
  "NMLParameters",
  [
    ("name", str),
    ("scale", Vector3),
    ("offset", Vector3),
    ("time", int),
    ("editPosition", Vector3),
    ("editRotation", Vector3),
    ("zoomLevel", float),
  ],
)
Node = NamedTuple(
  "Node",
  [
    ("id", int),
    ("radius", float),
    ("position", Vector3),
    ("rotation", Optional[Vector3]),
    ("inVp", Optional[int]),
    ("inMag", Optional[int]),
    ("bitDepth", Optional[int]),
    ("interpolation", Optional[bool]),
    ("time", Optional[int]),
  ],
)
Edge = NamedTuple(
  "Edge",
  [
    ("source", int),
    ("target", int),
  ],
)
Tree = NamedTuple(
  "Tree",
  [
    ("id", int),
    ("color", Vector4),
    ("name", str),
    ("groupId", int),
    ("nodes", List[Node]),
    ("edges", List[Edge]),
  ],
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
    )


def parse_node(nml_node):
    return Node(
        id=int(nml_node.get("id")),
        radius=float(nml_node.get("radius")),
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
        time=int(nml_node.get("time")),
    )


def parse_edge(nml_edge):
    return Edge(source=int(nml_edge.get("source")), target=int(nml_edge.get("target")))


def parse_tree(nml_tree):
    name = ""
    if "comment" in nml_tree.attrib:
        name = nml_tree.get("comment")
    if "name" in nml_tree.attrib:
        name = nml_tree.get("name")

    color = (0, 0, 0, 1)
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

    return Tree(
        nodes=[parse_node(n) for n in nml_tree.find("nodes")],
        edges=[parse_edge(e) for e in nml_tree.find("edges")],
        id=int(nml_tree.get("id")),
        name=name,
        groupId=int(nml_tree.get("groupId", default=1)),
        color=color,
    )


def parse_branchpoint(nml_branchpoint):
    return Branchpoint(int(nml_branchpoint.get("id")), int(nml_branchpoint.get("time", 0)))


def parse_comment(nml_comment):
    return Comment(int(nml_comment.get("node")), nml_comment.get("content", default=""))


def parse_group(nml_group):
    return Group(int(nml_group.get("id")), nml_group.get("name", default=""))


def parse_nml(nml_root):

    groups = [Group(id=1, name="")]
    if nml_root.find("groups") is not None:
      groups = [parse_group(g) for g in nml_root.find("groups")]

    branchpoints = []
    if nml_root.find("branchpoints") is not None:
      branchpoints = [parse_branchpoint(b) for b in nml_root.find("branchpoints")]

    comments = []
    if nml_root.find("comments") is not None:
      comments = [parse_comment(c) for c in nml_root.find("comments")]

    return NML(
        parameters=parse_parameters(nml_root.find("parameters")),
        trees=[parse_tree(t) for t in nml_root.iter("thing")],
        branchpoints=branchpoints,
        comments=comments,
        groups=groups,
    )


def dump_parameters(parameters):
    nml_parameters = ET.Element("parameters")
    ET.SubElement(nml_parameters, "experiment", {"name": parameters.name})
    ET.SubElement(nml_parameters, "time", {"ms": str(parameters.time)})
    ET.SubElement(
        nml_parameters,
        "scale",
        {
            "x": str(parameters.scale[0]),
            "y": str(parameters.scale[1]),
            "z": str(parameters.scale[2]),
        },
    )
    ET.SubElement(
        nml_parameters,
        "editPosition",
        {
            "x": str(parameters.editPosition[0]),
            "y": str(parameters.editPosition[1]),
            "z": str(parameters.editPosition[2]),
        },
    )
    ET.SubElement(
        nml_parameters,
        "editRotation",
        {
            "xRot": str(parameters.editRotation[0]),
            "yRot": str(parameters.editRotation[1]),
            "zRot": str(parameters.editRotation[2]),
        },
    )
    ET.SubElement(nml_parameters, "zoomLevel", {"zoom": str(parameters.zoomLevel)})
    return nml_parameters


def dump_node(node):

    attributes = {
        "id": str(node.id),
        "radius": str(node.radius),
        "x": str(node.position[0]),
        "y": str(node.position[1]),
        "z": str(node.position[2]),
    }

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

    return ET.Element("node", attributes)


def dump_edge(edge):
    return ET.Element("edge", {"source": str(edge.source), "target": str(edge.target)})


def dump_tree(tree):
    nml_tree = ET.Element(
        "thing",
        {
            "id": str(tree.id),
            "groupId": str(tree.groupId),
            "color.r": str(tree.color[0]),
            "color.g": str(tree.color[1]),
            "color.b": str(tree.color[2]),
            "color.a": str(tree.color[3]),
            "name": tree.name,
        },
    )
    nml_nodes = ET.SubElement(nml_tree, "nodes")
    for n in tree.nodes:
        nml_nodes.append(dump_node(n))
    nml_edges = ET.SubElement(nml_tree, "edges")
    for e in tree.edges:
        nml_edges.append(dump_edge(e))
    return nml_tree


def dump_branchpoint(branchpoint):
    return ET.Element(
        "branchpoint", {"id": str(branchpoint.id), "time": str(branchpoint.time)}
    )


def dump_comment(comment):
    return ET.Element(
        "comment", {"node": str(comment.node), "content": comment.content}
    )


def dump_group(group):
    return ET.Element("group", {"id": str(group.id), "name": group.name})


def dump_nml(nml: NML):

    nml_root = ET.Element("things")
    nml_root.append(dump_parameters(nml.parameters))
    for t in nml.trees:
        nml_root.append(dump_tree(t))

    nml_branchpoints = ET.SubElement(nml_root, "branchpoints")
    for b in nml.branchpoints:
        nml_branchpoints.append(dump_branchpoint(b))

    nml_comments = ET.SubElement(nml_root, "comments")
    for c in nml.comments:
        nml_comments.append(dump_comment(c))

    nml_groups = ET.SubElement(nml_root, "groups")
    for g in nml.groups:
        nml_groups.append(dump_group(g))

    return nml_root
