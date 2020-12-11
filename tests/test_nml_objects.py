from itertools import count

from networkx.algorithms.cuts import volume

from wknml import (
    Edge,
    Group,
    Node,
    Comment,
    NML,
    Tree,
    Branchpoint,
    NMLParameters,
    Volume,
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

    volume = Volume(
        id=next(id_counter),
        location="some/path/to/data.zip",
        fallback_layer="segmentation_layer",
    )

    nml = NML(
        parameters=parameters,
        trees=[tree],
        branchpoints=[branchpoint],
        comments=[comment],
        groups=[group3],
        volume=volume,
    )

    # pass test if all objects can be constructed successfully
    assert True


def test_optional_parameters():
    """Test minimal object constructor. Are the defaults applied."""
    id_counter = count()

    node = Node(id=next(id_counter), position=[1, 2, 3])
    assert node.radius is None
    assert node.rotation is None
    assert node.inVp is None
    assert node.inMag is None
    assert node.bitDepth is None
    assert node.interpolation is None
    assert node.time is None

    tree = Tree(next(id_counter), edges=[], nodes=[], name="Test", color=[])
    assert tree.groupId is None

    parameters = NMLParameters("Test Annotation", [1, 2, 3])
    assert parameters.offset is None
    assert parameters.time is None
    assert parameters.editPosition is None
    assert parameters.editRotation is None
    assert parameters.zoomLevel is None
    assert parameters.taskBoundingBox is None
    assert parameters.userBoundingBox is None

    volume = Volume(
        id=next(id_counter),
        location="some/path/to/data.zip",
    )
    assert volume.fallback_layer is None