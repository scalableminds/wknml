# Table of Contents

* [wknml](#wknml)
  * [NMLParameters](#wknml.NMLParameters)
  * [Node](#wknml.Node)
  * [Edge](#wknml.Edge)
  * [Tree](#wknml.Tree)
  * [Branchpoint](#wknml.Branchpoint)
  * [Group](#wknml.Group)
  * [Comment](#wknml.Comment)
  * [NML](#wknml.NML)
  * [parse\_nml](#wknml.parse_nml)
  * [write\_nml](#wknml.write_nml)

<a name="wknml"></a>
# wknml

<a name="wknml.NMLParameters"></a>
## NMLParameters Objects

```python
class NMLParameters(NamedTuple)
```

Contains common metadata for NML files

**Attributes**:

- `name` _str_ - Foo
- `scale` _Vector3_ - Foo
- `offset` _Optional[Vector3]_ - Foo
- `time` _Optional[int]_ - Foo
- `editPosition` _Optional[Vector3]_ - Foo
- `editRotation` _Optional[Vector3]_ - Foo
- `zoomLevel` _Optional[float]_ - Foo
  taskBoundingBox (Optional[IntVector6])
  userBoundingBox (Optional[IntVector6])

<a name="wknml.Node"></a>
## Node Objects

```python
class Node(NamedTuple)
```

A webKnossos skeleton node annotation object.

**Attributes**:

- `id` - int
- `position` - Vector3
- `radius` - Optional[float]
- `rotation` - Optional[Vector3]
- `inVp` - Optional[int]
- `inMag` - Optional[int]
- `bitDepth` - Optional[int]
- `interpolation` - Optional[bool]
- `time` - Optional[int]

<a name="wknml.Edge"></a>
## Edge Objects

```python
class Edge(NamedTuple)
```

A webKnossos skeleton edge.

**Attributes**:

- `source` - int (node id reference)
- `target` - int (node id reference)

<a name="wknml.Tree"></a>
## Tree Objects

```python
class Tree(NamedTuple)
```

A webKnossos skeleton (tree) object. A graph structure consisting of nodes and edges.

**Attributes**:

- `id` - int
- `color` - Vector4 (RGBA)
- `name` - str
- `nodes` - List[Node]
- `edges` - List[Edge]
- `groupId` - Optional[int] (group id reference)

<a name="wknml.Branchpoint"></a>
## Branchpoint Objects

```python
class Branchpoint(NamedTuple)
```

A webKnossos branchpoint, i.e. a skeleton node with more than one outgoing edge.

**Attributes**:

- `id` - int (node id reference)
- `time` - int (Unix timestamp)

<a name="wknml.Group"></a>
## Group Objects

```python
class Group(NamedTuple)
```

A container to group several skeletons (trees) together. Mostly for cosmetic or organizational purposes.

**Attributes**:

- `id` - int
- `name` - str
- `children` - List[Group]

<a name="wknml.Comment"></a>
## Comment Objects

```python
class Comment(NamedTuple)
```

A single comment belonging to a skeleton node.

**Attributes**:

- `node` - int (node id reference)
- `content` - str (supports Markdown)

<a name="wknml.NML"></a>
## NML Objects

```python
class NML(NamedTuple)
```

A complete webKnossos skeleton annotation object contain one or more skeletons (trees).

**Attributes**:

- `parameters` - NMLParameters
- `trees` - List[Tree]
- `branchpoints` - List[Branchpoint]
- `comments` - List[Comment]
- `groups` - List[Group]

<a name="wknml.parse_nml"></a>
#### parse\_nml

```python
parse_nml(file: BinaryIO) -> NML
```

Reads a webKnossos NML skeleton file from disk, parses it and returns an NML Python object

**Attributes**:

- `file` _BinaryIO_ - A Python file handle
  

**Returns**:

- `NML` - A webKnossos skeleton annotation as Python NML object
  

**Example**:

  with open("input.nml", "rb") as f:
  nml = wknml.parse_nml(f, nml)

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

  with open("out.nml", "wb") as f:
  wknml.write_nml(f, nml)

