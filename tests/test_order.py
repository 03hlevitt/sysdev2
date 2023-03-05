from unittest.mock import patch
import pytest
from backend.menu import Menu

from backend.order import Order, NewOrder, ExistingOrder


# TODO: TEST DATES
# TODO: TEST LOCATION
# TODO: setup and teardown
# TODO: more exceptions!
# TODO: better logging of the whole thing

def test_order():
    order = Order()
    assert order.date == None


@patch('backend.order.datetime')
def test_order_with_args(mock_time):
    mock_time.utcnow.return_value = "test"
    order = NewOrder(1, 1)
    order.set_order_date()
    assert order.order_id == 1
    assert order.customer_id == 1
    assert order.location == 1
    assert order.date == "test"

def test_save():
    order = NewOrder(1, 1)
    order.save()
    assert order.view_orders() == [(1, 1, '1', 'None')]

def test_new_order():
    order = NewOrder(1, 1)
    assert order.order_id == 2

# TODO: change this so that it checks the number adds to quantity
def test_add_item():
    menu = Menu("test", 1)
    menu.delete_from_db()
    menu.save()
    order = Order(1, 1, 1)
    order.add_items("test", 2)
    assert order.view_order_items() == [("test", 2)]

def test_get_total():
    order = Order(1, 1, 1)
    assert order.get_total() == 2

def test_update_item_quanity():
    order = Order(1, 1, 1)
    order.update_items("test", 1)
    assert order.view_order_items() == [("test", 1)]

def test_update_item_quanity_to_0():
    order = Order(1, 1, 1)
    order.add_items("foobar", 2)
    order.update_items("foobar", 0)
    assert order.view_order_items() == [("test", 1)]
    

def test_delete_order():
    order = Order(1, 1, 1)
    order.delete()
    assert order.view_orders() == []
    assert order.view_order_items() == []