"""handler class for returning objects for interacting with the db
 or select all type functions"""
from backend.menu import NewMenuItem, ExistingMenuItem, Menu
from backend.order import Order, NewOrder, ExistingOrder


class Backend:
    """handle returning of objects for interacting with the database"""

    def new_item(self, name: str, price: str) -> NewMenuItem:
        """instantiates a new item object

        Args:
            name (str): Name of new menu item
            price (int): Price

        Returns:
            NewMenuItem: instanciated object
        """
        return NewMenuItem(name, price)

    def existing_item(self, name: str) -> ExistingMenuItem:
        """instantiates an existing item object

        Args:
            name (str): of existing menu item

        Returns:
            ExistingMenuItem: instantiates object
        """
        return ExistingMenuItem(name)

    @classmethod
    def view_menu(cls) -> list:
        """shows alll menu items and their prices

        Returns:
            list: list returned by db of all menu items i.e. [("hotdog", 1)]
        """
        menu = Menu()
        return menu.view_menu()

    def new_order(self, customer: str, location_co_ords: str) -> NewOrder:
        """instantiates a new order object

        Args:
            customer (str): customer username
            location_co_ords (str): latitude and longitude separated by a comma

        Returns:
            NewOrder: instantiated new order object
        """
        return NewOrder(customer, location_co_ords)

    def existing_order(self, order_id: str) -> ExistingOrder:
        """instantiates na existing order object

        Args:
            order_id (int): order id of exisitng order

        Returns:
            ExistingOrder: instantiated order object
        """
        return ExistingOrder(order_id)

    @classmethod
    def view_orders(cls) -> list:
        """show all orders from the db (no items attatched)

        Returns:
            list: list returned by db of all orders
        """
        order = Order()
        return order.view_orders()
    