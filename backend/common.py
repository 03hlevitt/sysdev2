"""utils code for the backend"""
import os
import json
import sqlite3
import requests
from custom.exceptions import NoKeyError, WhatThreeWordsError


def coordinates_to_words(lat: str, lon: str) -> dict:
    """convert to co ords to words using the what three words api

    Args:
        lat (str): latitude
        lon (str): longitude

    Returns:
        dict: threewords location string
    """
    try:
        key = os.environ.get("THREEWORDS_SUBSCRIPTION_KEY")
        url = "https://api.what3words.com/v3/convert-to-3wa"
        params = {"coordinates": f"{lat},{lon}", "key": key}
        print("sending to what3words:", params)
        response = requests.get(url, params=params, timeout=30)
        response_dict = json.loads(response.text)
        print("response from what3 words", response_dict)
        return response_dict["words"]
    except KeyError as error:
        if response_dict["error"]["code"] == "BadCoordinates":
            print(error)
            raise ValueError("Bad co ords")
        elif (
            response_dict["error"]["code"] == "InvalidKey"
            or response_dict["error"]["code"] == "MissingKey"
        ):
            print(error)
            raise NoKeyError("No key found")
        else:
            print(error)
            raise WhatThreeWordsError("Unknown error")


def words_to_coordinates(words: str) -> str:
    """turn what three words location into latitude and location

    Args:
        words (str): what three words as a string
          with each word separated with a .

    Returns:
        str: co ords location in a string e.e. (1.1,1.1)
    """
    try:
        key = os.environ.get("THREEWORDS_SUBSCRIPTION_KEY")
        url = "https://api.what3words.com/v3/convert-to-coordinates"
        params = {"words": words, "key": key}
        print("sending to what3words:", params)
        response = requests.get(url, params=params, timeout=30)
        response_dict = json.loads(response.text)
        print("response from what3 words", response_dict)
        co_ords = response_dict["coordinates"]
        co_ords_string = f"{co_ords['lat']},{co_ords['lng']}"
        return co_ords_string
    except KeyError as error:
        if (
            response_dict["error"]["code"] == "InvalidKey"
            or response_dict["error"]["code"] == "MissingKey"
        ):
            print(error)
            raise NoKeyError("No key found")
        else:
            print(error)
            raise WhatThreeWordsError("Unknown error")


class DBClass:
    """class used by all backend classes for interacting with sqllite"""

    def init_tables(self):
        """creates tables if hasnt already been created"""
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()
        with open("./backend/models.sql", mode="r", encoding="utf-8") as file:
            sql = str(file.read())
            print(sql)
            cursor.executescript(sql)
            cursor.close()
            conn.close()

    def __sql_attempt(self, sql: str) -> list:
        """wrapper for a sql attempt to connect/commit to db (private)

        Args:
            sql (str): sql query in a string

        Returns:
            list: return from db
        """
        self.conn = sqlite3.connect("orders.db")
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        self.conn.commit()
        self.conn.close()
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
        except sqlite3.Error as error:
            self.conn.rollback()
            self.conn.close()
            print("rolling back to prevnt db lock, %s", error)
            raise error
