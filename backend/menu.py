"""all interactions with the menu"""
import sqlite3

class Menu:
    def __init__(self, name=None, price=None):
        self.name = name
        self.price = price

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

    def view_menu(self):
        """view the menu"""
        return self.__execute_sql("SELECT * FROM menu_items")

    def get_menu_item(self, kwargs):
        """get a menu item from the db and stoer it in the object"""
        data = self.__execute_sql("SELECT * FROM menu_items WHERE name = '%s'" % kwargs)
        self.name = data[0][0]
        self.price = data[0][1]

    def save(self):
        """save the menu item stored in the object"""
        self.__execute_sql("INSERT INTO menu_items (name, price) VALUES ('%s', '%s')" % (self.name, self.price))

    def delete_from_db(self):
        """delete the menu item stored in the object"""
        self.__execute_sql("DELETE FROM menu_items WHERE name = '%s'" % self.name)
    