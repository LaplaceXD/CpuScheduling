from typing import List, Optional
from views import View

class GanttView(View):
    def __init__(self, name: str = "", show_timestamps: bool = True, min_cell_width: int = 4, start_time: int = 0):
        super().__init__(min_cell_width)
        self.__name: str = name 
        self.__show_timestamps: bool = show_timestamps 
        self.__start_time: int = start_time
        
        self.__labels: List[str] = []
        self.__timestamps: List[int] = []


    def __str__(self):
        gantt = ""
        name_padding = " " (len(self.__name) + 1) if self.__name else "" 
        name = self.__name + " " if self.__name else "" 

        bar_line = name_padding + "+" + "+".join(["-" * w for w in self._cell_widths]) + "+"

        gantt += bar_line + "\n"
        gantt += name + self._format_row(self.__labels) + "\n"
        gantt += bar_line
        
        if self.__show_timestamps:
            gantt += "\n" + name_padding + str(self.__start_time) + self._format_row(self.__timestamps, sep=" ")
        
        return gantt

    def add_data(self, name: str, time: int):
        """ Add data to the gantt. """
        self._adjust_cell_size_at(len(self.__labels), name)
        self.__labels.append(name)
        self.__timestamps.append(time)
        return self

    def render(self):
        print(self)