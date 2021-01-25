from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import time
import logging


def getModbus():
    SERVER_HOST = "192.168.1.18"
    SERVER_PORT = 502
    SERVER_U_ID = 1

    c = ModbusClient()

    # uncomment this line to see debug message
    # c.debug(True)

    # define modbus server host, port and unit_id
    c.host(SERVER_HOST)
    c.port(SERVER_PORT)
    c.unit_id(SERVER_U_ID)

    if not c.is_open():
        if not c.open():
            logging.debug("unable to connect to " +
                          SERVER_HOST+":"+str(SERVER_PORT))
            return 0, 0

    offset = c.read_holding_registers(0)
    rot = c.read_holding_registers(1)

    offset = utils.get_2comp(offset[0], 16) / 100
    rot = utils.get_2comp(rot[0], 16) / 100

    logging.debug('Offset: ' + str(offset))
    logging.debug('ROT: ' + str(rot))

    return offset, rot


if __name__ == "__main__":
    offset, rot = getModbus()
    print('Offset:', offset)
    print('ROT:', rot)
