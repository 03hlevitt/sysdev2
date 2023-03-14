"""all interactions with orders"""
from datetime import datetime

from backend.common import DBClass, coordinates_to_words, words_to_coordinates


class Order(DBClass):
    """super class for all order interactions"""

    def __init__(self) -> None:
        """constructor for superclass"""
        super().__init__()
        self.date = (
            None  # init to None so that it can be set to a datetime later
        )

    def set_order_date(self) -> None:
        """set the date of the order to now"""
        self.date = datetime.utcnow()

    @property
    def date_string(self) -> str:
        """return stringified date

        Returns:
            str: datetime in the form year-month-day hour:minute:seconds.miliseconds
        """
        try:
            return self.date.strftime("%Y-%m-%d %H:%M:%S.%f")
        except AttributeError as error:
            print("date not set, set it with set_order_date(), %s", error)
            return "date not set"

    def view_orders(self) -> list:
        """view all orders in teh db without their items

        Returns:
            list: db return i.e. [(x,y,z),(a,b,c)]
        """
        return self.execute_sql("SELECT * FROM orders")

    def view_order_items(self) -> list:
        """view items and their quantities in a specific order

        Returns:
            list: return from db; [(x,y),(a,b)]
        """
        return self.execute_sql(
            """SELECT menu_item, quantity FROM order_items
              WHERE order_id = '%s'"""
            % self.order_id
        )

    def delete(self) -> None:
        """delete the order stored in the object from the db"""
        self.execute_sql("DELETE FROM orders WHERE id = '%s'" % self.order_id)
        self.execute_sql(
            "DELETE FROM order_items WHERE order_id = '%s'" % self.order_id
        )

    def get_total(self) -> int:
        """return total cost of items in an order

        Returns:
            int: total cost of items in an order
        """
        order_items = self.view_order_items()
        total = 0
        for item in order_items:
            quantity = item[1]
            price = self.execute_sql(
                "SELECT price FROM menu_items WHERE name = '%s'" % item[0]
            )[0][0]
            total += price * quantity
        return total


class NewOrder(Order):
    """new order object which can later be added to db"""
    def __init__(self, customer: str, location_co_ords:str) -> None:
        """constructor for a new order

        Args:
            customer (str): custoemr name (must be unique)
            location_co_ords (str): lat and long in a string e.g. "1,1"
        """
        super().__init__()
        self.customer = customer
        self.location_co_ords = location_co_ords

    @property
    def order_id(self) -> int:
        """find next available order id for order to take

        Returns:
            int: id of the orders
        """
        try:
            last_order_id = self.execute_sql("SELECT id FROM orders ORDER BY id DESC LIMIT 1")[0][0]
            order_id = last_order_id + 1
            return order_id
        except (TypeError, IndexError) as error:
            print("no orders yet, so setting order id to one, %s", error)
            return 1

    @property
    def location_words(self) -> str:
        """converts co ords to what three words

        Returns:
            str: what threee words str separated by . e.g. "hello.my.name"
        """
        try:
            co_ords = self.location_co_ords.split(",")
            return coordinates_to_words(co_ords[0], co_ords[1])
        except (IndexError, AttributeError) as error:
            print("location co ords not set, %s", error)
            raise ValueError("location co ords not set, %s", error)

    def save(self) -> None:
        """save teh order stored in the object to the database"""
        self.execute_sql(
            """INSERT INTO orders (id, customer, location, date)
              VALUES ('%s', '%s', '%s', '%s')"""
            % (self.order_id, self.customer, self.location_words, self.date)
        )


class ExistingOrder(Order):
    """class for all interactions with existing orders"""

    def __init__(self, order_id: str) -> None:
        """constructor for existing order, found by id"""
        super().__init__()
        self.order_id = order_id
        self.customer = self.execute_sql(
            "SELECT customer FROM orders WHERE id = '%s'" % self.order_id
        )[0][0]
        self.location_words = self.execute_sql(
            "SELECT location FROM orders WHERE id = '%s'" % self.order_id
        )[0][0]
        self.date = self.__set_date()
    
    def __set_date(self) -> datetime:
        """get the date of the order from the db and
          overwrite the date in the super class,
        if not found set to none, added to super class
        both classes needed set order

        Returns:
            datetime: date of the order
        """
        try:
            return self.execute_sql("SELECT date FROM orders WHERE id = '%s'" % self.order_id)[0][0]
        except IndexError as error:
            print("order not found in db, setting to none as init %s", error)
            return None

    @property
    def location_co_ords(self):
        """converts what three words to co ords

        Returns:
            str: lat and long in a string e.g. "1,1"
        """
        return words_to_coordinates(self.location_words)

    @location_co_ords.setter
    def location_co_ords(self, value: str):
        """converts what co ords to what three words

        Args:
            value (str): lat and long in a string e.g. "1,1"
        """
        co_ords = value.split(",")
        self.location_words = coordinates_to_words(co_ords[0], co_ords[1])
        

    def update_order(self) -> None:
        """updates order in db with new values stored in object"""
        self.set_order_date()
        self.execute_sql(
            "UPDATE orders SET (customer, location, date) = ('%s', '%s', '%s') WHERE id = '%s'"
            % (self.customer, self.location_words, self.date, self.order_id)
        )

    def add_items(self, name: str, quantity: int) -> None:
        """add a given quantity of an item to the db

        Args:
            name (str): name of menu item (must be unique!)
            quantity (int): amount of the item to add the db
        """
        if not self.execute_sql("SELECT price FROM menu_items WHERE name = '%s'" % name):
            print("item not in menu")
            raise NotImplementedError("item not in menu")
        else:
            item = self.execute_sql(
                """select * from order_items
                where order_id = '%s' and menu_item = '%s'"""
                % (self.order_id, name)
            )
            if item:
                current_quantity = item[0][2]
                name = item[0][1]
                quantity = int(quantity) + int(current_quantity) # value errors are caught
                self.execute_sql(
                    """UPDATE order_items SET quantity = '%s'
                    WHERE order_id = '%s' AND menu_item = '%s'"""
                    % (quantity, self.order_id, name)
                )
            else:
                string = """INSERT INTO order_items (order_id, menu_item, quantity)
                    VALUES ('%s', '%s', '%s')""" % (
                    self.order_id,
                    name,
                    quantity,
                )
                print(string)
                self.execute_sql(string)

    def remove_items(self, name: str) -> None:
        """remove an item and all of its quantities from the db

        Args:
            name (str): name of menu item (must be unique!)
        """
        string = """DELETE FROM order_items
              WHERE order_id = '%s' AND menu_item = '%s'""" % (
            self.order_id,
            name,
        )
        print(string)
        self.execute_sql(string)
