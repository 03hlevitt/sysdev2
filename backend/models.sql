PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS customer (
  name VARCHAR(255) PRIMARY KEY NOT NULL
);
CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  location VARCHAR(255) NOT NULL,
  order_date DATETIME NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customer(id)
);
CREATE TABLE IF NOT EXISTS menu_items (
  name VARCHAR(255) NOT NULL PRIMARY KEY,
  price DECIMAL(10, 2) NOT NULL
);
CREATE TABLE IF NOT EXISTS order_items (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  menu_item VARCHAR(255) NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (menu_item) REFERENCES menu_items(name)
);
