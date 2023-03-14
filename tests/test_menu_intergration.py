"""test the menu class"""
from backend.main import Backend

backend = Backend()

def test_menu_with_args():
    menu = backend.new_item("test", "1") # string number as inserted directly from text box
    assert menu.name == "test"
    assert menu.price == "1"

def test_save_menu():
    new_item = backend.new_item("test", "1")
    new_item.delete_from_db()
    new_item.save()
    existing_item = backend.existing_item("test")
    assert existing_item.name == "test"
    assert existing_item.price == 1

def test_view_menu():
    assert ("test", 1) in backend.view_menu()

def test_delete_from_db_menu():
    existing_item = backend.existing_item("test")
    existing_item.delete_from_db()
    assert ("test", 1) not in backend.view_menu()