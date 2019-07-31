from wknml import parse_nml, write_nml
from wknml.nml_utils import ensure_max_edge_length

def test_ensure_max_edge_length():
    with open("testdata/nml_with_too_long_edges.nml", "r") as file:
        test_nml = parse_nml(file)
    max_length = 2.0
    test_result_nml = ensure_max_edge_length(test_nml, max_length)

    with open("testdata/nml_corrected_long_edges.nml", "r") as file:
        expected_nml = parse_nml(file)

    # need to save and load the test_result_nml since reading applies default values
    # thus this is needed to be able to compare the nmls
    with open("testoutput/max_length_temp.nml", "wb") as file:
        write_nml(file=file, nml=test_result_nml)

    with open("testoutput/max_length_temp.nml", "r") as file:
        test_result_nml = parse_nml(file)

    assert test_result_nml == expected_nml


if __name__ == "__main__":
    test_ensure_max_edge_length()
