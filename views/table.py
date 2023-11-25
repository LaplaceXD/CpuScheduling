from typing import List, Any
from views import View

class TableView(View):
    def __init__(self, min_cell_width: int = 5, headers: List[str] = []):
        super().__init__(min_cell_width)
        self.__data: List[List[Any]] = []
        self.__headers: List[str] = headers

        if len(headers) > 0: 
            self._adjust_cell_sizes_to_fit(*headers)

    def __str__(self):
        table = ""
        sep_line = self._create_separator_line()

        if len(self.__headers) > 0:
            table += sep_line + "\n"
            table += self._format_row(self.__headers) + "\n"

        table += sep_line + "\n"
        for data in self.__data:
            table += self._format_row(data) + "\n"
        table += sep_line
        
        return table
    
    def add_item(self, *data: Any):
        self._adjust_cell_sizes_to_fit(*data)
        self.__data.append(data)
        return self
    
    def render(self):
        print(self)