CREATE TABLE customer (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
);

CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  FOREIGN KEY (customer_id) REFERENCES customer(id),
  location VARCHAR(255) NOT NULL,
  order_date DATETIME NOT NULL
);

CREATE TABLE menu_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  menu_item_id INT NOT NULL,
  quantity INT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);

insert into customer (name) values ('John Doe', 'Jane Doe', 'Joe Bloggs', 'James Penman');