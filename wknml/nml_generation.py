from wknml import NMLParameters, Group, Edge, Node, Tree, NML, Branchpoint, Comment
import networkx as nx
import numpy as np

import logging
import colorsys
from typing import Tuple, List, Dict, Union, Any


logger = logging.getLogger(__name__)


def random_color_rgba():
  # https://stackoverflow.com/a/43437435/783758

  h, s, l = np.random.random(), 0.5 + np.random.random() / 2.0, 0.4 + np.random.random() / 5.0
  r, g, b = colorsys.hls_to_rgb(h, l, s)
  return (r, g, b, 1)


def globalize_node_ids(trees: Dict[str, List[nx.Graph]]):
  current_id = 1
  for tree_group in trees:
    for tree in tree_group:
      for node in tree.nodes:
        old_id = node["id"]
        node["id"] = current_id
        for edge in tree.edges:
            if edge[0] == old_id:
                edge[0] = current_id
            if edge[1] == old_id:
                edge[1] == current_id

        current_id += 1



def generate_nml(group_dict: Union[List[nx.Graph], Dict[str, List[nx.Graph]]], globalize_ids: bool = True, parameters: Dict[str, Any] = {}) -> NML:

  """ASSERTIONS SO FAR: every tree has an id, name"""

  if type(group_dict) is not dict:
    group_dict = ["main_group", group_dict]

  if globalize_ids:
    globalize_node_ids(group_dict)

  nmlParameters = NMLParameters(
    name=parameters["name"] if "name" in parameters else "dataset",
    scale=parameters["scale"] if "scale" in parameters else [11.24, 11.24, 25],
    offset=parameters["offset"] if "offset" in parameters else (0, 0, 0),
    time=parameters["time"] if "time" in parameters else 0,
    editPosition=parameters["editPosition"] if "editPosition" in parameters else (0, 0, 0),
    editRotation=parameters["editRotation"] if "editRotation" in parameters else (0, 0, 0),
    zoomLevel=parameters["zoomLevel"] if "zoomLevel" in parameters else 0,
  )

  comments = [Comment(node["id"], node["comment"]) for group in group_dict.values()
                  for tree in group
                  for node in tree if "comment" in node]

  branchpoints = [Branchpoint(node["id"], 0) for group in group_dict.values()
                  for tree in group
                  for node in tree if "branchpoint_id" in node]

  groups = [Group(id=group_id, name=group_name, children=[])
            for group_id, group_name in enumerate(group_dict, 1)]

  trees = []

  for group_id, group_name in enumerate(group_dict, 1):
    for tree in group_dict[group_name]:
      nodes, edges = extract_nodes_and_edges_from_graph(tree)
      color = tree.graph["color"] if "color" in tree.graph else random_color_rgba()

      trees.append(Tree(nodes=nodes,
                       edges=edges,
                       id=tree.graph["id"],
                       name=tree.graph["name"],
                       groupId=group_id,
                       color=color))

  nml = NML(parameters=nmlParameters,
            trees=trees,
            branchpoints=branchpoints,
            comments=comments,
            groups=groups)

  return nml


def generate_graph(nml: NML) -> Dict[str, List[nx.Graph]]:
    graph_dict = {}
    for group in NML["groups"]:
        graphs_in_current_group = []
        for tree in NML["trees"]:
            if tree["groupId"] == group["id"]:
                graphs_in_current_group.append(nml_tree_to_graph(tree))
        graph_dict[group["name"]] = graphs_in_current_group

    return graph_dict


def nml_tree_to_graph(tree: Tree) -> nx.Graph:
    optional_attribute_list = ["rotation", "inVp", "inMag", "bitDepth","interpolation"]

    graph = nx.Graph(id= tree["id"], color=tree["color"], name=tree["name"], groupId=tree["edges"])
    for node in tree["nodes"]:
        node_id = node["id"]
        graph.add_node(node_id, id=node_id, radius=node["radius"], position=node["position"])
        for optional_attribute in optional_attribute_list:
            if node[optional_attribute] is not None:
                graph.nodes[node_id][optional_attribute] = node[optional_attribute]

    graph.add_edges_from(tree["edges"])
    return graph


def extract_nodes_and_edges_from_graph(graph: nx.Graph) -> Tuple[List[Node], List[Edge]]:
  node_nml = [Node(id=graph.nodes[node_index]["id"],
                   radius=1.0,
                   position=graph.node[node_index]["position"],
                   rotation=graph.node[node_index]["rotation"] if "rotation" in graph.node[node_index] else None,
                   inVp=graph.node[node_index]["inVp"] if "inVp" in graph.node[node_index] else None,
                   inMag=graph.node[node_index]["inMag"] if "inMag" in graph.node[node_index] else None,
                   bitDepth=graph.node[node_index]["bitDepth"] if "bitDepth" in graph.node[node_index] else None,
                   interpolation=graph.node[node_index]["interpolation"] if "interpolation" in graph.node[node_index] else None)
                  for node_index in range(len(graph.nodes))]

  edge_nml = [Edge(edge[0], edge[1]) for edge in graph.edges]

  return node_nml, edge_nml
