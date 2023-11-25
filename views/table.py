from typing import List, Any
from views import View

class TableView(View):
    def __init__(self, min_cell_width: int = 5, header: List[str] = [], footer: List[str] = []):
        super().__init__(min_cell_width)
        self.__data: List[List[Any]] = []
        self.__header: List[str] = header
        self.__footer: List[str] = footer

        if len(header) > 0: 
            self._adjust_cell_sizes_to_fit(*header)
        if len(footer) > 0: 
            self._adjust_cell_sizes_to_fit(*footer)

    def __str__(self):
        table = ""
        sep_line = self._create_separator_line()

        if len(self.__header) > 0:
            table += sep_line + "\n"
            table += self._format_row(self.__header) + "\n"

        table += sep_line + "\n"
        for data in self.__data:
            table += self._format_row(data) + "\n"
        table += sep_line
        
        if len(self.__footer) > 0:
            table += "\n"
            table += self._format_row(self.__footer) + "\n"
            table += sep_line
        
        return table
    
    def add_item(self, *data: Any):
        self._adjust_cell_sizes_to_fit(*data)
        self.__data.append(data)
        return self
    
    def render(self):
        print(self)