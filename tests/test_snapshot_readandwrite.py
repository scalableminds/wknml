import pickle
from pathlib import Path

import wknml
import filecmp
import pytest

OUTPUT_FILES = ["testoutput/dataset.nml", "testoutput/complex_dataset.nml"]
SNAPSHOT_FILES = ["testdata/dataset.nml", "testdata/complex_dataset.nml"]
INPUT_FILES = ["testdata/dataset.fixture.nml", "testdata/complex_dataset.fixture.nml"]


@pytest.fixture(scope="session", autouse=True)
def create_temp_output_directory():
    output_directory = Path("testoutput")
    output_directory.mkdir(exist_ok=True)


def test_read_and_write_and_read():
    for i in range(0, len(INPUT_FILES)):
        input_file = INPUT_FILES[i]
        output_file = OUTPUT_FILES[i]

        first = wknml.parse_nml(input_file)

        with open(output_file, "wb") as f:
            wknml.write_nml(f, first)

        second = wknml.parse_nml(output_file)
        assert first == second


def test_snapshot_read_and_compare_nml():
    for i in range(0, len(INPUT_FILES)):
        input_file = INPUT_FILES[i]
        snapshot_file = SNAPSHOT_FILES[i]
        output_file = OUTPUT_FILES[i]

        parsed = wknml.parse_nml(input_file)

        with open(output_file, "wb") as f:
            wknml.write_nml(f, parsed)

        assert filecmp.cmp(snapshot_file + ".snapshot", output_file)
