import os
import xml.etree.ElementTree as ET
from pathlib import Path

from dredge_logger import dataHandler
from dredge_logger.config import config

from Tests.testUtils import is_equal


def test_xml_parse():
    # Arrange
    tmpDredgeType = config.vars["dredge_type"]
    config.vars["dredge_type"] = "hopper"
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
    c_obj = [
        "EJE",
        "0                  ",
        "0                   ",
        "0    ",
        "0.000000   ",
        "0.000000   ",
        "0.000000   ",
        "0.000000   ",
        "0.000000   ",
        "0.000000   ",
        "0     ",
        "0  ",
        "0.0  ",
        "0  ",
        "0     ",
        "0.00  ",
        "0.00  ",
        "0.00  ",
        "0.00  ",
        "0    ",
        "0    ",
        "0    ",
        "0.0  ",
        "0.0  ",
        "0.000  ",
        "0.000  ",
        "0.00  ",
        "0.00  ",
        "0   ",
        "0   ",
    ]
    # Act
    xml_obj = dataHandler.getXML(xml_str)
    csv_obj = dataHandler.getCSV(xml_obj, False)
    # Assert
    assert isinstance(xml_obj, ET.Element), type(xml_obj)
    assert isinstance(csv_obj, tuple), type(csv_obj)
    assert isinstance(csv_obj[0], list), type(csv_obj[0])
    assert isinstance(csv_obj[1], dict), type(csv_obj[1])
    assert not csv_obj[1], f"Modbus values returned, when none were expected: {csv_obj[1]}"
    assert csv_obj[0] == c_obj, "CSV object is not equal"
    # Restore
    config.vars["dredge_type"] = tmpDredgeType


def test_xml_empty():
    # Arrange
    xml_str = ""
    # Act
    xml_obj = dataHandler.getXML(xml_str)
    # Assert
    assert xml_obj is None, type(xml_obj)


def test_xml_incomplete_1():
    # Arrange
    tmpXMLPath = config.vars["xml_path"]
    config.vars["xml_path"] = "Tests\\xml_files\\xml"
    if os.path.exists(Path("Tests/xml_files/failed/failed.txt")):
        os.remove(Path("Tests/xml_files/failed/failed.txt"))
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
>0   </PUMP_RPM_STBD></HOPPER_DREDGING_DATA>'
    # Act
    xml_obj = dataHandler.getXML(xml_str)
    # Assert
    assert xml_obj is None, type(xml_obj)
    result = is_equal(
        Path("Tests/test_files/failed_xml_expected_1.txt"),
        Path("Tests/xml_files/failed/failed.txt"),
        True,
    )
    assert result[0], result[1]
    # Restore
    config.vars["xml_path"] = tmpXMLPath


def test_xml_incomplete_2():
    # Arrange
    tmpXMLPath = config.vars["xml_path"]
    config.vars["xml_path"] = "Tests\\xml_files\\xml"
    if os.path.exists(Path("Tests/xml_files/failed/failed.txt")):
        os.remove(Path("Tests/xml_files/failed/failed.txt"))
    xml_str = '<?xml version="1.0"?><DREDGE_NAME>EJE</DREDGE_NAME><HOPPER_DATA_RECORD><DA\
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
    # Act
    xml_obj = dataHandler.getXML(xml_str)
    # Assert
    assert xml_obj is None, type(xml_obj)
    result = is_equal(
        Path("Tests/test_files/failed_xml_expected_2.txt"),
        Path("Tests/xml_files/failed/failed.txt"),
        True,
    )
    assert result[0], result[1]
    # Restore
    config.vars["xml_path"] = tmpXMLPath


def test_xml_csv_parse_missing_data():
    # Arrange
    tmpDredgeType = config.vars["dredge_type"]
    config.vars["dredge_type"] = "hopper"
    xml_str = '<?xml version="1.0"?><HOPPER_DREDGING_DATA version="2.0"><HOPPER_DATA_RECORD></HOPPER_DATA_RECORD></HOPPER_DRE\
DGING_DATA>'
    xml_obj = dataHandler.getXML(xml_str)
    # Act
    csv_obj = dataHandler.getCSV(xml_obj, False)
    # Assert
    assert isinstance(csv_obj, tuple), type(csv_obj)
    assert csv_obj[0] is None, type(csv_obj[0])
    assert csv_obj[1] is None, type(csv_obj[1])

    # Restore
    config.vars["dredge_type"] = tmpDredgeType
