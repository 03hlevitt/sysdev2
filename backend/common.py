"""utils code for the backend"""
import os
import json
import sqlite3
import requests


def coordinates_to_words(lat: str, lon: str) -> dict:
    """convert to co ords to words using the what three words api

    Args:
        lat (str): latitude
        lon (str): longitude

    Returns:
        dict: threewords location string
    """
    key = os.environ.get("THREEWORDS_SUBSCRIPTION_KEY")
    url = "https://api.what3words.com/v3/convert-to-3wa"
    params = {"coordinates": f"{lat},{lon}", "key": key}
    print("***", params)
    response = requests.get(url, params=params, timeout=30)
    response_dict = json.loads(response.text)
    print("***", response_dict)
    return response_dict["words"]


def words_to_coordinates(words: str) -> str:
    """turn what three words location into latitude and location

    Args:
        words (str): what three words as a string
          with each word separated with a .

    Returns:
        str: co ords location in a string e.e. (1.1,1.1)
    """
    key = os.environ.get("THREEWORDS_SUBSCRIPTION_KEY")
    url = "https://api.what3words.com/v3/convert-to-coordinates"
    params = {"words": words, "key": key}
    response = requests.get(url, params=params, timeout=30)
    response_dict = json.loads(response.text)
    co_ords = response_dict["coordinates"]
    co_ords_string = f"{co_ords['lat']},{co_ords['lng']}"
    return co_ords_string


class DBClass:
    """class used by all backend classes for interacting with sqllite"""

    def init_tables(self):
        """creates tables if hasnt already been created"""
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()
        with open("./backend/models.sql", mode="r", encoding="utf-8") as file:
            sql = str(file.read())
            print(sql)
            try:
                cursor.executescript(sql)
                cursor.close()
                conn.close()
            except sqlite3.Error as error:
                print(error)

    def __sql_attempt(self, sql: str) -> list:
        """wrapper for a sql attempt to connect/commit to db (private)

        Args:
            sql (str): sql query in a string

        Returns:
            list: return from db
        """
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows

    def execute_sql(self, sql: str) -> list:
        """wrapper for a sql attempt with try/ except

        Args:
            sql (str): sql in string

        Returns:
            list: return from db
        """
        try:
            return self.__sql_attempt(sql)
        except sqlite3.OperationalError as error:
            print(error)
            self.init_tables()
            return self.__sql_attempt(sql)
