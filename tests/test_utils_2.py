from wknml import parse_nml, write_nml
from wknml.nml_utils_2 import approximate_minimal_edge_length


def test_approximate_minimal_edge_length():
    with open("testdata/nml_with_small_distance_nodes.nml", "r") as file:
        test_nml = parse_nml(file)
    max_length = 2.0
    max_angle = 0.2
    test_result_nml = approximate_minimal_edge_length(test_nml, max_length, max_angle)

    with open("testdata/nml_with_approximated_distances.nml", "r") as file:
        expected_nml = parse_nml(file)

    # need to save and load the test_result_nml since reading applies default values
    # thus this is needed to be able to compare the nmls
    with open("testoutput/approximate_min_length.nml", "wb") as file:
        write_nml(file=file, nml=test_result_nml)

    with open("testoutput/approximate_min_length.nml", "r") as file:
        test_result_nml = parse_nml(file)

    assert test_result_nml == expected_nml


if __name__ == "__main__":
    test_approximate_minimal_edge_length()
