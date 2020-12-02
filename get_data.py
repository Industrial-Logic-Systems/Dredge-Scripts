import serial
import json

def listen_on_serial():
    ser = serial.Serial( 'com19', 9600, timeout=20 )
    data = ser.read_until( b'\r' ).strip( b'\n\r' )
    data = data.decode( 'ASCII' )
    return data

def json_from_data(data):
    json_obj = json.loads( data )
    return json_obj

def generate_csv(json_obj):
    csv_obj = []
    # Main Json
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["msg_time"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["vert_correction"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["ch_latitude"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["ch_longitude"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["ch_depth"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["ch_heading"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["slurry_velocity"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["slurry_density"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["pump_rpm"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["vacuum"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["outlet_psi"])
    csv_obj.append(json_obj["DQM_Data"]["messages"][0]["work_event"]["comment"])

    # Non Effective Event
    if "non_eff_event" in json_obj["DQM_Data"]["messages"][0]:
        csv_obj.append(json_obj["DQM_Data"]["messages"][0]["non_eff_event"]["msg_start_time"])
        csv_obj.append(json_obj["DQM_Data"]["messages"][0]["non_eff_event"]["msg_start_time"])
        csv_obj.append(json_obj["DQM_Data"]["messages"][0]["non_eff_event"]["function_code"])
        csv_obj.append(json_obj["DQM_Data"]["messages"][0]["non_eff_event"]["comment"])
    else:
        csv_obj.append('')
        csv_obj.append('')
        csv_obj.append('')
        csv_obj.append('')

    return csv_obj
