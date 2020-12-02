from typing import Dict, List
import networkx as nx
import numpy as np
from wknml import parse_nml
from wknml.nml_generation import generate_graph
from wknml.nml_utils import (
    ensure_max_edge_length,
    calculate_distance_between_nodes,
    approximate_minimal_edge_length,
    get_vector_between_nodes,
    vector_length,
    calculate_angle_between_vectors,
)


def test_ensure_max_edge_length():
    with open("testdata/nml_with_too_long_edges.nml", "r") as file:
        test_nml = parse_nml(file)
    max_length = 2.0
    scale = np.array(test_nml.parameters.scale)

    test_nml_graph = generate_graph(test_nml)
    # test if the loaded graph violates the max_length
    assert not is_max_length_violated(test_nml_graph[0], max_length, scale)

    # test the graph version
    test_result_nml_graph, _ = ensure_max_edge_length(test_nml_graph, max_length)
    assert is_max_length_violated(test_result_nml_graph, max_length, scale)

    # test the nml version
    test_result_nml = ensure_max_edge_length(test_nml, max_length)
    test_result_nml, _ = generate_graph(test_result_nml)
    assert is_max_length_violated(test_result_nml, max_length, scale)


def is_max_length_violated(
    graph_dict: Dict[str, List[nx.Graph]], max_length: float, scale: np.ndarray
):
    # test if all edges are smaller than the max length
    for group in graph_dict.values():
        for graph in group:
            for edge in graph.edges:
                node1 = graph.nodes[edge[0]]
                node2 = graph.nodes[edge[1]]
                edge_distance = calculate_distance_between_nodes(node1, node2, scale)
                if not edge_distance <= max_length:
                    return False
    return True


def test_approximate_minimal_edge_length():
    with open("testdata/nml_with_small_distance_nodes.nml", "r") as file:
        test_nml = parse_nml(file)
    max_length = 2.0
    max_angle = 0.2
    scale = np.array(test_nml.parameters.scale)

    test_nml_graph = generate_graph(test_nml)
    # test if the loaded graph violates the max_length
    assert not is_minimal_edge_length_violated(
        test_nml_graph[0], max_length, max_angle, scale
    )

    # test the graph interface
    test_result_nml_graph, _ = approximate_minimal_edge_length(
        test_nml_graph, max_length, max_angle
    )
    assert is_minimal_edge_length_violated(
        test_result_nml_graph, max_length, max_angle, scale
    )

    # test the graph interface
    test_result_nml = approximate_minimal_edge_length(test_nml, max_length, max_angle)
    test_result_nml, _ = generate_graph(test_result_nml)
    assert is_minimal_edge_length_violated(
        test_result_nml, max_length, max_angle, scale
    )


def is_minimal_edge_length_violated(
    graph_dict: Dict[str, List[nx.Graph]],
    max_length: float,
    max_angle: float,
    scale: np.ndarray,
):
    for group in graph_dict.values():
        for graph in group:
            nodes_with_degree_of_two = [
                node for node in graph.nodes if graph.degree(node) == 2
            ]
            for two_degree_node in nodes_with_degree_of_two:
                current_node = graph.nodes[two_degree_node]
                neighbors = list(graph.neighbors(two_degree_node))
                neighbor1 = graph.nodes[neighbors[0]]
                neighbor2 = graph.nodes[neighbors[1]]
                vector1 = get_vector_between_nodes(neighbor1, current_node, scale)
                vector2 = get_vector_between_nodes(current_node, neighbor2, scale)
                vector_between_neighbors = get_vector_between_nodes(
                    neighbor1, neighbor2, scale
                )
                distance_between_neighbors = vector_length(vector_between_neighbors)
                angle = calculate_angle_between_vectors(vector1, vector2)
                if not angle > max_angle or distance_between_neighbors > max_length:
                    return False
    return True
