import os
from pathlib import Path
from Tests.testUtils import is_equal


from dredge_logger.config import config
from dredge_logger import fileHandler


def test_csv_write():
    # Arrange
    tmpHeader = config.vars["header"]
    config.vars["header"] = ["Value 1", "Value 2", "Value 3"]
    filepath = Path("Tests/csv_files/test_write.csv")
    if os.path.exists(filepath):
        os.remove(filepath)
    data = ["This is a string", 10, 3.14]

    # Act
    fileHandler.write_file(filepath.parent, filepath.name, data)

    # Assert
    result = is_equal(Path("Tests/test_files/test_write_expected.csv"), filepath, True)
    assert result[0], result[1]

    # Restore
    config.vars["header"] = tmpHeader


def test_csv_header_change_1():
    # Arrange
    tmpHeader = config.vars["header"]
    config.vars["header"] = ["Value 1", "Value 2", "Value 3"]
    filepath = Path("Tests/csv_files/test_header_change_1.csv")
    if os.path.exists(filepath):
        os.remove(filepath)
    data = ["This is a string", 10, 3.14]

    # Act
    fileHandler.write_file(filepath.parent, filepath.name, data)
    config.vars["header"] = ["Value 1", "Value 2", "Value 3", "Value 4"]
    data.append("123.456")
    fileHandler.write_file(filepath.parent, filepath.name, data)

    # Assert
    result = is_equal(
        Path("Tests/test_files/test_header_change_1_expected.csv"), filepath, True
    )
    assert result[0], result[1]

    # Restore
    config.vars["header"] = tmpHeader


def test_csv_header_change_2():
    # Arrange
    tmpHeader = config.vars["header"]
    config.vars["header"] = ["Value 1", "Value 2", "Value 3"]
    filepath = Path("Tests/csv_files/test_header_change_2.csv")
    if os.path.exists(filepath):
        os.remove(filepath)
    data = ["This is a string", 10, 3.14]

    # Act
    fileHandler.write_file(filepath.parent, filepath.name, data)
    config.vars["header"] = ["Value 1", "Value 2", "Value 4", "Value 3"]
    data = ["This is a string", 10, 123.456, 3.14]
    fileHandler.write_file(filepath.parent, filepath.name, data)

    # Assert
    result = is_equal(
        Path("Tests/test_files/test_header_change_2_expected.csv"), filepath, True
    )
    assert result[0], result[1]

    # Restore
    config.vars["header"] = tmpHeader


def test_csv_header_change_3():
    # Arrange
    tmpHeader = config.vars["header"]
    config.vars["header"] = [
        "msg_time",
        "vert_correction",
        "ch_latitude",
        "ch_longitude",
        "ch_depth",
        "ch_heading",
        "slurry_velocity",
        "slurry_density",
        "pump_rpm",
        "vacuum",
        "outlet_psi",
        "comment",
        "offset",
        "rot",
        "stack_temp",
        "swing_pressure",
        "cutter_pressure",
        "vacuum_break",
        "msg_start_time",
        "msg_end_time",
        "function_code",
        "comment_ne",
        "msg_time_of",
        "outfall_location",
        "outfall_latitude",
        "outfall_longitude",
        "outfall_heading",
        "outfall_elevation",
        "comment_of",
    ]
    filepath = Path("Tests/csv_files/test_header_change_3.csv")
    if os.path.exists(filepath):
        os.remove(filepath)
    data = [
        "2021-11-28 05:58:53",
        1.4,
        29.614471,
        -94.963593,
        50.79,
        111,
        12.77,
        1.8,
        546,
        -12.62,
        72.8,
        "comment",
        505.05,
        0.0,
        278.38,
        811.34,
        3000.0,
        False,
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]

    # Act
    fileHandler.write_file(filepath.parent, filepath.name, data)
    config.vars["header"] = [
        "msg_time",
        "vert_correction",
        "ch_latitude",
        "ch_longitude",
        "ch_depth",
        "ch_heading",
        "slurry_velocity",
        "slurry_density",
        "pump_rpm",
        "vacuum",
        "outlet_psi",
        "comment",
        "offset",
        "rot",
        "stack_temp",
        "swing_pressure",
        "cutter_pressure",
        "new_value",
        "vacuum_break",
        "msg_start_time",
        "msg_end_time",
        "function_code",
        "comment_ne",
        "msg_time_of",
        "outfall_location",
        "outfall_latitude",
        "outfall_longitude",
        "outfall_heading",
        "outfall_elevation",
        "comment_of",
    ]
    data = [
        "2021-11-28 05:59:03",
        1.4,
        29.614479,
        -94.963593,
        50.77,
        109,
        12.87,
        1.8,
        546,
        -12.69,
        72.95,
        "comment",
        506.7,
        0.0,
        278.38,
        798.75,
        3000.0,
        100,
        False,
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]
    fileHandler.write_file(filepath.parent, filepath.name, data)

    # Assert
    result = is_equal(
        Path("Tests/test_files/test_header_change_3_expected.csv"), filepath, True
    )
    assert result[0], result[1]

    # Restore
    config.vars["header"] = tmpHeader


if __name__ == "__main__":
    test_csv_write()
