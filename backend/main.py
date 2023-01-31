import sqlite3


def view_orders_by_customer_id(customer_id):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE customer_id = '%s'", customer_id)
    rows = c.fetchall()
    conn.close()
    return rows


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