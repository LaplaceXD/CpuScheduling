from typing import List, TypeVar
from .memory import Memory

T = TypeVar("T")

class LFU(Memory[T]):
    name: str = "Least Frequently Used (LFU)"
    short_name: str = "LFU"
    state_annotation: str = "[ (page, freq), ... ] Sorted by Lowest -> Highest Frequency, then by Oldest -> Newest in Memory"

    def __init__(self, frame_size: int):
        super().__init__(frame_size)
        self._state: List[int] = [0 for _ in range(self._capacity)] # Frequency State
        self.__time_state: List[T] = []                             # Time in Memory State

    @property
    def state(self):
        page_freqs = zip(filter(lambda m : m is not None, self._memory), self._state)
        
        # Sort by count, then time in memory
        sorted_page_freqs = sorted(page_freqs, key=lambda pf : (pf[1], self.__time_state.index(pf[0])))
        return list(sorted_page_freqs)
    
    def load(self, page: T):
        if not self.is_full:
            self._memory[self._size] = page
            self._state[self._size] = 1
            self.__time_state.append(page)
            
            self._size += 1
            return None, True
        elif page not in self._memory:
            least_frequently_used_page, _ = self.state.pop(0) 
            idx_of_least_freq_used = self._memory.index(least_frequently_used_page)
            
            self._memory[idx_of_least_freq_used] = page
            self._state[idx_of_least_freq_used] = 1
            
            self.__time_state.remove(least_frequently_used_page)
            self.__time_state.append(page)
            return least_frequently_used_page, True

        # Increase count of page for each access
        self._state[self._memory.index(page)] += 1
        return None, False