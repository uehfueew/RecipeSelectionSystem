from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Sequence, TypeVar

T = TypeVar('T')

class SortingAlgorithm(ABC):
    @abstractmethod
    def sort(self, items: Sequence[T], key_func: Optional[Callable[[T], object]] = None, reverse: bool = False) -> List[T]:
        raise NotImplementedError

class BubbleSort(SortingAlgorithm):
    def sort(self, items: Sequence[T], key_func: Optional[Callable[[T], object]] = None, reverse: bool = False) -> List[T]:
        key = key_func or (lambda x: x)
        arr = list(items)
        n = len(arr)
        if n < 2: return arr
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                should_swap = key(arr[j]) < key(arr[j + 1]) if reverse else key(arr[j]) > key(arr[j + 1])
                if should_swap:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped: break
        return arr

class MergeSort(SortingAlgorithm):
    def sort(self, items: Sequence[T], key_func: Optional[Callable[[T], object]] = None, reverse: bool = False) -> List[T]:
        key = key_func or (lambda x: x)
        arr = list(items)
        if len(arr) < 2: return arr
        mid = len(arr) // 2
        left = self.sort(arr[:mid], key, reverse)
        right = self.sort(arr[mid:], key, reverse)
        return self._merge(left, right, key, reverse)

    def _merge(self, left: List[T], right: List[T], key: Callable[[T], object], reverse: bool) -> List[T]:
        merged: List[T] = []
        i = j = 0
        while i < len(left) and j < len(right):
            is_less_or_equal = key(left[i]) >= key(right[j]) if reverse else key(left[i]) <= key(right[j])
            if is_less_or_equal:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged
