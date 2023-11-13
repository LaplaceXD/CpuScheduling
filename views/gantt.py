from typing import List
from views import View

class Gantt(View):
    def __init__(self, cell_width: int = 4, start_time: int = 0):
        super().__init__(cell_width)
        self.__start_time: int = start_time
        self.__labels: List[str] = []
        self.__timestamps: List[int] = []

    def add_data(self, name: str, time: int):
        """ Add data to the gantt. """
        self.__labels.append(name)
        self.__timestamps.append(time)
        return self
    
    def render(self):
        gantt = ""
        bar_line = ("+" + "-" * self._cell_width) * len(self.__labels) + "+\n"

        gantt += bar_line
        gantt += self._format_items(self.__labels) + "\n"
        gantt += bar_line
        gantt += str(self.__start_time) + self._format_items(self.__timestamps, sep=" ")

        print(gantt)