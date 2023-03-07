"""all interactions with the menu"""
import sqlite3
from backend.common import DBClass

class Menu(DBClass):
    def __init__(self, name=None, price=None):
        super().__init__()
    
    def view_menu(self):
        """view the menu"""
        return self.execute_sql("SELECT * FROM menu_items")

    def delete_from_db(self):
        """delete the menu item stored in the object"""
        self.execute_sql("DELETE FROM menu_items WHERE name = '%s'" % self.name)

class newMenuItem(Menu):
    def __init__(self, name, price):
        super().__init__(name, price)
        self.name = name
        self.price = price

    def save(self):
        """save the menu item stored in the object"""
        self.execute_sql("INSERT INTO menu_items (name, price) VALUES ('%s', '%s')" % (self.name, self.price))

class existingMenuItem(Menu):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.price = self._get_price()
    
    def _get_price(self):
        """get a menu item from the db and store it in the object"""
        data = self.execute_sql("SELECT price FROM menu_items WHERE name = '%s'" % self.name)
        print(data)
        return data[0][0]
    
    # setter for price
    def update_price(self, price):
        self.price = price

    def save(self):
        """save the menu item stored in the object"""
        self.execute_sql("UPDATE menu_items SET price = '%s' WHERE name = '%s'" % (self.price, self.name))