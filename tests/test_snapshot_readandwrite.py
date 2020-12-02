import wknml
import pickle
import filecmp

OUTPUT_FILES = ["testoutput/dataset.nml", "testoutput/complex_dataset.nml"]
SNAPSHOT_FILES = ["testdata/dataset.nml", "testdata/complex_dataset.nml"]
INPUT_FILES = ["testdata/dataset.fixture.nml", "testdata/complex_dataset.fixture.nml"]


def test_read_and_write_and_read():
    for i in range(0, len(INPUT_FILES)):
        input_file = INPUT_FILES[i]
        output_file = OUTPUT_FILES[i]
        first = wknml.parse_nml(input_file)
        with open(output_file, "wb") as f:
            wknml.write_nml(f, first)
        second = wknml.parse_nml(output_file)
        assert first == second


def test_snapshot_read_and_compare_pickle():
    for i in range(0, len(INPUT_FILES)):
        input_file = INPUT_FILES[i]
        snapshot_file = SNAPSHOT_FILES[i]
        output_file = OUTPUT_FILES[i]
        parsed = wknml.parse_nml(input_file)
        with open(output_file + ".pickle.cmp", "wb") as f:
            pickle.dump(parsed, f)
        assert filecmp.cmp(snapshot_file + ".pickle", output_file + ".pickle.cmp")


def test_snapshot_read_and_compare_nml():
    for i in range(0, len(INPUT_FILES)):
        input_file = INPUT_FILES[i]
        snapshot_file = SNAPSHOT_FILES[i]
        output_file = OUTPUT_FILES[i]
        parsed = wknml.parse_nml(input_file)
        with open(output_file, "wb") as f:
            wknml.write_nml(f, parsed)
        assert filecmp.cmp(snapshot_file + ".snapshot", output_file)
