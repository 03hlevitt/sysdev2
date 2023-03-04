from unittest.mock import patch
import pytest

from backend.order import Order

def test_order():
    order = Order()
    assert order.order_id == None
    assert order.customer_id == None
    assert order.location == None
    assert order.date == None


@patch('backend.order.datetime.datetime.utcnow')
def test_order_with_args(mock_time):
    mock_time.return_value = "test"
    order = Order(1, 1, 1)
    order.set_order_date()
    assert order.order_id == 1
    assert order.customer_id == 1
    assert order.location == 1
    assert order.date == "test"

def test_new_order():
    order = Order(1, 1, 1)
    order.save()
    order = Order(1, 1)
    order.order_id = 2
    order.save()
    assert order.view_orders() == [(1, 1, 1, []), (2, 1, 1, [])]

def test_add_item():
    order = Order(1, 1, 1)
    order.save()
    order.add_item("test", 1)
    assert order.view_order_items == [("test", 1)]

def test_get_total():
    order = Order(1, 1, 1)
    order.save()
    order.add_item("test", 1)
    assert order.get_total() == 2

def test_remove_item():
    order = Order(1, 1, 1)
    order.save()
    order.remove_item("test", 1)
    assert order.view_order_items == []

def test_view_orders():
    order = Order()
    assert order.view_orders() == [(1, 1, 1, [])]

def test_delete_order():
    order = Order(1, 1, 1)
    order.delete()
    assert order.view_orders() == [(2, 1, 1, [])]