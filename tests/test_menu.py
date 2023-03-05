"""test the menu class"""
import pytest
from backend.menu import newMenuItem, existingMenuItem, Menu


def test_menu_with_args():
    menu = newMenuItem("test", 1)
    assert menu.name == "test"
    assert menu.price == 1

def test_save_menu():
    new_item = newMenuItem("test", 1)
    new_item.delete_from_db()
    new_item.save()
    existing_item = existingMenuItem("test")
    assert existing_item.name == "test"
    assert existing_item.price == 1

def test_view_menu():
    menu = Menu()
    assert menu.view_menu() == [("test", 1)]

def test_delete_from_db_menu():
    existing_item = existingMenuItem("test")
    existing_item.delete_from_db()
    assert existing_item.view_menu() == []