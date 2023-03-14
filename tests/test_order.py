from unittest.mock import patch
from pytest import raises
from backend.main import Backend
from custom.exceptions import NoKeyError
import os

# TODO: setup and teardown
# TODO: more exceptions!
# TODO: better logging of the whole thing

backend = Backend()


@patch("backend.order.datetime")
def test_order_with_args(mock_time: patch):
    """test order with args"""
    if os.getenv("THREEWORDS_SUBSCRIPTION_KEY") is None:
        print("please input api key!!!")
        with raises(NoKeyError):
            order = backend.new_order("mike", "51.521251,-0.203586")
            order.location_words
    else:
        mock_time.utcnow.return_value = "test"
        order = backend.new_order("mike", "51.521251,-0.203586")
        order.set_order_date()
        assert isinstance(order.order_id, int) # can only assert type
        assert order.customer == "mike"
        assert order.location_words == "index.home.raft"
        assert order.date == "test"


def test_save():
    """test save"""
    if os.getenv("THREEWORDS_SUBSCRIPTION_KEY") is None:
        print("please input api key!!!")
        with raises(NoKeyError):
            order = backend.new_order("mike", "51.521251,-0.203586")
            order.set_order_date()
            order.save()
    else:
        order = backend.new_order("mike", "51.521251,-0.203586")
        order.set_order_date()
        global id  # to test existing order
        id = order.order_id
        global date_time
        date_time = order.date  # to test existing order
        order.save()
        assert (
            id,
            "mike",
            "index.home.raft",
            order.date.strftime("%Y-%m-%d %H:%M:%S.%f"),
        ) in backend.view_orders()

def test_new_order():
    """test new order"""
    order = backend.new_order(1, [51.521251, -0.203586])
    assert isinstance(order.order_id, int)
    with raises(ValueError):
        order.location_words


def test_existing_order():
    """test existing order"""
    order = backend.existing_order(id)
    order.location_co_ords = "1.000013,1.000013"
    assert order.date == date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    order.update_order()
    assert order.customer == "mike"
    assert order.location_words == "dermatologists.discusses.unroll"
    assert order.location_co_ords == "1.000013,1.000013"


# These will all fail if an api key is not set!!!! You were warned in line 16!
def test_add_item():
    """test add item"""
    menu = backend.new_item("test", "1")
    menu.delete_from_db()
    menu.save()
    order = backend.existing_order(id)
    order.add_items("test", "2")
    assert order.view_order_items() == [("test", 2)]


def test_get_total():
    """test get total"""
    order = backend.existing_order(id)
    assert order.get_total() == 2


def test_update_item_quanity():
    """test update item quanity"""
    order = backend.existing_order(id)
    order.add_items("test", 1)
    assert order.view_order_items() == [("test", 3)]


def test_not_implemented_error():
    """test not implemented error"""
    order = backend.existing_order(id)
    with raises(NotImplementedError):
        order.add_items("notintheresurely", 1)


def test_update_item_quanity_to_0():
    """test update item quanity to 0"""
    order = backend.existing_order(id)
    order.add_items("test", 2)
    order.remove_items("test")
    assert order.view_order_items() == []


def test_delete_order():
    """test delete order"""
    order = backend.existing_order(id)
    order.delete()
    assert (
        id,
        "mike",
        "dermatologists.discusses.unroll",
        order.date,
    ) not in backend.view_orders()
    assert order.view_order_items() == []


@patch("backend.order.DBClass.execute_sql")
def test_first_order_id(mock_dbclass: patch):
    """test first order id"""
    mock_dbclass.return_value = []
    order = backend.new_order("mike", [51.521251, -0.203586])
    assert order.order_id == 1
