from typing import List, TypeVar
from .memory import Memory

T = TypeVar("T")

class LFU(Memory[T]):
    name: str = "Least Frequently Used (LFU)"
    short_name: str = "LFU"
    state_annotation: str = "[ (page, freq), ... ] Sorted by Lowest -> Highest Frequency, then by Oldest -> Newest in Memory"

    def __init__(self, frame_size: int):
        super().__init__(frame_size)
        self.__frequencies: List[int] = [0] * self._capacity
        self.__arrival_queue: List[T] = []

    @property
    def state(self):
        page_freqs = zip((page for page in self._memory if page is not None), self.__frequencies)
        
        # Sort by count, then time in memory
        sorted_page_freqs = sorted(page_freqs, key=lambda pf : (pf[1], self.__arrival_queue.index(pf[0])))
        return list(sorted_page_freqs)
    
    def load(self, page: T):
        replaced_page, is_fault = None, False
        
        if page not in self._memory:
            # frame is defaulted to size, since we want to insert sequentially 
            # into None filled spaces in memory until it is full
            frame, is_fault = self.size, True

            if self.is_full:
                replaced_page, _ = self.state.pop(0)
                frame = self._memory.index(replaced_page)
                self.__arrival_queue.remove(replaced_page)

            self._memory[frame] = page
            self.__frequencies[frame] = 1
            self.__arrival_queue.append(page)
        else:
            self.__frequencies[self._memory.index(page)] += 1
        
        return replaced_page, is_fault
