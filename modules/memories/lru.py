from typing import List, TypeVar
from .memory import Memory

T = TypeVar("T")

class LRU(Memory[T]):
    name: str = "Least Recently Used (LRU)"
    short_name: str = "LRU"
    state_annotation: str = "[ page, ... ] Sorted from Least -> Most Recently Used"

    def __init__(self, frame_size: int):
        super().__init__(frame_size)
        self.__usage_queue: List[T] = []

    @property
    def state(self):
        return self.__usage_queue

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
        else:
            self.__usage_queue.remove(page)

        self.__usage_queue.append(page)
        return replaced_page, is_fault
