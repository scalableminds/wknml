from wknml import parse_nml, write_nml
from wknml.nml_generation import generate_graph, generate_nml
import os

def test_generate_nml():
    with open("testdata/nml_with_invalid_ids.nml", "r") as file:
        test_nml = parse_nml(file)

    (graph, parameter_dict) = generate_graph(test_nml)
    test_result_nml = generate_nml(tree_dict=graph, parameters=parameter_dict)

    with open("testdata/expected_result.nml", "r") as file:
        expected_nml = parse_nml(file)

    # need to save and load the test_result_nml since reading applies default values
    # thus this is needed to be able to compare the nmls
    with open("testoutput/temp.nml", "wb") as file:
        write_nml(file=file, nml=test_result_nml)

    with open("testoutput/temp.nml", "r") as file:
        test_result_nml = parse_nml(file)

    assert test_result_nml == expected_nml


def test_no_default_values_written():
    # read and write the test file
    with open("testdata/nml_without_default_values.nml", "r") as file:
        test_nml = parse_nml(file)
        with open("testoutput/nml_without_default_values.nml", "wb") as output_file:
            write_nml(file=output_file, nml=test_nml)


    # read the written testfile and compare the content
    with open("testdata/nml_without_default_values.nml", "r") as file:
        test_nml = parse_nml(file)
        with open("testoutput/nml_without_default_values.nml", "r") as output_file:
            test_result_nml = parse_nml(output_file)

            assert test_nml == test_result_nml, "The testdata file and the testoutput file do not have the same content."

    # test if both files have the same length
    assert os.path.getsize("testdata/nml_without_default_values.nml") == os.path.getsize("testoutput/nml_without_default_values.nml"), "The testdata file and the testoutput file do not have the same length."

if __name__ == "__main__":
    test_generate_nml()
    test_no_default_values_written()
