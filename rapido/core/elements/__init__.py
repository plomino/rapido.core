from elements import *


def get_element_class(element_type):
    return getattr(elements, element_type.capitalize() + "Element", None)