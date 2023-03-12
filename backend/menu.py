"""all interactions with the menu"""
from backend.common import DBClass


#todo exception if not unique!

class Menu(DBClass):
    """SUperclass with basic methods for interacting with the menu"""
    def __init__(self, name):
        self.name = name

    def view_menu(self)->list:
        """view the menu as it currently is in the db

        Returns:
            list: e.g. [("name1", price)]
        """
        return self.execute_sql("SELECT * FROM menu_items")

    def delete_from_db(self):
        """Delete teh menu item (stored in the object) from the db
        """
        self.execute_sql(
            "DELETE FROM menu_items WHERE name = '%s'" % self.name)


class NewMenuItem(Menu):
    """instantiates a new menu item object"""
    def __init__(self, name: str, price: int):
        """constructor for a new menu item

        Args:
            name (str): name of menu item (must be unique!)
            price (int): price fo menu item
        """
        super().__init__(name)
        self.price = price

    def save(self):
        """save the menu item stored in the object"""
        self.execute_sql(
            "INSERT INTO menu_items (name, price) VALUES ('%s', '%s')"
            % (self.name, self.price)
        )


class ExistingMenuItem(Menu):
    """instantiates a new menu item object"""
    def __init__(self, name: str):
        """init method for a new menu item

        Args:
            name (str): unqiue name for menu item already in db
        """
        super().__init__(name)
        self.price = self._get_price()

    def _get_price(self) -> int:
        """fetches price of a menu item from the db

        Returns:
            int: price of menu item
        """
        data = self.execute_sql(
            "SELECT price FROM menu_items WHERE name = '%s'" % self.name
        )
        print(data)
        return data[0][0]

    def save(self):
        """save the menu item stored in the object to the db"""
        self.execute_sql(
            "UPDATE menu_items SET price = '%s' WHERE name = '%s'"
            % (self.price, self.name)
        )
