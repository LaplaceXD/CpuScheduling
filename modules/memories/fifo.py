from typing import List, TypeVar
from .memory import Memory

T = TypeVar("T")

class FIFO(Memory[T]):
    name: str = "First-In, First-Out (FIFO)"
    short_name: str = "FIFO"
    state_annotation: str = "[ page, ... ] Sorted from Oldest -> Newest in Memory"
    
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
            oldest_page = self._state.pop(0)
            self._memory[self._memory.index(oldest_page)] = page
            
            self._state.append(page)
            return oldest_page, True
        
        return None, False