from typing import TypeVar, Generic, List, Callable

T = TypeVar('T')

class Signal(Generic[T]):
    """ A class that events signals to subscribed functions. """

    def __init__(self):
        self.__subscribers: List[Callable[[T], None]]= []

    def listen(self, fn: Callable[[T], None]):
        """ Subscribe a function to the signal, if it has not been subscribed. """
        if fn not in self.__subscribers:
            self.__subscribers.append(fn)

    def ignore(self, fn: Callable[[T], None]):
        """ Remove a function's subscription from the signal. """
        if fn in self.__subscribers:
            self.__subscribers.remove(fn)

    def emit(self, payload: T):
        """ Emit the signal with a given payload to all subscribers. """
        for fn in self.__subscribers:
            fn(payload)