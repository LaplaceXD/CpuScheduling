from typing import Any, List
from abc import ABC, abstractmethod

class View(ABC):
    def __init__(self, cell_width: int):
        self._cell_width: int = cell_width

    def _format_item(self, item: Any):
        """ Formats an item to a string of a given cell width. """        
        return "{:>{}}".format(item, self._cell_width)

    def _format_items(self, items: List[Any], sep: str = "|"):
        """ Formats a list of items to a row of formatted cells that are separated by a given separator. """        
        row = ""
        row += sep
        row += sep.join([self._format_item(i) for i in items]) 
        row += sep

        return row

    @abstractmethod
    def render(self):
        """ Render the given view to the console. """
        pass 