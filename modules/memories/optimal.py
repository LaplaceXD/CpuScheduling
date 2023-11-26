from copy import deepcopy
from typing import List, TypeVar
from .memory import Memory

T = TypeVar("T")

class Optimal(Memory[T]):
    name: str = "Optimal"
    short_name: str = "Optimal"
    state_annotation: str = "[ page, ... ] Sorted from Longest -> Shortest Next Usage Interval"

    def __init__(self, frame_size: int, pages: List[T]):
        super().__init__(frame_size)
        self._state: List[T] = deepcopy(pages)      # Page references to predict the future
        self.__time_state: List[T] = []             # Time in Memory State 

    @property
    def state(self):
        none_removed = [page for page in self._memory if page is not None]
        
        pages_with_next_intervals = [page for page in none_removed if page in self._state]
        no_next_interval_pages = [page for page in none_removed if page not in self._state]

        pages_with_next_intervals.sort(key=lambda page : self._state.index(page), reverse=True) # Sort by their next interval
        no_next_interval_pages.sort(key=lambda page : self.__time_state.index(page)) # Sort by oldest

        # Pages with no intervals have lower purpose to be in memory, since they no longer get hit
        return no_next_interval_pages + pages_with_next_intervals

    def load(self, page: T):
        # We only need to keep track of future pages
        if page in self._state:
            self._state.remove(page)

        if page in self._memory: 
            return None, False
        
        longest_page_usage_interval = None
        frame = self.size
        if self.is_full:
            longest_page_usage_interval = self.state.pop(0)
            frame = self._memory.index(longest_page_usage_interval)
            self.__time_state.remove(longest_page_usage_interval)

        self._memory[frame] = page
        self.__time_state.append(page)
        
        return longest_page_usage_interval, True