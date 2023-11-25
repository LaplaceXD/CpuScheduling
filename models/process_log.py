from typing import Optional

class ProcessLog:
    """ A frame that records the start time, end time, and name of the execution of a process. """

    def __init__(self, name: str, start_time: int, end_time: int, tag: int = None):
        self.__name: str = name
        self.__tag: Optional[int] = tag
        self.__start: int = start_time
        self.__end: int = end_time

    @property
    def name(self):
        """ The name of the process or its pid."""
        return self.__name
    
    @property
    def tag(self):
        """ A tagging number to allow for grouping of processes based on a value. """
        return self.__tag
    
    @property
    def start(self):
        return self.__start
    
    @property
    def end(self):
        return self.__end