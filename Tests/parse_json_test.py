import os
from pathlib import Path

from dredge_logger import dataHandler
from dredge_logger.config import config

from Tests.testUtils import is_equal


def test_json_parse():
    # Arrange
    j_str = '{"DQM_Data": {"messages": [{"work_event": {"msg_time": "2021-11-28 07:46:07","vert_correction": 1.8,"ch_latitude\
": 29.614393,"ch_longitude": -94.963516,"ch_depth": 53.42,"ch_heading": 130,"slurry_velocity": 13.44,"slurry_density"\
: 1.8,"pump_rpm": 546,"vacuum": -14.72,"outlet_psi": 69.62,"comment": "comment             "}}]}}'
    j_obj = {
        "DQM_Data": {
            "messages": [
                {
                    "work_event": {
                        "msg_time": "2021-11-28 07:46:07",
                        "vert_correction": 1.8,
                        "ch_latitude": 29.614393,
                        "ch_longitude": -94.963516,
                        "ch_depth": 53.42,
                        "ch_heading": 130,
                        "slurry_velocity": 13.44,
                        "slurry_density": 1.8,
                        "pump_rpm": 546,
                        "vacuum": -14.72,
                        "outlet_psi": 69.62,
                        "comment": "comment             ",
                    }
                }
            ]
        }
    }
    c_obj = [
        "2021-11-28 07:46:07",
        1.8,
        29.614393,
        -94.963516,
        53.42,
        130,
        13.44,
        1.8,
        546,
        -14.72,
        69.62,
        "comment",
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
    json_obj = dataHandler.getJSON(j_str)
    csv_obj = dataHandler.getCSV(json_obj, False)
    # Assert
    assert isinstance(json_obj, dict), type(json_obj)
    assert isinstance(csv_obj, tuple), type(csv_obj)
    assert isinstance(csv_obj[0], list), type(csv_obj[0])
    assert isinstance(csv_obj[1], dict), type(csv_obj[1])
    assert not csv_obj[1], f"Modbus values returned, when none were expected: {csv_obj[1]}"
    assert json_obj == j_obj, "JSON object is not equal"
    assert csv_obj[0] == c_obj, "CSV object is not equal"


def test_json_parse_ne():
    # Arrange
    j_str = '{"DQM_Data": {"messages": [{"work_event": {"msg_time": "2021-11-28 07:46:17","vert_correction": 1.8,"ch_latitude\
": 29.614393,"ch_longitude": -94.963516,"ch_depth": 52.7,"ch_heading": 130,"slurry_velocity": 13.36,"slurry_density":\
1.8,"pump_rpm": 546,"vacuum": -14.17,"outlet_psi": 70.5,"comment": "comment             "}},{"non_eff_event": {"m\
sg_start_time": "2021-11-28 07:28:05","msg_end_time": "2021-11-28 07:46:09","function_code": "HSL ","comment"\
: "comment             "}}]}}'
    j_obj = {
        "DQM_Data": {
            "messages": [
                {
                    "work_event": {
                        "msg_time": "2021-11-28 07:46:17",
                        "vert_correction": 1.8,
                        "ch_latitude": 29.614393,
                        "ch_longitude": -94.963516,
                        "ch_depth": 52.7,
                        "ch_heading": 130,
                        "slurry_velocity": 13.36,
                        "slurry_density": 1.8,
                        "pump_rpm": 546,
                        "vacuum": -14.17,
                        "outlet_psi": 70.5,
                        "comment": "comment             ",
                    }
                },
                {
                    "non_eff_event": {
                        "msg_start_time": "2021-11-28 07:28:05",
                        "msg_end_time": "2021-11-28 07:46:09",
                        "function_code": "HSL ",
                        "comment": "comment             ",
                    }
                },
            ]
        }
    }

    c_obj = [
        "2021-11-28 07:46:17",
        1.8,
        29.614393,
        -94.963516,
        52.7,
        130,
        13.36,
        1.8,
        546,
        -14.17,
        70.5,
        "comment",
        "2021-11-28 07:28:05",
        "2021-11-28 07:46:09",
        "HSL",
        "comment",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]
    # Act
    json_obj = dataHandler.getJSON(j_str)
    csv_obj = dataHandler.getCSV(json_obj, False)
    # Assert
    assert isinstance(json_obj, dict), type(json_obj)
    assert isinstance(csv_obj, tuple), type(csv_obj)
    assert isinstance(csv_obj[0], list), type(csv_obj[0])
    assert isinstance(csv_obj[1], dict), type(csv_obj[1])
    assert not csv_obj[1], f"Modbus values returned, when none were expected: {csv_obj[1]}"
    assert json_obj == j_obj, "JSON object is not equal"
    assert csv_obj[0] == c_obj, "CSV object is not equal"


def test_json_parse_of():
    # Arrange
    j_str = '{"DQM_Data": {"messages": [{"work_event": {"msg_time": "2021-11-28 07:46:07","vert_correction": 1.8,"ch_latitude\
": 29.614393,"ch_longitude": -94.963516,"ch_depth": 53.42,"ch_heading": 130,"slurry_velocity": 13.44,"slurry_density": 1.8,"p\
ump_rpm": 546,"vacuum": -14.72,"outlet_psi": 69.62,"comment": "comment             "}},{"outfall_position": {"msg_time": "202\
1-11-28 07:46:07","outfall_location": "Shore","outfall_latitude": 29.614393,"outfall_longitude": -94.963516,"outfall_heading"\
: 142,"outfall_elevation": 10.1,"comment": "comment             "}}]}}'
    j_obj = {
        "DQM_Data": {
            "messages": [
                {
                    "work_event": {
                        "msg_time": "2021-11-28 07:46:07",
                        "vert_correction": 1.8,
                        "ch_latitude": 29.614393,
                        "ch_longitude": -94.963516,
                        "ch_depth": 53.42,
                        "ch_heading": 130,
                        "slurry_velocity": 13.44,
                        "slurry_density": 1.8,
                        "pump_rpm": 546,
                        "vacuum": -14.72,
                        "outlet_psi": 69.62,
                        "comment": "comment             ",
                    }
                },
                {
                    "outfall_position": {
                        "msg_time": "2021-11-28 07:46:07",
                        "outfall_location": "Shore",
                        "outfall_latitude": 29.614393,
                        "outfall_longitude": -94.963516,
                        "outfall_heading": 142,
                        "outfall_elevation": 10.1,
                        "comment": "comment             ",
                    }
                },
            ]
        }
    }
    c_obj = [
        "2021-11-28 07:46:07",
        1.8,
        29.614393,
        -94.963516,
        53.42,
        130,
        13.44,
        1.8,
        546,
        -14.72,
        69.62,
        "comment",
        "",
        "",
        "",
        "",
        "2021-11-28 07:46:07",
        "Shore",
        29.614393,
        -94.963516,
        142,
        10.1,
        "comment",
    ]
    # Act
    json_obj = dataHandler.getJSON(j_str)
    csv_obj = dataHandler.getCSV(json_obj, False)
    # Assert
    assert isinstance(json_obj, dict), type(json_obj)
    assert isinstance(csv_obj, tuple), type(csv_obj)
    assert isinstance(csv_obj[0], list), type(csv_obj[0])
    assert isinstance(csv_obj[1], dict), type(csv_obj[1])
    assert not csv_obj[1], f"Modbus values returned, when none were expected: {csv_obj[1]}"
    assert json_obj == j_obj, "JSON object is not equal"
    assert csv_obj[0] == c_obj, "CSV object is not equal"


def test_json_empty():
    # Arrange
    j_str = ""
    # Act
    json_obj = dataHandler.getJSON(j_str)
    # Assert
    assert json_obj is None, type(json_obj)


def test_json_incomplete_1():
    # Arrange
    tmpJsonPath = config.vars["json_path"]
    config.vars["json_path"] = "Tests\\json_files\\json"
    if os.path.exists(Path("Tests/json_files/failed/failed.txt")):
        os.remove(Path("Tests/json_files/failed/failed.txt"))
    j_str = '{"DQM_Data": {"messages": [{"work_event": {"msg_time": "2021-11-28 07:46:07","vert_correction": 1.8,"ch_latitude\
": 29.614393,"ch_longitude": -94.963516,"ch_depth": 53.42,"ch_heading": 130,"slurry_velocity": 13.44,"slurry_density"\
: 1.8,"pump_rpm": 546,"vacuum": -14.72,"outlet_psi": 69.62,"comment": "comment             "}}'
    # Act
    json_obj = dataHandler.getJSON(j_str)
    # Assert
    assert json_obj is None, type(json_obj)
    result = is_equal(
        Path("Tests/test_files/failed_json_expected.txt"),
        Path("Tests/json_files/failed/failed.txt"),
        True,
    )
    assert result[0], result[1]
    # Restore
    config.vars["json_path"] = tmpJsonPath


def test_json_csv_parse_missing_data():
    # Arrange
    tmpDredgeType = config.vars["dredge_type"]
    config.vars["dredge_type"] = "pipeline"
    j_obj = {}
    # Act
    csv_obj = dataHandler.getCSV(j_obj, False)
    # Assert
    assert isinstance(csv_obj, tuple), type(csv_obj)
    assert csv_obj[0] is None, type(csv_obj[0])
    assert csv_obj[1] is None, type(csv_obj[1])
    # Restore
    config.vars["dredge_type"] = tmpDredgeType
