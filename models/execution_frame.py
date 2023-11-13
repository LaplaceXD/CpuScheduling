class ExecutionFrame:
    """ A frame that records the start time, end time, and name of a certain execution. """

    def __init__(self, name: str, start_time: int, end_time: int):
        self.__name: str = name
        self.__start: int = start_time
        self.__end: int = end_time

    @property
    def name(self):
        return self.__name
    
    @property
    def start(self):
        return self.__start
    
    @property
    def end(self):
        return self.__end
    
    @property
    def span(self):
        return self.__end - self.__end