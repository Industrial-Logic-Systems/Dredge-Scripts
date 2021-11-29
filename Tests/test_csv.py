import os
import sys
from pathlib import Path
import subprocess

p = os.path.abspath(".")
sys.path.insert(1, p)

import config
import fileHandler


def is_equal(expected, actual_file):
    with open(expected) as f1:
        with open(actual_file) as f2:
            if f1.read() == f2.read():
                return (True, "")
    try:
        result = subprocess.check_output(
            f"diff {expected} {actual_file}", stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        result = e.output
    return (False, result.decode("utf-8"))
    return (False, result.decode("utf-8"))


def test_csv_write():
    # Arrange
    tmpHeader = config.header
    config.header = ["Value 1", "Value 2", "Value 3"]
    filepath = Path("Tests/csv_files/test_write.csv")
    if os.path.exists(filepath):
        os.remove(filepath)
    data = ["This is a string", 10, 3.14]

    # Act
    fileHandler.write_file(filepath.parent, filepath.name, data)

    # Assert
    result = is_equal(Path("Tests/test_files/test_write_expected.csv"), filepath)
    assert result[0], result[1]

    # Restore
    config.header = tmpHeader


def test_csv_header_change_1():
    # Arrange
    tmpHeader = config.header
    config.header = ["Value 1", "Value 2", "Value 3"]
    filepath = Path("Tests/csv_files/test_header_change_1.csv")
    if os.path.exists(filepath):
        os.remove(filepath)
    data = ["This is a string", 10, 3.14]

    # Act
    fileHandler.write_file(filepath.parent, filepath.name, data)
    config.header = ["Value 1", "Value 2", "Value 3", "Value 4"]
    data.append("123.456")
    fileHandler.write_file(filepath.parent, filepath.name, data)

    # Assert
    result = is_equal(
        Path("Tests/test_files/test_header_change_1_expected.csv"), filepath
    )
    assert result[0], result[1]

    # Restore
    config.header = tmpHeader


def test_csv_header_change_2():
    # Arrange
    tmpHeader = config.header
    config.header = ["Value 1", "Value 2", "Value 3"]
    filepath = Path("Tests/csv_files/test_header_change_2.csv")
    if os.path.exists(filepath):
        os.remove(filepath)
    data = ["This is a string", 10, 3.14]

    # Act
    fileHandler.write_file(filepath.parent, filepath.name, data)
    config.header = ["Value 1", "Value 2", "Value 4", "Value 3"]
    data = ["This is a string", 10, 123.456, 3.14]
    fileHandler.write_file(filepath.parent, filepath.name, data)

    # Assert
    result = is_equal(
        Path("Tests/test_files/test_header_change_2_expected.csv"), filepath
    )
    assert result[0], result[1]

    # Restore
    config.header = tmpHeader


if __name__ == "__main__":
    result = is_equal("Tests/Test_Files/test1.txt", "Tests/Test_Files/test2.txt")
    print(result[0], result[1])
