import base64
import datetime

from dredge_logger import Log
from dredge_logger.config import config


def test_blank_key():
    # Arrange
    tmpKey = config.vars["program_key"]
    tmpDate = config.vars["last_check_for_update"]
    config.vars["last_check_for_update"] = datetime.date.today()
    config.vars["program_key"] = ""

    # Act
    result = Log.verify_key()

    # Assert
    assert result == [False, False], result

    # Restore
    config.vars["program_key"] = tmpKey
    config.vars["last_check_for_update"] = tmpDate


def test_random_key():
    # Arrange
    tmpKey = config.vars["program_key"]
    tmpDate = config.vars["last_check_for_update"]
    config.vars["last_check_for_update"] = datetime.date.today()
    config.vars["program_key"] = "sdjfsdjfhsj"

    # Act
    result = Log.verify_key()

    # Assert
    assert result == [False, False], result

    # Restore
    config.vars["program_key"] = tmpKey
    config.vars["last_check_for_update"] = tmpDate


def test_passed_date_one_month_key():
    # Arrange
    tmpKey = config.vars["program_key"]
    tmpDate = config.vars["last_check_for_update"]
    config.vars["last_check_for_update"] = datetime.datetime.today()
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    date_str = last_month.strftime("%m/%d/%Y")
    new_key = base64.b64encode(date_str.encode("utf-8")).decode("utf-8")
    config.vars["program_key"] = new_key

    # Act
    result = Log.verify_key()

    # Assert
    assert result == [False, True], result
    assert config.vars["last_check_for_update"] == last_month, f'{config.vars["last_check_for_update"]} == {last_month}'

    # Restore
    config.vars["program_key"] = tmpKey
    config.vars["last_check_for_update"] = tmpDate


def test_passed_date_29_days_key():
    # Arrange
    tmpKey = config.vars["program_key"]
    tmpDate = config.vars["last_check_for_update"]
    config.vars["last_check_for_update"] = datetime.datetime.today()
    last_month = datetime.date.today() - datetime.timedelta(days=29)
    date_str = last_month.strftime("%m/%d/%Y")
    new_key = base64.b64encode(date_str.encode("utf-8")).decode("utf-8")
    config.vars["program_key"] = new_key

    # Act
    result = Log.verify_key()

    # Assert
    assert result == [False, False], result
    assert config.vars["last_check_for_update"] == last_month, f'{config.vars["last_check_for_update"]} == {last_month}'

    # Restore
    config.vars["program_key"] = tmpKey
    config.vars["last_check_for_update"] = tmpDate


def test_passed_date_key():
    # Arrange
    tmpKey = config.vars["program_key"]
    tmpDate = config.vars["last_check_for_update"]
    config.vars["last_check_for_update"] = datetime.datetime.today()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    date_str = yesterday.strftime("%m/%d/%Y")
    new_key = base64.b64encode(date_str.encode("utf-8")).decode("utf-8")
    config.vars["program_key"] = new_key

    # Act
    result = Log.verify_key()
    assert config.vars["last_check_for_update"] == yesterday, f'{config.vars["last_check_for_update"]} == {yesterday}'

    # Assert
    assert result == [False, False], result

    # Restore
    config.vars["program_key"] = tmpKey
    config.vars["last_check_for_update"] = tmpDate


def test_future_date_key():
    # Arrange
    tmpKey = config.vars["program_key"]
    tmpDate = config.vars["last_check_for_update"]
    config.vars["last_check_for_update"] = datetime.date.today() - datetime.timedelta(days=1)
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    date_str = tomorrow.strftime("%m/%d/%Y")
    new_key = base64.b64encode(date_str.encode("utf-8")).decode("utf-8")
    config.vars["program_key"] = new_key

    # Act
    result = Log.verify_key()

    # Assert
    assert result == [True, False], result
    assert (
        config.vars["last_check_for_update"] == datetime.date.today()
    ), f'{config.vars["last_check_for_update"]} == {datetime.date.today()}'

    # Restore
    config.vars["program_key"] = tmpKey
    config.vars["last_check_for_update"] = tmpDate


if __name__ == "__main__":
    test_passed_date_one_month_key()
