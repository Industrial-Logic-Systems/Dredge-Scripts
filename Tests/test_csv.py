import os
import sys
from pathlib import Path

p = os.path.abspath(".")
sys.path.insert(1, p)

import config
import fileHandler


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
    with open(filepath, "r") as f:
        assert (
            f.readline() == "Value 1,Value 2,Value 3\n"
        ), "Header not written correctly"
        assert (
            f.readline() == "This is a string,10,3.14\n"
        ), "Data not written correctly"

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
    with open(filepath, "r") as f:
        assert (
            f.readline() == "Value 1,Value 2,Value 3,Value 4\n"
        ), "Header not written correctly"
        assert (
            f.readline() == "This is a string,10,3.14,\n"
        ), "Data line 1 not written correctly"
        assert (
            f.readline() == "This is a string,10,3.14,123.456\n"
        ), "Data line 2 not written correctly"

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
    with open(filepath, "r") as f:
        assert (
            f.readline() == "Value 1,Value 2,Value 4,Value 3\n"
        ), "Header not written correctly"
        assert (
            f.readline() == "This is a string,10,,3.14\n"
        ), "Data line 1 not written correctly"
        assert (
            f.readline() == "This is a string,10,123.456,3.14\n"
        ), "Data line 2 not written correctly"

    # Restore
    config.header = tmpHeader


if __name__ == "__main__":
    test_csv_header_change_1()
