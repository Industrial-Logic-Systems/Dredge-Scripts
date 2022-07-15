import datetime
import os
from pathlib import Path

from dredge_logger import dataHandler
from dredge_logger import Log
from dredge_logger.config import config

from tests.testUtils import is_equal


def test_save_hopper():
    # Arrange
    tmpDredgeType = config.vars["dredge_type"]
    tmpXML_Path = config.vars["xml_path"]
    tmpCSV_path = config.vars["csv_path"]
    tmp_csv0600 = config.vars["csv0600"]

    config.vars["dredge_type"] = "hopper"
    config.vars["xml_path"] = Path("tests/xml_files")
    config.vars["csv_path"] = Path("tests/csv_files")
    config.vars["csv0600"] = False

    filename = str(datetime.datetime.today().strftime("%Y-%m-%d"))

    if os.path.isfile(config.vars["xml_path"] / (filename + ".xml_bak")):
        os.remove(config.vars["xml_path"] / (filename + ".xml_bak"))
    if os.path.isfile(config.vars["csv_path"] / (filename + ".csv")):
        os.remove(config.vars["csv_path"] / (filename + ".csv"))

    xml_str = '<?xml version="1.0"?><HOPPER_DREDGING_DATA version="2.0"><DREDGE_NAME>EJE</DREDGE_NAME><HOPPER_DATA_RECORD><DA\
TE_TIME>0                  </DATE_TIME><CONTRACT_NUMBER>0                   </CONTRACT_NUMBER><LOAD_NUMBER>0    </LOAD_NUMBER\
><VESSEL_X coord_type="LL">0.000000   </VESSEL_X><VESSEL_Y coord_type="LL">0.000000   </VESSEL_Y><PORT_DRAG_X coord_type="LL"\
>0.000000   </PORT_DRAG_X><PORT_DRAG_Y coord_type="LL">0.000000   </PORT_DRAG_Y><STBD_DRAG_X coord_type="LL">0.000000   </STB\
D_DRAG_X><STBD_DRAG_Y coord_type="LL">0.000000   </STBD_DRAG_Y><HULL_STATUS>0     </HULL_STATUS><VESSEL_COURSE>0  </VESSEL_CO\
URSE><VESSEL_SPEED>0.0  </VESSEL_SPEED><VESSEL_HEADING>0  </VESSEL_HEADING><TIDE>0     </TIDE><DRAFT_FORE>0.00  </DRAFT_FORE>\
<DRAFT_AFT>0.00  </DRAFT_AFT><ULLAGE_FORE>0.00  </ULLAGE_FORE><ULLAGE_AFT>0.00  </ULLAGE_AFT><HOPPER_VOLUME>0    </HOPPER_VOL\
UME><DISPLACEMENT>0    </DISPLACEMENT><EMPTY_DISPLACEMENT>0    </EMPTY_DISPLACEMENT><DRAGHEAD_DEPTH_PORT>0.0  </DRAGHEAD_DEPT\
H_PORT><DRAGHEAD_DEPTH_STBD>0.0  </DRAGHEAD_DEPTH_STBD><PORT_DENSITY>0.000  </PORT_DENSITY><STBD_DENSITY>0.000  </STBD_DENSIT\
Y><PORT_VELOCITY>0.00  </PORT_VELOCITY><STBD_VELOCITY>0.00  </STBD_VELOCITY><PUMP_RPM_PORT>0   </PUMP_RPM_PORT><PUMP_RPM_STBD\
>0   </PUMP_RPM_STBD></HOPPER_DATA_RECORD></HOPPER_DREDGING_DATA>'
    xml_obj = dataHandler.getXML(xml_str)
    csv_obj = dataHandler.getCSV(xml_obj, False)

    # Act
    Log.saveFiles(xml_str, csv_obj)

    result_1 = is_equal(Path("tests/test_files/test_save_hopper.xml"), config.vars["xml_path"] / (filename + ".xml_bak"), True)
    result_2 = is_equal(Path("tests/test_files/test_save_hopper.csv"), config.vars["csv_path"] / (filename + ".csv"), True)

    # Assert
    assert result_1[0], result_1[1]
    assert result_2[0], result_2[1]

    # Restore
    if os.path.isfile(config.vars["xml_path"] / (filename + ".xml_bak")):
        os.remove(config.vars["xml_path"] / (filename + ".xml_bak"))
    if os.path.isfile(config.vars["csv_path"] / (filename + ".csv")):
        os.remove(config.vars["csv_path"] / (filename + ".csv"))
    config.vars["dredge_type"] = tmpDredgeType
    config.vars["xml_path"] = tmpXML_Path
    config.vars["csv_path"] = tmpCSV_path
    config.vars["csv0600"] = tmp_csv0600


