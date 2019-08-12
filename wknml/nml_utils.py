from typing import Union, Dict, List, Tuple
from copy import deepcopy
from math import acos, ceil
import numpy as np
import networkx as nx

from . import NML
from .nml_generation import generate_graph, generate_nml


def get_vector(node: Dict) -> np.ndarray:
    return np.array(node["position"])


def vector_length(vector: List[int]) -> np.ndarray:
    return np.sqrt(vector.dot(vector))


def get_vector_between_nodes(node1: Dict, node2: Dict) -> np.ndarray:
    return get_vector(node2) - get_vector(node1)


def calculate_angle_between_vectors(vector1: np.ndarray, vector2: np.ndarray) -> float:
    dot_val = vector1.dot(vector2)
    length_values = vector_length(vector1) * vector_length(vector2)
    angle = acos(dot_val / length_values)
    return angle


def calculate_distance_between_nodes(node1: Dict, node2: Dict) -> float:
    difference_vector = get_vector_between_nodes(node1, node2)
    return np.sqrt(difference_vector.dot(difference_vector))


def get_padding_node_position(node1: Dict, node2: Dict, relative_distance_along_vector: float) -> List[int]:
    node1_position = get_vector(node1)
    vector_between_nodes = get_vector_between_nodes(node1, node2)
    return node1_position + vector_between_nodes * relative_distance_along_vector


def detect_max_node_id_from_all_graphs(graph_dict: Dict[str, nx.Graph]) -> int:
    max_id = 0
    for group in graph_dict.values():
        for tree in group:
            max_id_of_current_tree = np.array(list(tree.nodes)).max()
            max_id = max(max_id_of_current_tree, max_id)
    return max_id


def approximate_minimal_edge_length(nml_or_graph: Union[NML, nx.Graph], max_length: int, max_angle: float) -> Union[NML, nx.Graph]:
    # it is easier to operate on a graph
    if isinstance(nml_or_graph, NML):
        nml_graph, parameter_dict = generate_graph(nml_or_graph)
    else:
        nml_graph = nml_or_graph[0]
        parameter_dict = nml_or_graph[1]
    for group in nml_graph.values():
        for graph in group:
            approximate_minimal_edge_length_for_graph(graph, max_length, max_angle)

    # return the same format as the input
    if isinstance(nml_or_graph, NML):
        return generate_nml(nml_graph, parameter_dict, globalize_ids=False)
    else:
        return nml_graph, parameter_dict


def approximate_minimal_edge_length_for_graph(graph: nx.Graph, max_length: int, max_angle: float):
    nodes_with_degree_of_two = [node for node in graph.nodes if graph.degree(node) == 2]

    for two_degree_node in nodes_with_degree_of_two:
        current_node = graph.nodes[two_degree_node]
        neighbors = list(graph.neighbors(two_degree_node))
        neighbor1 = graph.nodes[neighbors[0]]
        neighbor2 = graph.nodes[neighbors[1]]
        vector1 = get_vector_between_nodes(neighbor1, current_node)
        vector2 = get_vector_between_nodes(current_node, neighbor2)
        new_edge_vector = get_vector_between_nodes(neighbor1, neighbor2)
        distance_between_combined_edges = vector_length(new_edge_vector)
        angle = calculate_angle_between_vectors(vector1, vector2)
        if angle <= max_angle and distance_between_combined_edges <= max_length:
            graph.remove_edges_from([(neighbors[0], two_degree_node), (two_degree_node, neighbors[1])])
            graph.remove_node(two_degree_node)
            graph.add_edge(neighbors[0], neighbors[1])


def ensure_max_edge_length(nml_or_graph: Union[NML, Tuple[Dict[str, List[nx.Graph]], Dict]], max_length: int) -> Union[NML, nx.Graph]:
    # it is easier to operate on a graph
    if isinstance(nml_or_graph, NML):
        nml_graph, parameter_dict = generate_graph(nml_or_graph)
    else:
        nml_graph = nml_or_graph[0]
        parameter_dict = nml_or_graph[1]
    max_id = detect_max_node_id_from_all_graphs(nml_graph)
    next_valid_id = max_id + 1
    for group in nml_graph.values():
        for graph in group:
            next_valid_id = ensure_max_edge_length_for_graph(graph, max_length, next_valid_id)

    # return the same format as the input
    if isinstance(nml_or_graph, NML):
        return generate_nml(nml_graph, parameter_dict, globalize_ids=False)
        return nml_graph
    else:
        return nml_graph


def ensure_max_edge_length_for_graph(graph: nx.Graph, max_length: int, current_id: int) -> int:
    edges_to_be_added = []
    edges_to_be_removed = []
    nodes_to_be_added = []
    for edge in graph.edges:
        node1 = graph.nodes[edge[0]]
        node2 = graph.nodes[edge[1]]
        edge_distance = calculate_distance_between_nodes(node1, node2)
        # add padding nodes if the distance is too high
        if edge_distance > max_length:
            number_of_nodes = ceil(edge_distance / max_length)
            # remove old edge
            edges_to_be_removed.append((edge[0], edge[1]))
            # add all padding nodes and the edges
            previous_edge_id = edge[0]
            for padding_node_number in range(1, number_of_nodes):
                relative_distance_between_nodes = padding_node_number / number_of_nodes
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
