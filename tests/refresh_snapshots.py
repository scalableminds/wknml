import wknml
import pickle
from tests.test_snapshot_readandwrite import INPUT_FILES, OUTPUT_FILES, SNAPSHOT_FILES


def save_snapshot_pickle_read_and_write():
    for i in range(0, len(INPUT_FILES)):
        input_file = INPUT_FILES[i]
        output_file = SNAPSHOT_FILES[i]
        parsed = wknml.parse_nml(input_file)
        with open(output_file + ".pickle", "wb") as f:
            pickle.dump(parsed, f)


def save_snapshot_nml_read_and_write():
    for i in range(0, len(INPUT_FILES)):
        input_file = INPUT_FILES[i]
        output_file = OUTPUT_FILES[i]
        parsed = wknml.parse_nml(input_file)
        with open(output_file + ".snapshot", "wb") as f:
            wknml.write_nml(f, parsed)


if __name__ == "__main__":
    save_snapshot_pickle_read_and_write()
    save_snapshot_nml_read_and_write()
