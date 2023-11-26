from copy import deepcopy
from typing import Optional, Generic, TypeVar
from .memories import Memory

T = TypeVar("T")

class MemorySnapshot(Generic[T]):
    def __init__(self, snap_time: int, memory: Memory[T], inserted_page: T, replaced_page: Optional[T], is_fault: bool):
        self.__snapped_on: int = snap_time
        self.__memory: Memory[T] = deepcopy(memory)
        self.__inserted_page: T = inserted_page
        self.__replaced_page: Optional[T] = replaced_page
        self.__is_fault: bool = is_fault

    @property
    def is_hit(self):
        return not self.__is_fault
    
    @property
    def is_fault(self):
        return self.__is_fault
    
    @property
    def status(self):
        return "F" if self.__is_fault else "H"

    @property
    def snapped_on(self):
        return self.__snapped_on

    @property
    def snapshot(self):
        return self.__memory

    @property
    def log(self):
        status = "❌ FAULT " if self.__is_fault else "🎯 HIT   "
        action = "loaded" if self.__is_fault else "found"
        
        page_inserted = "Page {}".format(self.__inserted_page)
        involved_frame = "Frame {}".format(str(self.__memory.frame_of(self.__inserted_page) + 1).zfill(3))
        
        replaced_clause = " replacing page {}".format(self.__replaced_page) if self.__replaced_page is not None else ""

        return "{}: {} {} in {}{}".format(status, page_inserted, action, involved_frame, replaced_clause)