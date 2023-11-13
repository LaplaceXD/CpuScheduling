from typing import List, Any
from views import View

class Table(View):
    def __init__(self, cell_width: int = 5, headers: List[str] = []):
        super().__init__(cell_width)
        self.__data: List[List[Any]] = []
        self.__headers: List[str] = headers

    def add_data(self, *data: Any):
        """ Add data to the table. """
        self.__data.append(data)
        return self

    def render(self):
        table = ""
        bar_line = "+" + "-" * ((self._cell_width + 1) * len(self.__headers) - 1) + "+\n"
        
        table += bar_line
        table += self._format_items(self.__headers) + "\n"
        table += bar_line

        for data in self.__data:
            table += self._format_items(data) + "\n"
        
        table += bar_line
        print(table)