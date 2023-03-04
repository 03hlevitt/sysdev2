"""all interactions with orders"""
from datetime import datetime
import sqlite3

from backend.common import DBClass

# TODO: Location
# TODO: base class
# TODO: if customer_id and location are None, then get order from db
# TODO: NewOrder and Existing order classes with show all as a class method

class Order(DBClass):
    def __init__(self, customer_id=None, location=None, order_id=None) -> None:
        super().__init__()
        self.date = None
        self.customer_id = customer_id
        self.location = location
        self.order_id_param = order_id

    @property
    def order_id(self):
        if self.order_id_param is None:
            print("getting next order id as no order id in params")
            return self.__get_next_order_id()
        else:
            return self.order_id_param
        
    def __get_next_order_id(self):
        try:
            orders_list = self.view_orders()
            print("current orders in db:, %s", len(orders_list))
            order_id = len(orders_list) + 1
            return order_id
        except TypeError as e:
            print("no orders yet, so setting order id to one, %s", e)
            return 1

    def set_order_date(self):
        self.date = datetime.utcnow() 

    def add_items(self, name, quantity):
        #  TODO: make composit key so cant add multiple of same item
        self.execute_sql("INSERT INTO order_items (menu_item, quantity, order_id) VALUES ('%s', '%s', '%s')" % (name, quantity, self.order_id))

    def update_items(self, menu_item, quantity):
        if quantity == 0:
            self.execute_sql("DELETE FROM order_items WHERE order_id = '%s' AND menu_item = '%s'" % (self.order_id, menu_item))
        else:
            self.execute_sql("UPDATE order_items SET quantity = '%s' WHERE order_id = '%s' AND menu_item = '%s'" % (quantity, self.order_id, menu_item))


    def view_orders(self):
        return self.execute_sql("SELECT * FROM orders")

    def view_order_items(self):
        return self.execute_sql("SELECT menu_item, quantity FROM order_items WHERE order_id = '%s'" % self.order_id)


    def save(self):
        self.execute_sql("INSERT INTO orders (id, customer_id, location, order_date) VALUES ('%s', '%s', '%s', '%s')" % (self.order_id, self.customer_id, self.location, self.date))

    def delete(self):
        self.execute_sql("DELETE FROM orders WHERE id = '%s'" % self.order_id)
        self.execute_sql("DELETE FROM order_items WHERE order_id = '%s'" % self.order_id)

    def get_total(self):
        order_items = self.view_order_items()
        total = 0
        for item in order_items:
            quantity = item[1]
            price = self.execute_sql("SELECT price FROM menu_items WHERE name = '%s'" % item[0])[0][0]
            total += price * quantity
        return total