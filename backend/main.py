from backend.menu import newMenuItem, existingMenuItem, Menu
from backend.order import Order, NewOrder, ExistingOrder

class Backend:
    """handle returning of objects for interacting with the database"""
    def new_item(self, name, price):
        return newMenuItem(name, price)
    
    def existing_item(self, name):
        return existingMenuItem(name)
    
    @classmethod
    def view_menu(self):
        menu = Menu()
        return menu.view_menu()
    
    def new_order(self, customer, location_co_ords):
        return NewOrder(customer, location_co_ords)
    
    def existing_order(self, order_id):
        return ExistingOrder(order_id)
    
    @classmethod
    def view_orders(self):
        order = Order()
        return order.view_orders()