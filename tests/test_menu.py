"""test the menu class"""
import pytest
from backend.menu import Menu

def test_menu():
    menu = Menu()
    assert menu.name == None
    assert menu.price == None

def test_menu_with_args():
    menu = Menu("test", 1)
    assert menu.name == "test"
    assert menu.price == 1

def test_save_menu():
    menu = Menu("test", 1)
    menu.delete_from_db()
    menu.save()
    menu.get_menu_item("test")
    assert menu.name == "test"
    assert menu.price == 1

def test_view_menu():
    menu = Menu("test", 1)
    menu.delete_from_db()
    menu.save()
    assert menu.view_menu() == [("test", 1)]

def test_delete_from_db_menu():
    menu = Menu("test", 1)
    menu.delete_from_db()
    assert menu.view_menu() == []