import base64
import binascii
import datetime

from dredge_logger import Log
from dredge_logger.config import config


def test_blank_key():
    # Arrange
    tmpKey = config.vars["program_key"]
    config.vars["program_key"] = ""

    # Act
    result = Log.verify_key()

    # Assert
    assert result is False, result

    # Restore
    config.vars["program_key"] = tmpKey


def test_random_key():
    # Arrange
    tmpKey = config.vars["program_key"]
    config.vars["program_key"] = "sdjfsdjfhsj"

    # Act
    result = Log.verify_key()

    # Assert
    assert result is False, result

    # Restore
    config.vars["program_key"] = tmpKey


def test_passed_date_one_month_key():
    # Arrange
    tmpKey = config.vars["program_key"]
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    date_str = last_month.strftime("%m/%d/%Y")
    new_key = base64.b64encode(date_str.encode("utf-8")).decode("utf-8")
    config.vars["program_key"] = new_key

    # Act
    result = Log.verify_key()

    # Assert
    assert result is False, result

    # Restore
    config.vars["program_key"] = tmpKey


def test_passed_date_key():
    # Arrange
    tmpKey = config.vars["program_key"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    date_str = yesterday.strftime("%m/%d/%Y")
    new_key = base64.b64encode(date_str.encode("utf-8")).decode("utf-8")
    config.vars["program_key"] = new_key

    # Act
    result = Log.verify_key()

    # Assert
    assert result is False, result

    # Restore
    config.vars["program_key"] = tmpKey


def test_future_date_key():
    # Arrange
    tmpKey = config.vars["program_key"]
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    date_str = tomorrow.strftime("%m/%d/%Y")
    new_key = base64.b64encode(date_str.encode("utf-8")).decode("utf-8")
    config.vars["program_key"] = new_key

    # Act
    result = Log.verify_key()

    # Assert
    assert result is True, result

    # Restore
    config.vars["program_key"] = tmpKey


if __name__ == "__main__":
    test_passed_date_one_month_key()
