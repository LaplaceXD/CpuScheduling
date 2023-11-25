from itertools import count
from typing import Any, List
from abc import ABC, abstractmethod

class View(ABC):
    def __init__(self, min_cell_width: int = 5):
        self._min_cell_width: int = min_cell_width
        self._cell_widths: List[int] = []

    def _adjust_cell_size_at(self, at: int, content: Any):
        """ Adjust the cell size at a particular position to fit the length of a content. """
        if len(self._cell_widths) <= at:
            for _ in range(len(self._cell_widths) - at + 1):
                self._cell_widths.append(self._min_cell_width)

        self._cell_widths[at] = max(len(str(content)), self._cell_widths[at])

    def _adjust_cell_sizes_to_fit(self, *content: Any):
        """ Adjust the cell sizes to fit according to the length of each stringified content. """
        if len(self._cell_widths) == 0:
            self._cell_widths = [self._min_cell_width for _ in range(len(content))]

        for i, c, w in zip(count(), content, self._cell_widths):
            self._cell_widths[i] = max(len(str(c)), w)
    
    def _format_row(self, items: List[Any], sep: str = "|"):
        """ 
            Formats a list of items to a row of formatted cells that are contained in a 
            fixed cell width, and are separated by a given separator. 
        """

        row = ""
        row += sep
        row += sep.join(["{:>{}}".format(item, cell_width) for item, cell_width in zip(items, self._cell_widths)]) 
        row += sep

        return row

    def _create_separator_line(self, joint: str = "+", line: str = "-"):
        return joint + joint.join([line * w for w in self._cell_widths]) + joint

    @abstractmethod
    def add_item(self):
        "Add an item to the view."
        pass

    @abstractmethod
    def render(self):
        """ Render the given view to the console. """
        pass 