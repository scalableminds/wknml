from wknml import NMLParameters, Group, Edge, Node, Tree, NML, Branchpoint
import networkx as nx
import numpy as np

import logging
import colorsys
from typing import Tuple, List, Generator, Optional, Dict, Union


logger = logging.getLogger(__name__)


def random_color_rgba():
  # https://stackoverflow.com/a/43437435/783758

  h, s, l = np.random.random(), 0.5 + np.random.random() / 2.0, 0.4 + np.random.random() / 5.0
  r, g, b = colorsys.hls_to_rgb(h, l, s)
  return (r, g, b, 1)


def generate_agglomeration_nmls(edge_list: np.ndarray,
                                affinities: np.ndarray,
                                thresholds: List[int],
                                first_mapping: MappingType,
                                segment_stats: Dict[int, SegmentStats],
                                dataset_name: str,
                                scale: Tuple[float, float, float],
                                sample_size: Optional[int] = None,
                                ids: Optional[List[int]] = None) \
    -> Generator[Tuple[int, NML], None, None]:

  logger.info("Building graph for threshold {}...".format(thresholds[0]))
  rag = nx.Graph()
  rag.add_edges_from(edge_list[affinities >= thresholds[0]])
  prev_threshold = thresholds[0]

  if sample_size is not None:
    logger.info("Sampling classes from first mapping...")
    mapping_sizes = np.array([len(c) for c in first_mapping])
    mapping_indices = np.random.choice(len(first_mapping),
                                       size=sample_size,
                                       replace=False,
                                       p=(mapping_sizes / mapping_sizes.sum()))
    ids = [min(first_mapping[i]) for i in mapping_indices]
  else:
    assert ids is not None, "Must provide either sample_size or segment_ids!"

  colors = [random_color_rgba() for _ in ids]

  for threshold in thresholds:

    if threshold != thresholds[0]:

      logger.info("Building graph for threshold {}...".format(threshold))
      new_edges_mask = np.logical_and(affinities >= threshold,
                                      affinities < prev_threshold)
      rag.add_edges_from(edge_list[new_edges_mask])
      prev_threshold = threshold

    logger.info("Selecting equivalence classes for threshold {}..".format(threshold))
    filtered_mapping = []
    for segment_id in ids:
      filtered_mapping.append(nx.node_connected_component(rag, segment_id))

    logger.info("Selecting subgraphs for threshold {}...".format(threshold))
    subgraphs = list(get_subgraphs(rag, filtered_mapping, ids, colors))

    logger.info("Building NML for threshold {}...".format(threshold))
    nml = generate_nml(dataset_name, scale, subgraphs, segment_stats, "Threshold {}".format(threshold))

    yield threshold, nml


def get_subgraphs(rag: nx.Graph,
                  mapping: MappingType,
                  ids: List[int],
                  colors: List[Tuple[float, float, float, float]]) \
    -> Generator[Tuple[nx.Graph, dict], None, None]:

  tree_ids = set()

  for equivalence_class, original_id, color in zip(mapping, ids, colors):

    tree_id = min(equivalence_class)
    if tree_id in tree_ids:
      # Two trees got merged
      continue
    tree_ids.add(tree_id)

    rag_subgraph = rag.subgraph(equivalence_class)
    attributes = {
      "id": tree_id,
      "color": color,
      "name": "Segment {} (originally {})".format(tree_id, original_id),
    }

    yield rag_subgraph, attributes

def globalize_node_ids(trees: List[nx.Graph]):
  current_id = 0
  for tree in trees:
    for node in tree.nodes:
      node['id'] = current_id
      current_id += 1


def generate_nml(trees: Union[List[nx.Graph], Dict[str, List[nx.Graph]]], dataset_name: str = None, globalize_ids: bool = True) -> NML:

  if type(trees) is dict:
    tree_list = trees.values()
  else:
    tree_list = trees

  if globalize_ids:
    globalize_node_ids(tree_list)

  nmlParameters = NMLParameters(
    name=dataset_name,
    scale=scale,
    offset=(0, 0, 0),
    time=0,
    editPosition=(0, 0, 0),
    editRotation=(0, 0, 0),
    zoomLevel=0
  )

  branchpoints = []
  comments = []
  groups = []

  if group_name is not None:
    groups = Group(id=1, name=group_name, children=[])

  if branchpoint_ids is not None:
    branchpoints = [Branchpoint(b, 0) for b in branchpoint_ids]

  trees = []
  for tree_nx, attributes in trees_nx:

    nodes, edges = extract_nodes_and_edges(tree_nx, segment_stats)
    color = attributes["color"] if "color" in attributes else random_color_rgba()

    trees.append(Tree(nodes=nodes,
                      edges=edges,
                      id=attributes["id"],
                      name=attributes["name"],
                      groupId=(None if group_name is None else 1),
                      color=color))

  nml = NML(parameters=nmlParameters,
            trees=trees,
            branchpoints=branchpoints,
            comments=comments,
            groups=groups)

  return nml


def extract_nodes_and_edges(graph: nx.Graph,
                            segment_stats: Dict[int, SegmentStats]) \
    -> Tuple[List[Node], List[Edge]]:

  node_nml = []
  edge_nml = []

  for node in graph.nodes:

    node_nml.append(Node(id=node,
                         radius=1.0,
                         position=segment_stats[node].position))

  for edge in graph.edges:
    edge_nml.append(Edge(edge[0], edge[1]))

  return node_nml, edge_nml
