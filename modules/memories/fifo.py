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
        if page in self._memory: 
            return None, False
        
        oldest_page = None
        frame = self.size
        if self.is_full:
            oldest_page = self._state.pop(0)
            frame = self._memory.index(oldest_page)

        self._memory[frame] = page
        self._state.append(page)

        return oldest_page, True