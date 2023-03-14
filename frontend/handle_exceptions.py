from custom.exceptions import NoKeyError, WhatThreeWordsError
from functools import wraps
from frontend.pop_up import UpdateMsg
from sqlite3 import IntegrityError


def handle_3words_exceptions(func: object):
    """handle exceptions from the what three words api

    Args:
        func (function): function to be decorated

    Returns:
        decorator
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            UpdateMsg("Please enter valid co ordinates!")
            print(error)
        except NoKeyError as error:
            UpdateMsg("Please Ensure there is a valid api key!")
            print(error)
        except WhatThreeWordsError as error:
            UpdateMsg("Something went wrong with the what three words api!")
            print(error)
        except Exception as error:
            UpdateMsg("Something went wrong!")
            print(error)

    return decorated


def handle_db_exceptions(func: object):
    """decorator to handle exceptions from the database

    Args:
        func (function): function to be decorated

    Returns:
        decorator
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as error:
            print(error)
            UpdateMsg("operation failed - is the item unique?")
        except ValueError as error:
            print(error)
            UpdateMsg("Please enter a valid data format!")
        except NotImplementedError as error:
            print(error)
            UpdateMsg("Item does not exist! - check the Menu!")
        except Exception as error:
            print(error)
            UpdateMsg("Something went wrong!")

    return decorated
