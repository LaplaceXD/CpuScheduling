from typing import List, TypeVar
from .memory import Memory

T = TypeVar("T")

class LRU(Memory[T]):
    name: str = "Least Recently Used (LRU)"
    short_name: str = "LRU"
    state_annotation: str = "[ page, ... ] Sorted from Least -> Most Recently Used"

    def __init__(self, frame_size: int):
        super().__init__(frame_size)
        self._state: List[T] = []

    def load(self, page: T):
        if page in self._memory: 
            self._state.remove(page)
            self._state.append(page)
            return None, False
        
        least_recently_used_page = None
        frame = self.size
        if self.is_full:
            least_recently_used_page = self._state.pop(0)
            frame = self._memory.index(least_recently_used_page)

        self._memory[frame] = page
        self._state.append(page)

        return least_recently_used_page, True