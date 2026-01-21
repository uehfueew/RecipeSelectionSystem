"""
Unit Tests for Recipe Selection System
═══════════════════════════════════════

This module contains automated tests that verify the recipe system works correctly.

Tests cover:
- Loading recipes from CSV files
- Searching recipes (by name, category, ingredient)
- Evaluating boolean logic expressions
- Generating truth tables
- Sorting algorithms (Bubble Sort and Merge Sort)
- Multiple sort keys (primary and secondary)

Run tests with: python -m unittest test_demo.py
Or:             python test_demo.py
"""

import os
import unittest

from recipe_system.logic import eval_expr, truth_table
from recipe_system.manager import RecipeManager
from recipe_system.recipe import Recipe
from recipe_system.sorting import BubbleSort, MergeSort


class TestRecipeSystem(unittest.TestCase):
    """Test suite for the entire recipe system."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that run once before all tests."""
        # Find the path to the test data CSV file
        cls.data_path = os.path.join(os.path.dirname(__file__), "recipes.csv")

    def setUp(self):
        """Set up fresh test fixtures before each test method."""
        # Create a new manager and load recipes for each test
        self.manager = RecipeManager()
        self.manager.load_csv(self.data_path)

    def test_load_csv(self):
        """Test 1: Verify that CSV file loads correctly and has expected data."""
        # Check that we loaded exactly 5 recipes
        self.assertEqual(len(self.manager.recipes), 5)
        # Check that the first recipe is correct
        self.assertEqual(self.manager.recipes[0].name, "Chicken Salad")

    def test_search_methods(self):
        """Test 2: Verify all search methods work correctly."""
        # Test search by exact name
        self.assertIsNotNone(self.manager.find_by_name("Pancakes"))
        
        # Test search by category
        mains = self.manager.search_by_category("main")
        self.assertEqual(len(mains), 2)
        
        # Test search by ingredient
        chicken_matches = {r.name for r in self.manager.search_by_ingredient("chicken")}
        self.assertIn("Chicken Salad", chicken_matches)

    def test_eval_expression(self):
        """Test 3: Verify that boolean expression evaluation works correctly."""
        # Get a sample recipe and create a boolean environment for it
        salad = self.manager.find_by_name("Chicken Salad")
        env = {
            "contains_chicken": any("chicken" in i.lower() for i in salad.ingredients),
            "cheap": salad.price < 4.0,
            "quick": salad.time_minutes <= 15,
            "healthy": salad.calories < 400,
        }
        # This expression should be True for Chicken Salad
        self.assertTrue(eval_expr("(contains_chicken and quick) or healthy", env))

        # Test with a different recipe
        pancakes = self.manager.find_by_name("Pancakes")
        env_pan = {
            "contains_chicken": any("chicken" in i.lower() for i in pancakes.ingredients),
            "cheap": pancakes.price < 4.0,
            "quick": pancakes.time_minutes <= 15,
            "healthy": pancakes.calories < 400,
        }
        # Pancakes are cheap but not contain chicken
        self.assertFalse(eval_expr("contains_chicken", env_pan))
        self.assertTrue(eval_expr("cheap", env_pan))

    def test_truth_table(self):
        """Test 4: Verify that truth tables are generated correctly."""
        # Generate truth table for "A and B"
        vars_, rows = truth_table("A and B")
        
        # Expected variables in alphabetical order
        self.assertEqual(vars_, ["A", "B"])
        
        # Expected truth table rows: (inputs, output)
        # 0,0 -> 0 (F and F = F)
        # 0,1 -> 0 (F and T = F)
        # 1,0 -> 0 (T and F = F)
        # 1,1 -> 1 (T and T = T)
        expected = [([0, 0], 0), ([0, 1], 0), ([1, 0], 0), ([1, 1], 1)]
        self.assertEqual(rows, expected)

    def test_bubble_sort_by_time(self):
        """Test 5: Verify that Bubble Sort correctly sorts recipes by cooking time."""
        sorter = BubbleSort()
        # Sort all recipes by their cooking time
        sorted_list = sorter.sort(self.manager.recipes, key_func=lambda r: r.time_minutes)
        
        # Extract the times from sorted list
        times = [r.time_minutes for r in sorted_list]
        
        # Verify they are in ascending order (matches sorted times)
        self.assertEqual(times, sorted(times))

    def test_merge_sort_matches_bubble(self):
        """Test 6: Verify that Merge Sort and Bubble Sort produce identical results."""
        # Define a sort key (by price)
        key = lambda r: r.price
        
        # Sort using both algorithms
        bubble = BubbleSort().sort(self.manager.recipes, key_func=key)
        merge = MergeSort().sort(self.manager.recipes, key_func=key)
        
        # Both should produce the same order
        self.assertEqual([r.name for r in merge], [r.name for r in bubble])

    def test_secondary_key_sort(self):
        """Test 7: Verify sorting with both primary and secondary keys works correctly."""
        # Create test recipes with specific attributes
        items = [
            Recipe("Healthy Tie", "main", 4.0, 30, ["veg"], ["cook"], 200, "Easy"),
            Recipe("Less Healthy", "main", 4.0, 30, ["veg"], ["cook"], 450, "Medium"),
            Recipe("Different Price", "main", 3.0, 25, ["veg"], ["cook"], 600, "Hard"),
        ]

        # Define a complex key function that sorts by price first, then by health
        def key_func(r: Recipe):
            env = {
                "contains_chicken": any("chicken" in i.lower() for i in r.ingredients),
                "cheap": r.price < 4.0,
                "quick": r.time_minutes <= 15,
                "healthy": r.calories < 400,
            }
            # Secondary key: 0 if healthy, 1 if not healthy
            secondary = 0 if eval_expr("healthy", env) else 1
            # Primary key: price, secondary key: health
            return (r.price, secondary)

        # Sort using Merge Sort
        sorted_items = MergeSort().sort(items, key_func=key_func)
        
        # The first two items should be "Different Price" (cheaper) and "Healthy Tie" (healthy at same price)
        self.assertEqual([r.name for r in sorted_items][:2], ["Different Price", "Healthy Tie"])


if __name__ == "__main__":
    # Run all tests when this file is executed directly
    unittest.main()
