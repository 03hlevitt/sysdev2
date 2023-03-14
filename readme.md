        +------------+          +---------------+          +---------------+
        |   Order    |          |   MenuItem    |          |   OrderItem   |
        +------------+          +---------------+          +---------------+
        |    id      |          |    name       |          |   order_id    |
        |  customer  |          |    price      |          |   menu_item   |
        |  location  |          +---------------+          |   quantity    |
        |    date    |                                       +---------------+
        +------------+
              ^                    ^                       ^
              |                    |                       |
              |                    |                       |
           order_id           menu_item            order_id, menu_item
              |                    |                       |
              |                    |                       |
              +-----------+--------+-----------------------+
                          |
                          |
                          |
                     +---------+
                     |  Menu   |
                     +---------+
