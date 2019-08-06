from typing import Union, Dict, List
from math import ceil
from copy import deepcopy
import networkx as nx
import numpy as np

from . import NML
from .nml_generation import generate_graph, generate_nml


def ensure_max_edge_length(nml_or_graph: Union[NML, nx.Graph], max_length: int) -> Union[NML, nx.Graph]:
    # it is easier to operate on a graph
    if isinstance(nml_or_graph, nx.Graph):
        nml_graph = nml_or_graph
    else:
        nml_graph, parameter_dict = generate_graph(nml_or_graph)
    max_id = detect_max_node_id_from_all_graphs(nml_graph)
    next_valid_id = max_id + 1
    for group in nml_graph.values():
        for graph in group:
            next_valid_id = ensure_max_edge_length_in_tree(graph, max_length, next_valid_id)

    # return the same format as the input
    if isinstance(nml_or_graph, nx.Graph):
        return nml_graph
    else:
        return generate_nml(nml_graph, parameter_dict, globalize=False)


def calculate_distance_between_nodes(node1: Dict, node2: Dict) -> float:
    difference_vector = get_vector_between_nodes(node1, node2)
    return np.sqrt(difference_vector.dot(difference_vector))


def get_vector(node: Dict) -> np.ndarray:
    return np.array(node["position"])


def get_vector_between_nodes(node1: Dict, node2: Dict) -> np.ndarray:
    return get_vector(node2) - get_vector(node1)


def get_padding_node_position(node1: Dict, node2: Dict, relative_distance_along_vector: float) -> List[int]:
    node1_position = get_vector(node1)
    vector_between_nodes = get_vector_between_nodes(node1, node2)
    return node1_position + vector_between_nodes * relative_distance_along_vector


def detect_max_node_id_from_all_graphs(graph_dict: Dict[str, nx.Graph]) -> int:
    max_id = 0
    for group in graph_dict.values():
        for tree in group:
            max_id_of_current_tree = np.array(list(tree.nodes)).max()
            max_id = max_id_of_current_tree if max_id_of_current_tree > max_id else max_id

    return max_id


def ensure_max_edge_length_in_tree(graph: nx.Graph, max_length: int, current_id: int) -> int:
    edges_to_be_added = []
    edges_to_be_removed = []
    nodes_to_be_added = []
    for edge in graph.edges:
        node1 = graph.nodes[edge[0]]
        node2 = graph.nodes[edge[1]]
        edge_distance = calculate_distance_between_nodes(node1, node2)
        # add padding nodes if the distance is too high
        if edge_distance > max_length:
            number_of_padding_nodes = ceil(edge_distance / max_length)
            # remove old edge
            edges_to_be_removed.append((edge[0], edge[1]))
            # add all padding nodes and the edges
            previous_edge_id = edge[0]
            for padding_node_number in range(1, number_of_padding_nodes):
                relative_distance_between_nodes = padding_node_number / number_of_padding_nodes
                padding_node_position = get_padding_node_position(node1, node2, relative_distance_between_nodes)

                # attributes of the new node
                padding_node_attributes = deepcopy(node1)
                padding_node_attributes['position'] = (padding_node_position[0],
                                               padding_node_position[1],
                                               padding_node_position[2])
                padding_node_attributes['id'] = current_id
                # add node and edge to predecessor
                nodes_to_be_added.append(padding_node_attributes)
                edges_to_be_added.append((previous_edge_id, current_id))

                # update variables
                previous_edge_id = current_id
                current_id += 1
            # add the edge between the last padding node and the second original node
            edges_to_be_added.append((previous_edge_id, edge[1]))

    graph.remove_edges_from(edges_to_be_removed)
    graph.add_edges_from(edges_to_be_added)
    for node in nodes_to_be_added:
        graph.add_node(node['id'], **node)

    return current_id
