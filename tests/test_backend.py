import pytest
from backend import main

def test_execute_sql():
    assert type(main.execute_sql("select * from menu_items")) == list

def test_create_menu_item():
    main.create_menu_item("test", 1)
    print(main.view_menu_items())
    assert "test" in main.view_menu_items()[0]

def test_update_menu_item():
    main.update_menu_item("test", price=2)
    main.update_menu_item("test", name="test2")
    assert ("test2", 2, 1) == main.view_menu_items()[0]

def test_delete_menu_item():
    main.delete_menu_item("test2")
    assert main.view_menu_items()[0] == ("test2", 2, 0)

# def test_view_orders_by_customer_id():
#     assert main.view_orders_by_customer_id(1) == "test"