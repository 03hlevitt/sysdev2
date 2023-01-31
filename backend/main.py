import sqlite3


def execute_sql(sql):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()
    conn.close()
    return rows

def view_orders_by_customer_id(customer_id):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE customer_id = '%s'", customer_id)
    rows = c.fetchall()
    conn.close()
    return rows


def create_menu_item(name, price):
    sql = "INSERT INTO menu_items (name, price) VALUES ('%s', '%s')" % (name, price)
    return execute_sql(sql)


def view_menu_items(**kwargs):
    sql = "SELECT * FROM menu_items"
    if kwargs:
        sql += " WHERE "
        for key, value in kwargs.items():
            sql += "%s = '%s' AND " % (key, value)
        sql = sql[:-5]
    return execute_sql(sql)

def update_menu_item(name, **kwargs):
    sql = "UPDATE menu_items SET "
    for key, value in kwargs.items():
        sql += "%s = '%s', " % (key, value)
    sql = sql[:-2] + " WHERE name = '%s'" % name
    return execute_sql(sql)

def delete_menu_item(name):
    sql = "DELETE FROM menu_items WHERE name = '%s'" % name
    return execute_sql(sql)


if __name__ == '__main__':
    try:
        print(view_orders(1))
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
        print(view_orders(1))