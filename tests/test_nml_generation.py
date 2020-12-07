from pathlib import Path
import pickle

import pytest
import filecmp
from wknml import parse_nml, write_nml
from wknml.nml_generation import generate_graph, generate_nml


@pytest.fixture(scope="session", autouse=True)
def create_temp_output_directory():
    output_directory = Path("testoutput")
    output_directory.mkdir(exist_ok=True)


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
    input_file_name = "testdata/nml_without_default_values.nml"
    output_file_name = "testoutput/nml_without_default_values.nml"

    # read and write the test file
    with open(input_file_name, "r") as file:
        test_nml = parse_nml(file)

    with open(output_file_name, "wb") as output_file:
        write_nml(file=output_file, nml=test_nml)

    # read the written testfile and compare the content
    with open(output_file_name, "r") as output_file:
        test_result_nml = parse_nml(output_file)

    assert (
        test_nml == test_result_nml
    ), "The testdata file and the testoutput file do not have the same content."

    # test if both files have the same content
    assert filecmp.cmp(
        input_file_name, output_file_name
    ), "The testdata and the testoutput file do not have the same content."


def test_pickle_serialization():
    # Test if NML objects can be serialized with pickle
    input_file_name = "testdata/nml_without_default_values.nml"
    output_file_name = "testoutput/nml_without_default_values.nml.pickle"

    with open(input_file_name, "r") as file:
        test_nml = parse_nml(file)

    with open(output_file_name, "wb") as outfile:
        pickle.dump(test_nml, outfile)

    assert True
