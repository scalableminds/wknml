from wknml import parse_nml, compare_nml
from wknml.nml_generation import generate_graph, generate_nml


def test_generate_nml():
    with open("./testdata/nml_with_invalid_ids.nml", "r") as file:
        test_nml = parse_nml(file)

    (graph, parameter_dict) = generate_graph(test_nml)
    test_result_nml = generate_nml(tree_dict=graph, parameters=parameter_dict)

    with open("./testdata/expected_result.nml", "r") as file:
        expected_nml = parse_nml(file)

    assert compare_nml(test_result_nml, expected_nml)


if __name__ == "__main__":
    test_generate_nml()
