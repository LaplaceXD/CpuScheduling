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
        self._state: List[T] = deepcopy(pages)

    @property
    def state(self):
        none_removed = filter(lambda page : page is not None, self._memory)
        return sorted(none_removed, key=lambda page : self._state.index(page) if page in self._state else len(self._state), reverse=True)

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

        self._memory[frame] = page
        return longest_page_usage_interval, True