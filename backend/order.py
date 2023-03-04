"""all interactions with orders"""
import datetime


class Order:
    def __init__(self, customer_id=None, location=None, order_id=None) -> None:
        self.date = None
        pass
    
    @property
    def order_id(self):
        return self.order_id

    def set_order_date(self):
        self.date = datetime.datetime.utcnow() 

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