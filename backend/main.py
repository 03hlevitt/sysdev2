import sqlite3


def view_orders(customer_id):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE customer_id = '%s'", customer_id)
    rows = c.fetchall()
    conn.close()
    return rows


if __name__ == '__main__':
    print(view_orders(1))