from typing import List, Generic, TypeVar
from .memory_snapshot import MemorySnapshot

T = TypeVar("T")

class MemoryMetrics(Generic[T]):
    def __init__(self, memory_snapshots: List[MemorySnapshot[T]]):
        self.__snapshot_length = len(memory_snapshots)
        self.__memory_name = memory_snapshots[0].snapshot.extended_name if self.__snapshot_length > 0 else ""
        self.__hits = [s.is_hit for s in memory_snapshots].count(True)

    @property
    def memory_name(self):
        return self.__memory_name

    @property
    def runtime(self):
        return self.__snapshot_length
    
    @property
    def hits(self):
        return self.__hits
    
    @property
    def faults(self):
        return self.__snapshot_length - self.__hits
    
    @property
    def hit_ratio(self):
        return self.__hits / self.__snapshot_length
    
    @property
    def fault_ratio(self):
        return self.faults / self.__snapshot_length
    
    @property
    def hit_percent(self):
        return "{:.2f}%".format(self.hit_ratio * 100)
    
    @property
    def fault_percent(self):
        return "{:.2f}%".format(self.fault_ratio * 100)