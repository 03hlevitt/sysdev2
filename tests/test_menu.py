"""test the menu class"""
from backend.main import Backend
from pytest import raises

backend = Backend()

def test_menu_with_args():
    menu = backend.new_item("test", "1") # string number as inserted directly from text box
    assert menu.name == "test"
    assert menu.price == "1"

def test_save_menu_updates(): # aslo tests view menu
    new_item = backend.new_item("test", "1")
    new_item.delete_from_db()
    new_item.save()
    existing_item = backend.existing_item("test")
    assert existing_item.name == "test"
    assert existing_item.price == 1
    existing_item.price = "2"
    existing_item.save()
    assert existing_item.price == "2"
    assert ("test",2) in backend.view_menu()
    with raises(ValueError):
        existing_item.price = "a"

def test_delete_from_db_menu():
    existing_item = backend.existing_item("test")
    existing_item.delete_from_db()
    assert ("test", 1) not in backend.view_menu()

def test_non_digit_price_new():
    with raises(ValueError):
        new_item = backend.new_item("test", "a")
        new_item.price
