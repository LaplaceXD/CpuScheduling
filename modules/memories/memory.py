
from typing import Optional, List, Any, Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")

class Memory(ABC, Generic[T]):
    name: str = "Memory"
    short_name: str = "Memory"
    state_annotation: str = "No State"
    
    def __init__(self, frame_size: int):
        self._memory: List[Optional[T]] = [None] * frame_size
        self._capacity: int = frame_size
        self.__iter_ptr: int = 0

    def __eq__(self, other: 'Memory'):
        return self.name == other.name and self.size == other.size and self._capacity == other.capacity and all(a == b for a, b in zip(self._memory, other))
    
    def __getitem__(self, idx: int):
        return self._memory[idx]
    
    def __iter__(self):
        self.__iter_ptr = 0
        return self

    def __next__(self):
        if self.__iter_ptr < self._capacity:
            value = self._memory[self.__iter_ptr]
            self.__iter_ptr += 1
            return value
        
        raise StopIteration

    def __len__(self):
        """ The current number of frames that is in memory. """
        return self._capacity - self._memory.count(None)
    
    def __str__(self):
        return str(self._memory)
    
    @property
    def extended_name(self):
        return self.name + " | frames=" + str(self._capacity)

    @property
    def capacity(self):
        """ The max number of frames that can be stored in memory. """
        return self._capacity

    @property
    def size(self):
        """ The current number of frames that is in memory. """
        return len(self)
    
    @property
    def is_full(self):
        return self.size == self._capacity
    
    @property
    def is_empty(self):
        return self.size == 0

    @property
    def state(self) -> Any:
        return None
    
    def frame_of(self, page: T) -> int:
        """ 
            Retrieve the frame number of the given page. It returns -1 
            if the page is not in memory. 
        """
        if page in self._memory:
            return self._memory.index(page)
        return -1
    
    def frame_label_of(self, page: T, min_padding: int = 3) -> str:
        """ 
            Retrieve the frame number of the given page. But it is
            in its padded form for presentation.
        """
        frame = self.frame_of(page)
        if frame == -1:
            return "N/A"
        return str(frame + 1).zfill(max(min_padding, len(str(self._capacity))))

    @abstractmethod
    def load(self, page: T) -> tuple[Optional[int], bool]:
        """ 
            Loads a page into a memory frame. It returns a tuple
            containing the replaced page, followed by the loading status.
            The replaced page is the page is the page that was replaced
            in the memory, if there was no page that was replaced it returns
            None. The loading status tells whether the loading of the page
            replaced a page in memory.
        """
        pass