def test_save_pipeline():
    # Arrange
    tmpDredgeType = config.vars["dredge_type"]
    tmpJSON_Path = config.vars["json_path"]
    tmpCSV_path = config.vars["csv_path"]
    tmp_csv0600 = config.vars["csv0600"]
    tmp_csv0600_saved = config.vars["csv0600_saved"]

    config.vars["dredge_type"] = "pipeline"
    config.vars["json_path"] = Path("tests/json_files")
    config.vars["csv_path"] = Path("tests/csv_files")
    config.vars["csv0600"] = True
    config.vars["csv0600_saved"] = False

    filename = str(datetime.datetime.today().strftime("%Y-%m-%d"))

    if os.path.isfile(config.vars["json_path"] / (filename + ".json")):
        os.remove(config.vars["json_path"] / (filename + ".json"))
    if os.path.isfile(config.vars["csv_path"] / (filename + ".csv")):
        os.remove(config.vars["csv_path"] / (filename + ".csv"))
    if os.path.isfile(config.vars["csv_path"] / (filename + "_0600.csv")):
        os.remove(config.vars["csv_path"] / (filename + "_0600.csv"))

    json_str = '{"DQM_Data": {"messages": [{"work_event": {"msg_time": "2021-11-28 07:46:07","vert_correction": 1.8,"ch_latit\
ude": 29.614393,"ch_longitude": -94.963516,"ch_depth": 53.42,"ch_heading": 130,"slurry_velocity": 13.44,"slurry_density": 1.8\
,"pump_rpm": 546,"vacuum": -14.72,"outlet_psi": 69.62,"comment": "comment             "}},{"outfall_position": {"msg_time": "\
2021-11-28 07:46:07","outfall_location": "Shore","outfall_latitude": 29.614393,"outfall_longitude": -94.963516,"outfall_headi\
ng": 142,"outfall_elevation": 10.1,"comment": "comment             "}}]}}'
    json_obj = dataHandler.getJSON(json_str)
    csv_obj = dataHandler.getCSV(json_obj, False)

    # Act
    Log.saveFiles(json_str, csv_obj)

    result_1 = is_equal(
        Path("tests/test_files/test_save_pipeline.json"), config.vars["json_path"] / (filename + ".json"), True
    )
    result_2 = is_equal(Path("tests/test_files/test_save_pipeline.csv"), config.vars["csv_path"] / (filename + ".csv"), True)
    result_3 = is_equal(
        Path("tests/test_files/test_save_pipeline_0600.csv"), config.vars["csv_path"] / (filename + "_0600.csv"), True
    )

    # Assert
    assert result_1[0], result_1[1]
    assert result_2[0], result_2[1]
    assert result_3[0], result_3[1]

    # Restore
    if os.path.isfile(config.vars["json_path"] / (filename + ".json")):
        os.remove(config.vars["json_path"] / (filename + ".json"))
    if os.path.isfile(config.vars["csv_path"] / (filename + ".csv")):
        os.remove(config.vars["csv_path"] / (filename + ".csv"))
    if os.path.isfile(config.vars["csv_path"] / (filename + "_0600.csv")):
        os.remove(config.vars["csv_path"] / (filename + "_0600.csv"))
    config.vars["dredge_type"] = tmpDredgeType
    config.vars["json_path"] = tmpJSON_Path
    config.vars["csv_path"] = tmpCSV_path
    config.vars["csv0600"] = tmp_csv0600
    config.vars["csv0600_saved"] = tmp_csv0600_saved


if __name__ == "__main__":
    test_save_hopper()
