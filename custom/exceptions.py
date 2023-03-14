"""custom exceptions used by both front end and backend
whislt this technically counts as higher coupling, I would 
argue that this would normally be imported in a package
and therfore would not be a problem, I cannot so instead
have produced this. It could have been avoided by misusing python
exceptions but theis was less pythonic than making custom ones 
and sufferign the higher coupling"""
class NoKeyError(Exception):
    """raised when no key is found in the environment"""

    pass

class WhatThreeWordsError(Exception):
    """raised when there is a problem with the what three words api"""

    pass