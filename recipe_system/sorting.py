from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Sequence, TypeVar

T = TypeVar("T")


class SortingAlgorithm(ABC):
    """Abstract base for sorting strategies."""

    @abstractmethod
    def sort(self, items: Sequence[T], key_func: Optional[Callable[[T], object]] = None) -> List[T]:
        """Return a sorted copy of *items* using the provided key function."""
        raise NotImplementedError


class BubbleSort(SortingAlgorithm):
    """Loop-based, stable bubble sort implementation."""

    def sort(self, items: Sequence[T], key_func: Optional[Callable[[T], object]] = None) -> List[T]:
        key = key_func or (lambda x: x)
        arr = list(items)
        n = len(arr)
        if n < 2:
            return arr
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if key(arr[j]) > key(arr[j + 1]):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:
                break
        return arr


class MergeSort(SortingAlgorithm):
    """Recursive, stable merge sort implementation."""

    def sort(self, items: Sequence[T], key_func: Optional[Callable[[T], object]] = None) -> List[T]:
        key = key_func or (lambda x: x)
        arr = list(items)
        if len(arr) < 2:
            return arr
        mid = len(arr) // 2
        left = self.sort(arr[:mid], key)
        right = self.sort(arr[mid:], key)
        return self._merge(left, right, key)

    def _merge(self, left: List[T], right: List[T], key: Callable[[T], object]) -> List[T]:
        merged: List[T] = []
        i = j = 0
        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        if i < len(left):
            merged.extend(left[i:])
        if j < len(right):
            merged.extend(right[j:])
        return merged

