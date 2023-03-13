PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY,
  customer VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  date DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS menu_items (
  name VARCHAR(255) NOT NULL PRIMARY KEY,
  price DECIMAL(10, 2) NOT NULL
);
CREATE TABLE IF NOT EXISTS order_items (
  order_id INTEGER NOT NULL,
  menu_item VARCHAR(255) NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (menu_item) REFERENCES menu_items(name)
);
