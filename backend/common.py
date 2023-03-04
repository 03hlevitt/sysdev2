import sqlite3

class DBClass:
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

    def execute_sql(self, sql):
        try:
            return self.__sql_attempt(sql)
        except sqlite3.OperationalError as e:
            print(e)
            self.__init_tables()
            return self.__sql_attempt(sql)