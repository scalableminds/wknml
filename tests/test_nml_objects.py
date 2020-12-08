from itertools import count

from wknml import (
    Edge,
    Group,
    Node,
    Comment,
    NML,
    Tree,
    Branchpoint,
    NMLParameters,
)
from networkx.classes.graph import Graph

timestamp = 1607446137


def test_build_new_nml_onject():
    """Create a new NML object from primitives. Test each constructor"""

    id_counter = count()

    node_1 = Node(
        id=next(id_counter),
        position=[1, 2, 3],
        radius=10,
        rotation=[1, 2, 3],
        inVp=1,
        inMag=1,
        bitDepth=8,
        interpolation=True,
        time=timestamp,
    )

    node_2 = Node(next(id_counter), [1, 2, 3], 10, [1, 2, 3], 1, 1, 8, True, timestamp)

    edge = Edge(node_1.id, node_2.id)

    comment = Comment(node_1.id, "This is a test")
    branchpoint = Branchpoint(node_2.id, timestamp)

    group1 = Group(id=next(id_counter), name="Test Sub Group", children=[])
    group2 = Group(next(id_counter), "Test Sub Group", [])
    group3 = Group(
        id=next(id_counter), name="Test Parent Group", children=[group1, group2]
    )

    tree = Tree(
        id=next(id_counter),
        nodes=[node_1, node_2],
        color=[255, 0, 255, 255],
        name="Test Tree 1",
        edges=[edge],
        groupId=group3.id,
    )

    parameters = NMLParameters(
        "Test Skeleton Annotation",
        scale=[1, 2, 3],
        offset=[1, 2, 3],
        time=timestamp,
        editPosition=[1, 2, 3],
        editRotation=[1, 2, 3],
        zoomLevel=1,
        taskBoundingBox=[1, 2, 3, 1, 2, 3],
        userBoundingBox=[1, 2, 3, 1, 2, 3],
    )

    nml = NML(
        parameters=parameters,
        trees=[tree],
        branchpoints=[branchpoint],
        comments=[comment],
        groups=[group3],
    )

    # pass test if all objects can be constructed successfully
    assert True


def test_optional_parameters():
    """Test minimal object constructor. Are the defaults applied."""
    id_counter = count()

    node = Node(id=next(id_counter), position=[1, 2, 3])
    assert node.radius == None
    assert node.rotation == None
    assert node.inVp == None
    assert node.inMag == None
    assert node.bitDepth == None
    assert node.interpolation == None
    assert node.time == None

    tree = Tree(next(id_counter), edges=[], nodes=[], name="Test", color=[])
    assert tree.groupId == None

    parameters = NMLParameters("Test Annotation", [1, 2, 3])
    assert parameters.offset == None
    assert parameters.time == None
    assert parameters.editPosition == None
    assert parameters.editRotation == None
    assert parameters.zoomLevel == None
    assert parameters.taskBoundingBox == None
    assert parameters.userBoundingBox == None
