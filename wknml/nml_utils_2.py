from typing import Union, Dict, List
from math import sqrt, acos
import networkx as nx

from . import NML
from .nml_generation import generate_graph, generate_nml


def calculate_distance_between_nodes(node1: Dict, node2: Dict) -> float:
    node1_position = node1['position']
    node2_position = node2['position']
    return sqrt((node1_position[0] - node2_position[0]) ** 2 +
                (node1_position[1] - node2_position[1]) ** 2 +
                (node1_position[2] - node2_position[2]) ** 2)


def vector_between_nodes(node1: Dict, node2: Dict) -> List[int]:
    node1_position = node1['position']
    node2_position = node2['position']
    return [node2_position[0] - node1_position[0],
            node2_position[1] - node1_position[1],
            node2_position[2] - node1_position[2]]


def dot_product(vector1: List[int], vector2: List[int]) -> int:
    return vector1[0] * vector2[0] + \
           vector1[1] * vector2[1] + \
           vector1[2] * vector2[2]


def vector_length(vector: List[int]) -> int:
    return sqrt(vector[0] ** 2 +
                vector[1] ** 2 +
                vector[2] ** 2)


def calculate_angle_between_vectors(vector1: List[int], vector2: List[int]):
    dot_val = dot_product(vector1, vector2)
    length_values = vector_length(vector1) * vector_length(vector2)
    angle = acos(dot_val / length_values)
    return angle


def approximate_minimal_edge_length(nml_or_graph: Union[NML, nx.Graph], max_length: int, max_angle: float) -> Union[NML, nx.Graph]:
    # it is easier to operate on a graph
    if isinstance(nml_or_graph, nx.Graph):
        nml_graph = nml_or_graph
    else:
        nml_graph, parameter_dict = generate_graph(nml_or_graph)
    for group in nml_graph.values():
        for graph in group:
            approximate_minimal_edge_length_for_graph(graph, max_length, max_angle)

    # return the same format as the input
    if isinstance(nml_or_graph, nx.Graph):
        return nml_graph
    else:
        return generate_nml(nml_graph, parameter_dict, globalize_ids=False)


def approximate_minimal_edge_length_for_graph(graph: nx.Graph, max_length: int, max_angle: float):
    all_nodes_with_degree_of_two = [node for node in graph.nodes if graph.degree(node) == 2]

    for two_degree_node in all_nodes_with_degree_of_two:
        current_node = graph.nodes[two_degree_node]
        neighbors = list(graph.neighbors(two_degree_node))
        neighbor1 = graph.nodes[neighbors[0]]
        neighbor2 = graph.nodes[neighbors[1]]
        vector1 = vector_between_nodes(neighbor1, current_node)
        vector2 = vector_between_nodes(current_node, neighbor2)
        new_edge_vector = vector_between_nodes(neighbor1, neighbor2)
        distance_between_combined_edges = vector_length(new_edge_vector)
        angle = calculate_angle_between_vectors(vector1, vector2)
        if angle <= max_angle and distance_between_combined_edges <= max_length:
            graph.remove_edges_from([(neighbors[0], two_degree_node), (two_degree_node, neighbors[1])])
            graph.remove_node(two_degree_node)
            graph.add_edge(neighbors[0], neighbors[1])
