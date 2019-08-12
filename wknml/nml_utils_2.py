from typing import Union, Dict, List
from math import acos
import numpy as np
import networkx as nx

from . import NML
from .nml_generation import generate_graph, generate_nml


def calculate_distance_between_nodes(node1: Dict, node2: Dict) -> float:
    difference_vector = get_vector_between_nodes(node1, node2)
    return np.sqrt(difference_vector.dot(difference_vector))


def get_vector(node: Dict) -> np.ndarray:
    return np.array(node["position"])


def get_vector_between_nodes(node1: Dict, node2: Dict) -> np.ndarray:
    return get_vector(node2) - get_vector(node1)


def vector_length(vector: List[int]) -> np.ndarray:
    return np.sqrt(vector.dot(vector))


def calculate_angle_between_vectors(vector1: np.ndarray, vector2: np.ndarray) -> float:
    dot_val = vector1.dot(vector2)
    length_values = vector_length(vector1) * vector_length(vector2)
    angle = acos(dot_val / length_values)
    return angle


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
