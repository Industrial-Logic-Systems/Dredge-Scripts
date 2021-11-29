from pathlib import Path
from testUtils import is_equal
import os
import sys

p = os.path.abspath(".")
sys.path.insert(1, p)

import config
import dataHandler


def test_json_parse():
    # Arrange
    j_str = '{"DQM_Data": {"messages": [{"work_event": {"msg_time": "2021-11-28 07:46:07","vert_correction": 1.8,"ch_latitude": 29.614393,"ch_longitude": -94.963516,"ch_depth": 53.42,"ch_heading": 130,"slurry_velocity": 13.44,"slurry_density": 1.8,"pump_rpm": 546,"vacuum": -14.72,"outlet_psi": 69.62,"comment": "comment             "}}]}}'
    # Act
    json_obj = dataHandler.getJson(j_str)
    # Assert
    assert isinstance(json_obj, dict), type(json_obj)


def test_json_parse_ne():
    # Arrange
    j_str = '{"DQM_Data": {"messages": [{"work_event": {"msg_time": "2021-11-28 07:46:17","vert_correction": 1.8,"ch_latitude": 29.614393,"ch_longitude": -94.963516,"ch_depth": 52.7,"ch_heading": 130,"slurry_velocity": 13.36,"slurry_density": 1.8,"pump_rpm": 546,"vacuum": -14.17,"outlet_psi": 70.5,"comment": "comment             "}},{"non_eff_event": {"msg_start_time": "2021-11-28 07:28:05","msg_end_time": "2021-11-28 07:46:09","function_code": "HSL ","comment": "comment             "}}]}}'
    # Act
    json_obj = dataHandler.getJson(j_str)
    # Assert
    assert isinstance(json_obj, dict), type(json_obj)


def test_json_empty():
    # Arrange
    j_str = ""
    # Act
    json_obj = dataHandler.getJson(j_str)
    # Assert
    assert json_obj is None, type(json_obj)


def test_json_incomplete_1():
    # Arrange
    tmpJsonPath = config.json_path
    config.json_path = "Tests\\json_files\\json"
    if os.path.exists(Path("Tests/json_files/failed/failed.txt")):
        os.remove(Path("Tests/json_files/failed/failed.txt"))
    j_str = '{"DQM_Data": {"messages": [{"work_event": {"msg_time": "2021-11-28 07:46:07","vert_correction": 1.8,"ch_latitude": 29.614393,"ch_longitude": -94.963516,"ch_depth": 53.42,"ch_heading": 130,"slurry_velocity": 13.44,"slurry_density": 1.8,"pump_rpm": 546,"vacuum": -14.72,"outlet_psi": 69.62,"comment": "comment             "}}'
    # Act
    json_obj = dataHandler.getJson(j_str)
    # Assert
    assert json_obj is None, type(json_obj)
    result = is_equal(
        Path("Tests/test_files/failed_expected.txt"),
        Path("Tests/json_files/failed/failed.txt"),
        True,
    )
    assert result[0], result[1]
    # Restore
    config.json_path = tmpJsonPath
