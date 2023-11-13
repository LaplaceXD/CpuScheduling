from typing import TypeVar, Generic, List, Callable

T = TypeVar('T')

class Signal(Generic[T]):
    def __init__(self):
        self.__subscribers: List[Callable[[T], None]]= []

    def listen(self, fn: Callable[[T], None]) -> None:
        """ Subscribe a function to the signal, if it has not been subscribed. """
        if fn not in self.__subscribers:
            self.__subscribers.append(fn)

    def ignore(self, fn: Callable[[T], None]) -> None:
        """ Remove a function's subscription from the signal. """
        if fn in self.__subscribers:
            self.__subscribers.remove(fn)

    def emit(self, payload: T) -> None:
        """ Emit the signal with a given payload to all subscribers. """
        for fn in self.__subscribers:
            fn(payload)