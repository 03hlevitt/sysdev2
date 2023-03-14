from unittest.mock import patch, MagicMock
from pytest import raises
from backend.main import Backend
from custom.exceptions import NoKeyError, WhatThreeWordsError
import os

# TODO: setup and teardown
# TODO: more exceptions!
# TODO: better logging of the whole thing

backend = Backend()

@patch('backend.order.datetime')
def test_order_with_args(mock_time):
    if os.getenv("THREEWORDS_SUBSCRIPTION_KEY") is None:
        print("please input api key!!!")
        with raises(NoKeyError):
            order = backend.new_order("mike", "51.521251,-0.203586")
            order.location_words
    else:
        mock_time.utcnow.return_value = "test"
        order = backend.new_order("mike", "51.521251,-0.203586")
        order.set_order_date()
        assert type(order.order_id) == type(6) # since order id increases each order 
        assert order.customer == "mike"        # can only assert type
        assert order.location_words == "index.home.raft"
        assert order.date == "test"

def test_save():
    if os.getenv("THREEWORDS_SUBSCRIPTION_KEY") is None:
        print("please input api key!!!")
        with raises(NoKeyError):
            order = backend.new_order("mike", "51.521251,-0.203586")
            order.set_order_date()
            order.save()
    else:
        order = backend.new_order("mike", "51.521251,-0.203586")
        order.set_order_date()
        global id # for later assertions
        id = order.order_id
        order.save()
        assert (id, "mike", "index.home.raft", order.date_string) in order.view_orders()

def test_date_not_set():
    order = backend.new_order("mike", [51.521251, -0.203586])
    assert order.date_string == "date not set"

def test_new_order():
    order = backend.new_order(1, [51.521251, -0.203586])
    assert type(order.order_id) == type(6) 

# These will all fail if an api key is not set!!!! You were warned in line 16!
def test_add_item():
    menu = backend.new_item("test", "1")
    menu.delete_from_db()
    menu.save()
    order = backend.existing_order(id)
    order.add_items("test", "2")
    assert order.view_order_items() == [("test", 2)]

def test_get_total():
    order = backend.existing_order(id)
    assert order.get_total() == 2

def test_update_item_quanity():
    order = backend.existing_order(id)
    order.add_items("test", 1)
    assert order.view_order_items() == [("test", 3)]

def test_not_implemented_error():
    order = backend.existing_order(id)
    with raises(NotImplementedError):
        order.add_items("notintheresurely", 1)

def test_update_item_quanity_to_0():
    order = backend.existing_order(id)
    order.add_items("test", 2)
    order.remove_items("test")
    assert order.view_order_items() == []
    

def test_delete_order():
    order = backend.existing_order(id)
    order.delete()
    assert (id, "mike", "index.home.raft", order.date_string) not in order.view_orders()
    assert order.view_order_items() == []

@patch('backend.order.DBClass.execute_sql')
def test_first_order_id(mock_dbclass):
    mock_dbclass.return_value = []
    order = backend.new_order("mike", [51.521251, -0.203586])
    assert order.order_id == 1
