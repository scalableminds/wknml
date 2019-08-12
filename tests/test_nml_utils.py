from wknml import parse_nml, write_nml
from wknml.nml_generation import generate_graph
from wknml.nml_utils import ensure_max_edge_length, calculate_distance_between_nodes

def test_ensure_max_edge_length():
    with open("testdata/nml_with_too_long_edges.nml", "r") as file:
        test_nml = parse_nml(file)
    max_length = 2.0
    test_nml = generate_graph(test_nml)
    test_result_nml_graph = ensure_max_edge_length(test_nml, max_length)

    # test if all edges are smaller than the max length
    for group in test_result_nml_graph.values():
        for graph in group:
            for edge in graph.edges:
                node1 = graph.nodes[edge[0]]
                node2 = graph.nodes[edge[1]]
                edge_distance = calculate_distance_between_nodes(node1, node2)
                assert edge_distance <= max_length


if __name__ == "__main__":
    test_ensure_max_edge_length()
