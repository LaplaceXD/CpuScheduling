class Clock:
    def __init__(self, start_time: int = 0):
        self.__time = start_time
        self.__start_time = start_time

    @property
    def start_time(self):
        return self.__start_time
    
    @property
    def time(self):
        return self.__time
    
    def tick(self):
        self.__time += 1
