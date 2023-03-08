import sqlite3
import requests
import os
import json

def coordinates_to_words(lat, lon):
    key = os.environ.get('THREEWORDS_SUBSCRIPTION_KEY')
    url = 'https://api.what3words.com/v3/convert-to-3wa'
    params = {"coordinates":f"{lat},{lon}","key":key}
    print("***", params)
    r = requests.get(url, params = params)
    r_dict = json.loads(r.text)
    print("***", r_dict)
    return r_dict["words"]

def words_to_coordinates(words):
    key = os.environ.get('THREEWORDS_SUBSCRIPTION_KEY')
    url = 'https://api.what3words.com/v3/convert-to-coordinates'
    params = {"words":words,"key":key}
    r = requests.get(url, params = params)
    r_dict = json.loads(r.text)
    return r_dict["coordinates"]

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
