from typing import List, Optional
from views import View

class GanttView(View):
    def __init__(self, name: Optional[str] = None, show_timestamps: bool = True, cell_width: int = 4, start_time: int = 0):
        super().__init__(cell_width)
        self.__name: Optional[str] = name 
        self.__show_timestamps: bool = show_timestamps 
        self.__start_time: int = start_time
        
        self.__labels: List[str] = []
        self.__timestamps: List[int] = []


    def __str__(self):
        gantt = ""
        name_padding = ""
        name = ""
        if self.__name is not None:
            name_padding = " " * (len(self.__name) + 1)
            name = self.__name + " "

        bar_line = name_padding + ("+" + "-" * self._cell_width) * len(self.__labels) + "+"

        gantt += bar_line + "\n"
        gantt += name + self._format_items(self.__labels) + "\n"
        gantt += bar_line
        
        if self.__show_timestamps:
            gantt += "\n" + name_padding + str(self.__start_time) + self._format_items(self.__timestamps, sep=" ")
        
        return gantt

    def add_data(self, name: str, time: int):
        """ Add data to the gantt. """
        self.__labels.append(name)
        self.__timestamps.append(time)
        return self

    def render(self):
        print(self)