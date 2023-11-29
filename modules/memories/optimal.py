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
        self.__pages: List[T] = deepcopy(pages)
        self.__arrival_queue: List[T] = []

    @property
    def state(self):
        mem_items = [page for page in self._memory if page is not None]
        sort_by_page_interval = lambda p : self.__pages.index(p) if p in self.__pages else len(self.__pages) 
        sort_by_arrival = lambda p : self.__arrival_queue.index(p)
        
        # -1 to sort by arrival in descending order
        mem_items.sort(key=lambda page : (sort_by_page_interval(page), -1 * sort_by_arrival(page)), reverse=True)
        return mem_items

    def load(self, page: T):
        replaced_page, is_fault = None, False
        
        # We only care about the next set of pages
        if page in self.__pages:
            self.__pages.remove(page)
        
        if page not in self._memory:
            # frame is defaulted to size, since we want to insert sequentially 
            # into None filled spaces in memory until it is full
            frame, is_fault = self.size, True

            if self.is_full:
                replaced_page = self.state.pop(0)
                frame = self._memory.index(replaced_page)
                self.__arrival_queue.remove(replaced_page)

            self._memory[frame] = page
            self.__arrival_queue.append(page)
        
        return replaced_page, is_fault
