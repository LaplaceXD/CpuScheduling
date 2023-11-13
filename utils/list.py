from typing import Callable, Iterable, Optional, TypeVar

T = TypeVar('T')

def find(criteria_fn: Callable[[T], bool], iter: Iterable[T]):
    """ Finds and returns a given element in a list based on a given criteria. """
    for elem in iter:
        if criteria_fn(elem):
            return elem
    return None