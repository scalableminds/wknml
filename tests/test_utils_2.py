from wknml import parse_nml
from wknml.nml_utils import approximate_minimal_edge_length, get_vector_between_nodes, vector_length, calculate_angle_between_vectors
from wknml.nml_generation import generate_graph


def test_approximate_minimal_edge_length():
    with open("testdata/nml_with_small_distance_nodes.nml", "r") as file:
        test_nml = parse_nml(file)
    max_length = 2.0
    max_angle = 0.2

    # test the graph interface
    test_nml_graph = generate_graph(test_nml)
    test_result_nml_graph, parameter_dict = approximate_minimal_edge_length(test_nml_graph, max_length, max_angle)

    for group in test_result_nml_graph.values():
        for graph in group:
            nodes_with_degree_of_two = [node for node in graph.nodes if graph.degree(node) == 2]
            for two_degree_node in nodes_with_degree_of_two:
                current_node = graph.nodes[two_degree_node]
                neighbors = list(graph.neighbors(two_degree_node))
                neighbor1 = graph.nodes[neighbors[0]]
                neighbor2 = graph.nodes[neighbors[1]]
                vector1 = get_vector_between_nodes(neighbor1, current_node)
                vector2 = get_vector_between_nodes(current_node, neighbor2)
                vector_between_neighbors = get_vector_between_nodes(neighbor1, neighbor2)
                distance_between_neighbors = vector_length(vector_between_neighbors)
                angle = calculate_angle_between_vectors(vector1, vector2)
                assert angle > max_angle or distance_between_neighbors > max_length

    # test the graph interface
    test_result_nml = approximate_minimal_edge_length(test_nml, max_length, max_angle)
    test_result_nml, parameter_dict = generate_graph(test_result_nml)
    for group in test_result_nml.values():
        for graph in group:
            nodes_with_degree_of_two = [node for node in graph.nodes if graph.degree(node) == 2]
            for two_degree_node in nodes_with_degree_of_two:
                current_node = graph.nodes[two_degree_node]
                neighbors = list(graph.neighbors(two_degree_node))
                neighbor1 = graph.nodes[neighbors[0]]
                neighbor2 = graph.nodes[neighbors[1]]
                vector1 = get_vector_between_nodes(neighbor1, current_node)
                vector2 = get_vector_between_nodes(current_node, neighbor2)
                vector_between_neighbors = get_vector_between_nodes(neighbor1, neighbor2)
                distance_between_neighbors = vector_length(vector_between_neighbors)
                angle = calculate_angle_between_vectors(vector1, vector2)
                assert angle > max_angle or distance_between_neighbors > max_length


if __name__ == "__main__":
    test_approximate_minimal_edge_length()
