"""all interactions with orders"""
from datetime import datetime
import sqlite3

from backend.common import DBClass, coordinates_to_words


class Order(DBClass):
    def __init__(self) -> None:
        super().__init__()
        self.date = None # init to None so that it can be set to a datetime object later

    def set_order_date(self):
        self.date = datetime.utcnow()

    @property
    def date_string(self):
        try:
            return self.date.strftime('%Y-%m-%d %H:%M:%S.%f')
        except AttributeError as e:
            print("date not set, set it with set_order_date(), %s", e)
            return "date not set"

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
        self.execute_sql("INSERT INTO orders (id, customer, location, order_date) VALUES ('%s', '%s', '%s', '%s')" % (self.order_id, self.customer, self.location_words, self.date))

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
    

class NewOrder(Order):
    def __init__(self, customer, location_co_ords):
        super().__init__()
        self.customer = customer
        self.location_co_ords = location_co_ords

    @property
    def order_id(self):
        try:
            orders_list = self.view_orders()
            print("current orders in db:, %s", len(orders_list))
            order_id = len(orders_list) + 1
            return order_id
        except TypeError as e:
            print("no orders yet, so setting order id to one, %s", e)
            return 1
        
    @property
    def location_words(self):
        return coordinates_to_words(self.location_co_ords[0], self.location_co_ords[1])

        

class ExistingOrder(Order):
    def __init__(self, order_id):
        super().__init__()
        self.order_id = order_id

    @property
    def customer(self):
        return self.execute_sql("SELECT customer FROM orders WHERE id = '%s'" % self.order_id)[0][0]
    
    @property
    def location_words(self):
        return self.execute_sql("SELECT location FROM orders WHERE id = '%s'" % self.order_id)[0][0]