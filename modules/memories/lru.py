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
        if not self.is_full:
            self._memory[self._size] = page
            self._size += 1
            
            self._state.append(page)
            return None, True
        elif page not in self._memory:
            least_recently_used_page = self._state.pop(0)
            self._memory[self._memory.index(least_recently_used_page)] = page
            
            self._state.append(page)
            return least_recently_used_page, True

        # Refresh the recency of usage of the item in memory
        self._state.remove(page)
        self._state.append(page)
        return None, False