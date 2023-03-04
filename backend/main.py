import sqlite3



def view_orders_by_customer_id(customer_id):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
    rows = c.fetchall()
    conn.close()
    return rows

class Menu:
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
            init_tables()
            return self.__sql_attempt(sql)

    def create_menu_item(self, name, price):
        sql = "INSERT INTO menu_items (name, price) VALUES ('%s', '%s')" % (name, price)
        print("insert sql: ", sql)
        return self.__execute_sql(sql)


    def view_menu_items(self, **kwargs):
        sql = "SELECT * FROM menu_items"
        if kwargs:
            sql += " WHERE "
            for key, value in kwargs.items():
                sql += "%s = '%s' AND " % (key, value)
            sql = sql[:-5]
        print(sql)
        return self.__execute_sql(sql)

    def update_menu_item(self, item_name, **kwargs):
        sql = "UPDATE menu_items SET "
        for key, value in kwargs.items():
            sql += "%s = '%s', " % (key, value)
        sql = sql[:-2] + " WHERE name = '%s'" % item_name
        return self.__execute_sql(sql)

    def delete_menu_item(self, name):
        sql = """UPDATE menu_items SET active = 0 
        WHERE menu_items.name = '%s'""" % name
        return self.__execute_sql(sql)

def init_tables():
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


if __name__ == '__main__':
    menu = Menu()
    try:
        print(view_orders_by_customer_id("1"))
    except sqlite3.OperationalError as e:
        print(e)
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
        print(view_orders_by_customer_id("1"))