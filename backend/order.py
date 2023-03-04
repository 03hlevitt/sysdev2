"""all interactions with orders"""
from datetime import datetime
import sqlite3

# TODO: Location

class Order:
    def __init__(self, customer_id=None, location=None, order_id=None) -> None:
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

    def __init_tables(self):
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        with open("./backend/models.sql", "r") as f:
            sql = str(f.read())
            print(sql)
            try:
                c.executescript(sql)
                c.close()
                conn.close()
            except Exception as e:
                print(e)

    def __sql_attempt(self, sql):
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        conn.commit()
        conn.close()
        return rows

    def __execute_sql(self, sql):
        try:
            return self.__sql_attempt(sql)
        except sqlite3.OperationalError as e:
            print(e)
            self.__init_tables()
            return self.__sql_attempt(sql)        

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
        self.__execute_sql("INSERT INTO order_items (menu_item, quantity, order_id) VALUES ('%s', '%s', '%s')" % (name, quantity, self.order_id))

    def update_items(self, menu_item, quantity):
        db_quantity = self.__execute_sql("SELECT quantity FROM order_items WHERE order_id = '%s' AND menu_item = '%s'" % (self.order_id, menu_item))
        if quantity == 0:
            self.__execute_sql("DELETE FROM order_items WHERE order_id = '%s' AND menu_item = '%s'" % (self.order_id, menu_item))
        else:
            self.__execute_sql("UPDATE order_items SET quantity = '%s' WHERE order_id = '%s' AND menu_item = '%s'" % (quantity, self.order_id, menu_item))


    def view_orders(self):
        return self.__execute_sql("SELECT * FROM orders")

    def view_order_items(self):
        return self.__execute_sql("SELECT menu_item, quantity FROM order_items WHERE order_id = '%s'" % self.order_id)


    def save(self):
        self.__execute_sql("INSERT INTO orders (id, customer_id, location, order_date) VALUES ('%s', '%s', '%s', '%s')" % (self.order_id, self.customer_id, self.location, self.date))

    def delete(self):
        self.__execute_sql("DELETE FROM orders WHERE id = '%s'" % self.order_id)

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