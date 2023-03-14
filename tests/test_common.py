from backend.common import DBClass, coordinates_to_words, words_to_coordinates
from backend.main import Backend
from custom.exceptions import NoKeyError
from pytest import raises, mark
from unittest.mock import patch
from sqlite3 import OperationalError


@mark.parametrize("no_key_resp", [("InvalidKey"), ("MissingKey")])
@patch("backend.common.json.loads")
def test_error_raised_when_no_key_co_ords(
    mock_response: patch, no_key_resp: str
):
    """test error raised when no key"""
    mock_response.return_value = {"error": {"code": no_key_resp}}
    """test error raised when no key"""
    with raises(NoKeyError):
        coordinates_to_words("1.1", "1.1")


@mark.parametrize("no_key_resp", [("InvalidKey"), ("MissingKey")])
@patch("backend.common.json.loads")
def test_error_raised_when_no_key_words(
    mock_response: patch, no_key_resp: str
):
    """test error raised when no key"""
    mock_response.return_value = {"error": {"code": no_key_resp}}
    """test error raised when no key"""
    with raises(NoKeyError):
        words_to_coordinates("test.test.test")


@patch("backend.common.json.loads")
def test_error_raised_when_bad_co_ords(mock_response: patch):
    """test error raised when bad co ords"""
    mock_response.return_value = {"error": {"code": "BadCoordinates"}}
    """test error raised when bad co ords"""
    with raises(ValueError):
        coordinates_to_words("1.1", "1.1h")


@patch("backend.common.json.loads")
def test_error_raised_when_unknown_error_co_ords(mock_response: patch):
    """test error raised when unknown error"""
    mock_response.return_value = {"error": {"code": "UnknownError"}}
    """test error raised when unknown error"""
    with raises(Exception):
        coordinates_to_words("1.1", "1.1")


@patch("backend.common.json.loads")
def test_error_raised_when_unknown_error_words(mock_response: patch):
    """test error raised when unknown error"""
    mock_response.return_value = {"error": {"code": "UnknownError"}}
    """test error raised when unknown error"""
    with raises(Exception):
        words_to_coordinates("test.test.test")


def test_execute_sql_fail():
    """test execute sql fail"""
    db = DBClass()
    with raises(OperationalError):
        db.execute_sql("SELECT * FROM test")


def test_init_tables():
    """test init tables"""
    Backend().init_db()
    db = DBClass()
    assert (
        db.execute_sql(
            """SELECT name FROM sqlite_schema
          WHERE type ='table' AND
            name NOT LIKE 'sqlite_%';"""
        )
        == [("orders",), ("menu_items",), ("order_items",)]
    )
