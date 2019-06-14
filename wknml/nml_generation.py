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

def globalize_tree_ids(group_dict: Dict[str, List[nx.Graph]]):
    current_id = 1
    for tree_group in group_dict.values():
        for tree in tree_group:
            tree.graph["id"] = current_id
            current_id += 1


def globalize_node_ids(group_dict: Dict[str, List[nx.Graph]]):
    current_id = 1
    for tree_group in group_dict.values():
        for tree_index in range(len(tree_group)):
            tree = tree_group[tree_index]
            new_tree = nx.Graph(**tree.graph)
            edge_mapping_dict = {}
            for node in tree.node:
                old_id = tree.nodes[node]["id"]
                tree.nodes[node]["id"] = current_id
                edge_mapping_dict[old_id] = current_id
                new_tree.add_node(current_id, **tree.nodes[node])

                current_id += 1
            new_edges = []
            for edge in tree.edges:
                new_edges.append((edge_mapping_dict[edge[0]], edge_mapping_dict[edge[1]]))

            new_tree.add_edges_from(new_edges)
            tree_group[tree_index] = new_tree


def generate_nml(group_dict: Union[List[nx.Graph], Dict[str, List[nx.Graph]]], globalize_ids: bool = True, parameters: Dict[str, Any] = {}) -> NML:

  if type(group_dict) is not dict:
    group_dict = ["main_group", group_dict]

    # todo ensure graph attributes and globalize tree ids and maybe group ids
  if globalize_ids:
    globalize_tree_ids(group_dict)
    globalize_node_ids(group_dict)

  nmlParameters = NMLParameters(
    name=parameters["name"] if "name" in parameters else "dataset",
    scale=parameters["scale"] if "scale" in parameters else [11.24, 11.24, 25],
    offset=parameters["offset"] if "offset" in parameters else (0, 0, 0),
    time=parameters["time"] if "time" in parameters else 0,
    editPosition=parameters["editPosition"] if "editPosition" in parameters else (0, 0, 0),
    editRotation=parameters["editRotation"] if "editRotation" in parameters else (0, 0, 0),
    zoomLevel=parameters["zoomLevel"] if "zoomLevel" in parameters else 0,
    taskBoundingBox=parameters["taskBoundingBox"] if "taskBoundingBox" in parameters else None,
    userBoundingBox=parameters["userBoundingBox"] if "userBoundingBox" in parameters else None,
  )

  comments = [Comment(node, tree.nodes[node]["comment"]) for group in group_dict.values()
                  for tree in group
                  for node in tree.nodes if "comment" in tree.nodes[node]]

  branchpoints = [Branchpoint(tree.nodes[node]["id"], 0) for group in group_dict.values()
                  for tree in group
                  for node in tree.nodes if "branchpoint" in tree.nodes[node]]

  groups = [Group(id=group_id, name=group_name, children=[])
            for group_id, group_name in enumerate(group_dict, 1)]

  trees = []

  for group_id, group_name in enumerate(group_dict, 1):
    for tree in group_dict[group_name]:
      nodes, edges = extract_nodes_and_edges_from_graph(tree)
      color = tree.graph["color"] if "color" in tree.graph else random_color_rgba()
      name = tree.graph["name"] if "name" in tree.graph else f"tree{tree.graph['id']}"

      trees.append(Tree(nodes=nodes,
                       edges=edges,
                       id=tree.graph["id"],
                       name=name,
                       groupId=group_id,
                       color=color))

  nml = NML(parameters=nmlParameters,
            trees=trees,
            branchpoints=branchpoints,
            comments=comments,
            groups=groups)

  return nml


def generate_graph(nml: NML) -> Tuple[Dict[str, List[nx.Graph]], Dict]:
    group_dict = {}
    for group in nml.groups:
        graphs_in_current_group = []
        for tree in nml.trees:
            if tree.groupId == group.id:
                graphs_in_current_group.append(nml_tree_to_graph(tree))
        group_dict[group.name] = graphs_in_current_group

    nml_parameters = nml.parameters
    parameter_dict = {}

    parameter_list = ["name", "scale", "offset", "time", "editPosition", "editRotation", "zoomLevel",
                      "taskBoundingBox", "userBoundingBox"]

    for parameter in parameter_list:
        if getattr(nml_parameters, parameter) is not None:
            parameter_dict[parameter] = getattr(nml_parameters, parameter)

    for comment in nml.comments:
        for group in group_dict.values():
            for tree in group:
                if comment.node in tree.nodes:
                    tree.nodes[comment.node]["comment"] = comment.content

    for branchpoint in nml.branchpoints:
        for group in group_dict.values():
            for tree in group:
                if branchpoint.id in tree.nodes:
                    tree.nodes[branchpoint.id]["branchpoint"] = branchpoint.time

    return group_dict, parameter_dict


def nml_tree_to_graph(tree: Tree) -> nx.Graph:
    optional_attribute_list = ["rotation", "inVp", "inMag", "bitDepth", "interpolation"]

    graph = nx.Graph(id= tree.id, color=tree.color, name=tree.name, groupId=tree.groupId)
    for node in tree.nodes:
        node_id = node.id
        graph.add_node(node_id, id=node_id, radius=node.radius, position=node.position)
        for optional_attribute in optional_attribute_list:
            if getattr(node, optional_attribute) is not None:
                graph.nodes[node_id][optional_attribute] = getattr(node, optional_attribute)

    graph.add_edges_from([(edge.source, edge.target) for edge in tree.edges])

    return graph

def discard_children_hierachy(Groups):
    groups_without_hierachy = []
    for group in NML.groups: 



def extract_nodes_and_edges_from_graph(graph: nx.Graph) -> Tuple[List[Node], List[Edge]]:
  node_nml = [Node(id=graph.nodes[node]["id"],
                   position=graph.nodes[node]["position"],
                   radius=graph.nodes[node]["radius"] if "radius" in graph.nodes[node] else None,
                   rotation=graph.nodes[node]["rotation"] if "rotation" in graph.nodes[node] else None,
                   inVp=graph.nodes[node]["inVp"] if "inVp" in graph.nodes[node] else None,
                   inMag=graph.nodes[node]["inMag"] if "inMag" in graph.nodes[node] else None,
                   bitDepth=graph.nodes[node]["bitDepth"] if "bitDepth" in graph.nodes[node] else None,
                   interpolation=graph.nodes[node]["interpolation"] if "interpolation" in graph.nodes[node] else None)
                for node in graph.nodes]

  edge_nml = [Edge(source=edge[0], target=edge[1]) for edge in graph.edges]

  return node_nml, edge_nml
