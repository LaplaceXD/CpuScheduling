from typing import List, TypeVar
from .memory import Memory

T = TypeVar("T")

class FIFO(Memory[T]):
    name: str = "First-In, First-Out (FIFO)"
    short_name: str = "FIFO"
    state_annotation: str = "[ page, ... ] Sorted from Oldest -> Newest in Memory"
    
    def __init__(self, frame_size: int):
        super().__init__(frame_size)
        self.__arrival_queue: List[T] = []

    @property
    def state(self):
        return self.__arrival_queue

    def load(self, page: T):
        replaced_page, is_fault = None, False
        
        if page not in self._memory:
            # frame is defaulted to size, since we want to insert sequentially 
            # into None filled spaces in memory until it is full
            frame, is_fault = self.size, True

            if self.is_full:
                replaced_page = self.state.pop(0)
                frame = self._memory.index(replaced_page)

            self._memory[frame] = page
            self.__arrival_queue.append(page)
        
        return replaced_page, is_fault
