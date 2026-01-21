"""
Sorting Module
──────────────
This module provides two sorting algorithms (BubbleSort and MergeSort) for sorting recipes.

Both algorithms can sort recipes by any attribute (price, time, calories, etc.) in ascending
or descending order. This allows comparisons of algorithm performance.

Key Concepts:
- Both implement the SortingAlgorithm interface (abstract base class)
- BubbleSort: O(n²) time complexity - slower but simpler
- MergeSort: O(n log n) time complexity - faster but more complex
"""

from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Sequence, TypeVar

# TypeVar 'T' allows these functions to work with ANY type of object
T = TypeVar('T')

class SortingAlgorithm(ABC):
    """
    Abstract base class that defines the interface for all sorting algorithms.
    
    Any sorting algorithm must implement the sort() method.
    This ensures all algorithms have consistent method signatures.
    """
    @abstractmethod
    def sort(self, items: Sequence[T], key_func: Optional[Callable[[T], object]] = None, reverse: bool = False) -> List[T]:
        """
        Sorts a sequence of items and returns a new sorted list.
        
        Args:
            items: The sequence to sort (can be a list, tuple, etc.)
            key_func: A function that extracts the sorting key from each item
                     Examples:
                     - lambda r: r.price  (sort by price)
                     - lambda r: r.time_minutes  (sort by cooking time)
            reverse: If False (default), sort ascending (smallest first)
                    If True, sort descending (largest first)
                    
        Returns:
            A new sorted list (does not modify the original)
        """
        raise NotImplementedError

class BubbleSort(SortingAlgorithm):
    """
    Bubble Sort Algorithm
    ─────────────────────
    Time Complexity: O(n²) - Gets slow with large lists
    Space Complexity: O(1) - Uses only constant extra space
    
    How it works:
    1. Compare adjacent items in the list
    2. If they're in the wrong order, swap them
    3. Repeat until no more swaps are needed (list is sorted)
    
    When to use: Good for learning, but avoid for large datasets
    """
    
    def sort(self, items: Sequence[T], key_func: Optional[Callable[[T], object]] = None, reverse: bool = False) -> List[T]:
        """
        Sorts items using the Bubble Sort algorithm.
        
        Args:
            items: Sequence to sort
            key_func: Function to extract sort key from each item
            reverse: If True, sort in descending order
            
        Returns:
            A new sorted list
        """
        # Use default identity function if no key function provided
        key = key_func or (lambda x: x)
        # Convert input to a list we can modify
        arr = list(items)
        n = len(arr)
        
        # If list has 0 or 1 items, it's already sorted
        if n < 2: 
            return arr
        
        # Outer loop: repeat sorting passes
        for i in range(n):
            swapped = False
            # Inner loop: compare adjacent elements
            for j in range(0, n - i - 1):
                # Determine if we should swap (depends on reverse flag)
                should_swap = key(arr[j]) < key(arr[j + 1]) if reverse else key(arr[j]) > key(arr[j + 1])
                if should_swap:
                    # Swap adjacent elements
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            # Early exit: if no swaps occurred, list is already sorted
            if not swapped: 
                break
        
        return arr

class MergeSort(SortingAlgorithm):
    """
    Merge Sort Algorithm (Divide & Conquer)
    ───────────────────────────────────────
    Time Complexity: O(n log n) - Much faster for large lists
    Space Complexity: O(n) - Requires extra space for merging
    
    How it works:
    1. Divide: Split list in half recursively until lists have 1 item
    2. Conquer: Merge pairs of sorted lists back together in sorted order
    3. Result: Final merged list is fully sorted
    
    When to use: Better than BubbleSort for large datasets (>100 items)
    """
    
    def sort(self, items: Sequence[T], key_func: Optional[Callable[[T], object]] = None, reverse: bool = False) -> List[T]:
        """
        Sorts items using the Merge Sort algorithm (recursive divide-and-conquer).
        
        Args:
            items: Sequence to sort
            key_func: Function to extract sort key from each item
            reverse: If True, sort in descending order
            
        Returns:
            A new sorted list
        """
        # Use default identity function if no key function provided
        key = key_func or (lambda x: x)
        # Convert input to a list we can modify
        arr = list(items)
        
        # Base case: if list has 0 or 1 items, it's already sorted
        if len(arr) < 2: 
            return arr
        
        # Divide: Find the middle point to split the list
        mid = len(arr) // 2
        # Recursively sort the left half
        left = self.sort(arr[:mid], key, reverse)
        # Recursively sort the right half
        right = self.sort(arr[mid:], key, reverse)
        
        # Conquer: Merge the two sorted halves back together
        return self._merge(left, right, key, reverse)

    def _merge(self, left: List[T], right: List[T], key: Callable[[T], object], reverse: bool) -> List[T]:
        """
        Merges two sorted lists into one sorted list.
        
        This is the "merge" step in merge sort. It efficiently combines two sorted lists
        by comparing elements from each list and taking the smaller (or larger) one.
        
        Args:
            left: First sorted list
            right: Second sorted list
            key: Function to extract sort key for comparison
            reverse: If True, use descending order logic
            
        Returns:
            A new merged and sorted list
        """
        merged: List[T] = []
        # Pointers for left and right lists
        i = j = 0
        
        # Compare elements from both lists and add the smaller one (or larger if reverse)
        while i < len(left) and j < len(right):
            # Determine which element should come first
            is_less_or_equal = key(left[i]) >= key(right[j]) if reverse else key(left[i]) <= key(right[j])
            if is_less_or_equal:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        
        # Add any remaining elements from left list
        merged.extend(left[i:])
        # Add any remaining elements from right list
        merged.extend(right[j:])
        
        return merged
