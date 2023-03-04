"""all interactions with orders"""
from datetime import datetime


class Order:
    def __init__(self, customer_id=None, location=None, order_id=None) -> None:
        self.date = None
        self.customer_id = customer_id
        self.location = location
        if order_id is None:
            self.order_id = self.__get_next_order_id()
        else:
            self.order_id = order_id        

    def __get_next_order_id(self):
        try:
            orders = len(self.view_order_items())
        except TypeError:
            orders = 0
        return orders + 1

    def set_order_date(self):
        self.date = datetime.utcnow() 

    def add_items(self, name, quantity):
        pass

    def remove_items(self):
        pass

    def view_orders(self):
        pass

    def view_order_items(self):
        pass

    def save(self):
        pass

    def delete(self):
        pass

    def get_total(self):
        pass

class orderItems:
    def __init__(self, name=None, quanity=None, order_id=None) -> None:
        self.name = name
        self.quanity = quanity
        self.order_id = order_id

    def view_order_items(self):
        pass

    def save(self):
        pass

    def delete(self):
        pass