import pytest
from backend import main

def test_execute_sql():
    assert main.execute_sql("test") == "test"

def test_create_menu_item():
    main.create_menu_item("test", 1)
    assert "test" in main.view_menu_items()

def test_view_menu_items():
    assert main.view_menu_items() == "test"

def test_update_menu_item():
    main.update_menu_item("test", price=2)
    main.update_menu_item("test", name="test2")
    assert ("test2", 2) in main.view_menu_items()

def test_delete_menu_item():
    main.delete_menu_item("test2")
    assert "test2" not in main.view_menu_items()

# def test_view_orders_by_customer_id():
#     assert main.view_orders_by_customer_id(1) == "test"