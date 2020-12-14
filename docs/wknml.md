# Table of Contents

* [wknml](#wknml)
  * [NMLParameters](#wknml.NMLParameters)
  * [Node](#wknml.Node)
  * [Edge](#wknml.Edge)
  * [Tree](#wknml.Tree)
  * [Branchpoint](#wknml.Branchpoint)
  * [Group](#wknml.Group)
  * [Comment](#wknml.Comment)
  * [Volume](#wknml.Volume)
  * [NML](#wknml.NML)
  * [parse\_nml](#wknml.parse_nml)
  * [write\_nml](#wknml.write_nml)
* [wknml.nml\_generation](#wknml.nml_generation)
  * [random\_color\_rgba](#wknml.nml_generation.random_color_rgba)
  * [discard\_children\_hierarchy](#wknml.nml_generation.discard_children_hierarchy)
  * [globalize\_tree\_ids](#wknml.nml_generation.globalize_tree_ids)
  * [globalize\_node\_ids](#wknml.nml_generation.globalize_node_ids)
  * [generate\_nml](#wknml.nml_generation.generate_nml)
  * [generate\_graph](#wknml.nml_generation.generate_graph)
  * [nml\_tree\_to\_graph](#wknml.nml_generation.nml_tree_to_graph)
  * [extract\_nodes\_and\_edges\_from\_graph](#wknml.nml_generation.extract_nodes_and_edges_from_graph)
* [wknml.nml\_utils](#wknml.nml_utils)

<a name="wknml"></a>
# wknml

<a name="wknml.NMLParameters"></a>
## NMLParameters Objects

```python
class NMLParameters(NamedTuple)
```

Contains common metadata for NML files

**Notes**:

  Setting a task or user bounding boxes will cause wK to 1) render these visually and 2) prevent data loading from outside them.
  

**Attributes**:

- `name` _str_ - Name of a dataset that the annotation is based on. Will cause wK to open the given skeleton annotation with the referenced dataset.
- `scale` _Vector3_ - Voxel scale of the referenced dataset in nanometers.
- `offset` _Optional[Vector3]_ - Deprecated. Kept for backward compatibility.
- `time` _Optional[int]_ - A UNIX timestamp marking the creation time & date of an annotation.
- `editPosition` _Optional[Vector3]_ - The position of the wK camera when creating/downloading an annotation
- `editRotation` _Optional[Vector3]_ - The rotation of the wK camera when creating/downloading an annotation
- `zoomLevel` _Optional[float]_ - The zoomLevel of the wK camera when creating/downloading an annotation
- `taskBoundingBox` _Optional[IntVector6]_ - A custom bounding box specified as part of a [wK task](https://docs.webknossos.org/guides/tasks). Will be rendered in wK.
- `userBoundingBox` _Optional[IntVector6]_ - A custom user-defined bounding box. Will be rendered in wK.

<a name="wknml.Node"></a>
## Node Objects

```python
class Node(NamedTuple)
```

A webKnossos skeleton node annotation object.

**Attributes**:

- `id` _int_ - A unique identifier
- `position` _Vector3_ - 3D position of a node. Format: [x, y, z]
- `radius` _float = 1.0_ - Radius of a node when rendered in wK. Unit: nanometers (nm)
- `rotation` _Optional[Vector3]_ - 3D rotation of the camera when the node was annotated. Mostly relevant for `Flight` mode to resume in the same direction when returning to `Flight` mode.
- `inVp` _Optional[int]_ - Enumeration of the wK UI viewport in which the node was annotated. `0`: XY plane, `1`: YZ plane. `2`: XY plane, `3`: 3D viewport
- `inMag` _Optional[int]_ - wK rendering magnification-level when the node was annotated. Lower magnification levels typically indicate a "zoomed-in" workflow resulting in more accurate annotations.
- `bitDepth` _Optional[int]_ - wK rendering bit-depth when the node was annotated. 4bit (lower data quality) or 8bit (regular quality). Lower quality data rendering might lead to less accurate annotations.
- `interpolation` _Optional[bool]_ - wK rendering interpolation flag when the node was annotated. Interpolated data rendering might lead to less accurate annotations.
- `time` _Optional[int]_ - A Unix timestamp

<a name="wknml.Edge"></a>
## Edge Objects

```python
class Edge(NamedTuple)
```

A webKnossos skeleton edge.

**Attributes**:

- `source` _int_ - node id reference
- `target` _int_ - node id reference

<a name="wknml.Tree"></a>
## Tree Objects

```python
class Tree(NamedTuple)
```

A webKnossos skeleton (tree) object. A graph structure consisting of nodes and edges.

**Attributes**:

- `id` - int
- `color` _Vector4_ - RGBA
- `name` - str
- `nodes` - List[Node]
- `edges` - List[Edge]
- `groupId` _Optional[int]_ - group id reference

<a name="wknml.Branchpoint"></a>
## Branchpoint Objects

```python
class Branchpoint(NamedTuple)
```

A webKnossos branchpoint, i.e. a skeleton node with more than one outgoing edge.

**Attributes**:

- `id` _int_ - Reference to a `Node` ID
- `time` _int_ - Unix timestamp

<a name="wknml.Group"></a>
## Group Objects

```python
class Group(NamedTuple)
```

A container to group several skeletons (trees) together. Mostly for cosmetic or organizational purposes.

**Attributes**:

- `id` _int_ - A u unique group identifier
- `name` _str_ - NameA  of the group. Will be displayed in wK UI
- `children` _List[Group]_ - List of all sub-groups belonging to this parent element for nested structures

<a name="wknml.Comment"></a>
## Comment Objects

```python
class Comment(NamedTuple)
```

A single comment belonging to a skeleton node.

**Attributes**:

- `node` _int_ - Reference to a `Node` ID
- `content` _str_ - A free text field. Supports Markdown formatting.

<a name="wknml.Volume"></a>
## Volume Objects

```python
class Volume(NamedTuple)
```

A metadata reference to a wK volume annotation. Typically, the volum annotation data is provided a ZIP file in the same directory as the skeleton annotation.

**Attributes**:

- `id` _int_ - A unique Identifier
- `location` _str_ - A path to a ZIP file containing a wK volume annotation
- `fallback_layer` _Optional[str]_ - name of an already existing wK volume annotation segmentation layer (aka "fallback layer")

<a name="wknml.NML"></a>
## NML Objects

```python
class NML(NamedTuple)
```

A complete webKnossos skeleton annotation object contain one or more skeletons (trees).

**Attributes**:

- `parameters` _NMLParameters_ - All the metadata attributes associated with a wK skeleton annotation.
- `trees` _List[Tree]_ - A list of all skeleton/tree objects. Usually contains of the information.
- `branchpoints` _List[Branchpoint]_ - A list of all branchpoint objects.
- `comments` _List[Comment]_ - A list of all comment objects.
- `groups` _List[Group]_ - A list of all group objects.
- `volume` _Optional[Volume]_ - A reference to any volume data that might reside in the directory as the NML file.

<a name="wknml.parse_nml"></a>
#### parse\_nml

```python
parse_nml(file: BinaryIO) -> NML
```

Reads a webKnossos NML skeleton file from disk, parses it and returns an NML Python object

**Arguments**:

- `file` _BinaryIO_ - A Python file handle
  

**Returns**:

- `NML` - A webKnossos skeleton annotation as Python NML object
  

**Example**:

  ```
  with open("input.nml", "rb") as f:
  nml = wknml.parse_nml(f, nml)
  ```

<a name="wknml.write_nml"></a>
#### write\_nml

```python
write_nml(file: BinaryIO, nml: NML)
```

Writes an NML object to a file on disk.

**Arguments**:

- `file` _BinaryIO_ - A Python file handle
- `nml` _NML_ - A NML object that should be persisted to disk
  

**Example**:

  ```
  with open("out.nml", "wb") as f:
  wknml.write_nml(f, nml)
  ```

<a name="wknml.nml_generation"></a>
# wknml.nml\_generation

<a name="wknml.nml_generation.random_color_rgba"></a>
#### random\_color\_rgba

```python
random_color_rgba() -> Tuple[float, float, float, float]
```

A utility to generate a new random RGBA color.

<a name="wknml.nml_generation.discard_children_hierarchy"></a>
#### discard\_children\_hierarchy

```python
discard_children_hierarchy(groups: List[Group]) -> List[Group]
```

A utility to flatten the group structure. All sub-groups will become top-level items.

<a name="wknml.nml_generation.globalize_tree_ids"></a>
#### globalize\_tree\_ids

```python
globalize_tree_ids(group_dict: Dict[str, List[nx.Graph]])
```

A utility to in-place re-assign new and globally unqiue IDs to all Tree objects. Starts with ID 1

**Arguments**:

- `group_dict` _Dict[str, List[nx.Graph]]_ - A mapping of group names to a list of tree as NetworkX graph objects

<a name="wknml.nml_generation.globalize_node_ids"></a>
#### globalize\_node\_ids

```python
globalize_node_ids(group_dict: Dict[str, List[nx.Graph]])
```

A utility to in-place re-assign new and globally unqiue IDs to all Node objects. Edges are updated accordingly. Starts with ID 1.

Note: Does not update any `Comment`s or `BranchPoint`s referencing these nodes.

**Arguments**:

- `group_dict` _Dict[str, List[nx.Graph]]_ - A mapping of group names to a list of tree as NetworkX graph objects

<a name="wknml.nml_generation.generate_nml"></a>
#### generate\_nml

```python
generate_nml(tree_dict: Union[List[nx.Graph], Dict[str, List[nx.Graph]]], parameters: Dict[str, Any] = {}, globalize_ids: bool = True, volume: Optional[Dict[str, Any]] = None) -> NML
```

A utility to convert a [NetworkX graph object](https://networkx.org/) into wK NML skeleton annotation object. Accepts both a simple list of multiple skeletons/trees or a dictionary grouping skeleton inputs.

**Arguments**:

- `tree_dict` _Union[List[nx.Graph], Dict[str, List[nx.Graph]]]_ - A list of wK tree-like structures as NetworkX graphs or a dictionary of group names and same list of NetworkX tree objects.
- `parameters` _Dict[str, Any]_ - A dictionary representation of the skeleton annotation metadata. See `NMLParameters` for accepted attributes.
- `globalize_ids` _bool = True_ - An option to re-assign new, globally unique IDs to all skeletons. Default: `True`
- `volume` _Optional[Dict[str, Any]] = None_ - A dictionary representation of a reference to wK a volume annotation. See `Volume` object for attributes.
  

**Returns**:

- `nml` _NML_ - A wK NML skeleton annotation object
  1. A dictionary with group names as keys and list of all respective NML trees as values
  2. A dictionary representation of the NML metadata parameters

<a name="wknml.nml_generation.generate_graph"></a>
#### generate\_graph

```python
generate_graph(nml: NML) -> Tuple[Dict[str, List[nx.Graph]], Dict[Text, any]]
```

A utility to convert wK NML object into a [NetworkX graph object](https://networkx.org/). Skeletons/Trees are grouped by the provided groups in the NML file.

**Arguments**:

- `nml` _NML_ - A wK NML skeleton annotation object
  

**Returns**:

  A tuple consisting of:
  1. A dictionary with group names as keys and list of all respective NML trees as values
  2. A dictionary representation of the NML metadata parameters. See `NMLParameters` for attributes.

<a name="wknml.nml_generation.nml_tree_to_graph"></a>
#### nml\_tree\_to\_graph

```python
nml_tree_to_graph(tree: Tree) -> nx.Graph
```

A utility to convert a single wK Tree object into a [NetworkX graph object](https://networkx.org/).

<a name="wknml.nml_generation.extract_nodes_and_edges_from_graph"></a>
#### extract\_nodes\_and\_edges\_from\_graph

```python
extract_nodes_and_edges_from_graph(graph: nx.Graph) -> Tuple[List[Node], List[Edge]]
```

A utility to convert a single [NetworkX graph object](https://networkx.org/) into a list of `Node`objects and `Edge` objects.

Return
    Tuple[List[Node], List[Edge]]: A tuple contain both all nodes and edges

<a name="wknml.nml_utils"></a>
# wknml.nml\_utils

