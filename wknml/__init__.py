import xml.etree.ElementTree as ET
from lxml import etree
from typing import NamedTuple, List, Tuple, Optional

Vector3 = Tuple[float, float, float]
Vector4 = Tuple[float, float, float, float]
IntVector6 = Tuple[int, int, int, int, int, int]

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
    ("taskBoundingBox", Optional[IntVector6]),
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
    ("groupId", Optional[int]),
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

    taskBoundingBox = None
    if nml_parameters.find("taskBoundingBox") is not None:
      taskBoundingBox = (
        int(nml_parameters.find("taskBoundingBox").get("topLeftX")),
        int(nml_parameters.find("taskBoundingBox").get("topLeftY")),
        int(nml_parameters.find("taskBoundingBox").get("topLeftZ")),
        int(nml_parameters.find("taskBoundingBox").get("width")),
        int(nml_parameters.find("taskBoundingBox").get("height")),
        int(nml_parameters.find("taskBoundingBox").get("depth")),
      )

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
        taskBoundingBox=taskBoundingBox
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


def dump_parameters(xf, parameters):
    with xf.element("parameters"):
        write_element(xf, "experiment", {"name": parameters.name})
        write_element(xf, "time", {"ms": str(parameters.time)})
        write_element(xf, "scale", {
            "x": str(parameters.scale[0]),
            "y": str(parameters.scale[1]),
            "z": str(parameters.scale[2]),
        })
        write_element(xf, "editPosition", {
            "x": str(parameters.editPosition[0]),
            "y": str(parameters.editPosition[1]),
            "z": str(parameters.editPosition[2]),
        })
        write_element(xf, "editRotation", {
            "xRot": str(parameters.editRotation[0]),
            "yRot": str(parameters.editRotation[1]),
            "zRot": str(parameters.editRotation[2]),
        })
        write_element(xf, "zoomLevel", {"zoom": str(parameters.zoomLevel)})

        if parameters.taskBoundingBox is not None:
            write_element(xf, "taskBoundingBox", {
                "topLeftX": str(parameters.taskBoundingBox[0]),
                "topLeftY": str(parameters.taskBoundingBox[1]),
                "topLeftZ": str(parameters.taskBoundingBox[2]),
                "width": str(parameters.taskBoundingBox[3]),
                "height": str(parameters.taskBoundingBox[4]),
                "depth": str(parameters.taskBoundingBox[5]),
            })

def write_element(xf, name, attr):
    xf.write(etree.Element(name, attr))

def dump_node(xf, node):
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

    write_element(xf, "node", attributes)


def dump_edge(xf, edge):
    write_element(xf, "edge", {"source": str(edge.source), "target": str(edge.target)})


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
    
    with xf.element("thing", attributes):
        with xf.element("nodes"):
            for n in tree.nodes: dump_node(xf, n)
        with xf.element("edges"):
            for e in tree.edges: dump_edge(xf, e)


def dump_branchpoint(xf, branchpoint):
    write_element(xf, 
        "branchpoint", {"id": str(branchpoint.id), "time": str(branchpoint.time)}
    )


def dump_comment(xf, comment):
    write_element(xf, 
        "comment", {"node": str(comment.node), "content": comment.content}
    )


def dump_group(xf, group):
    write_element(xf, "group", {"id": str(group.id), "name": group.name})


def dump_nml(xf, nml: NML):
    with xf.element("things"):
        dump_parameters(xf, nml.parameters)
        for t in nml.trees: dump_tree(xf, t)

        with xf.element("branchpoints"):
            for b in nml.branchpoints: dump_branchpoint(xf, b)

        with xf.element("comments"):
            for c in nml.comments: dump_comment(xf, c)

        with xf.element("groups"):
            for g in nml.groups: dump_group(xf, g)
