from enum import Enum


class ElementType(str, Enum):
    product = 'product'
    location = 'location'
    raport = 'raport'


def automatizations_checker(element: ElementType, id: str, details: dict):
    # DEVONLY: Bypass checking automation
    # return fn(*args, **kwargs)
    # Check if there is automation saved in DB
    # IF SO -> execute it
    print(element)
