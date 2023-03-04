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
    menu.save()
    menu.get_menu_item("test")
    assert menu.name == "test"
    assert menu.price == 1

def test_view_menu():
    menu = Menu("test", 1)
    menu.save()
    menu = Menu()
    assert menu.view_menu() == [("test", 1)]

def test_delete_menu():
    menu = Menu("test", 1)
    menu.save()
    menu.delete()
    assert menu.view_menu() == []