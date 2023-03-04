"""all interactions with the menu"""
import sqlite3
from backend.common import DBClass
# if price is noe then get db
# TODO: newItem and updateItem Classes, with show all as a class method

class Menu(DBClass):
    def __init__(self, name=None, price=None):
        super().__init__()
        self.name = name
        self.price = price

    def view_menu(self):
        """view the menu"""
        return self.execute_sql("SELECT * FROM menu_items")

    def get_menu_item(self, kwargs):
        """get a menu item from the db and stoer it in the object"""
        data = self.execute_sql("SELECT * FROM menu_items WHERE name = '%s'" % kwargs)
        self.name = data[0][0]
        self.price = data[0][1]

    def save(self):
        """save the menu item stored in the object"""
        self.execute_sql("INSERT INTO menu_items (name, price) VALUES ('%s', '%s')" % (self.name, self.price))

    def delete_from_db(self):
        """delete the menu item stored in the object"""
        self.execute_sql("DELETE FROM menu_items WHERE name = '%s'" % self.name)
    