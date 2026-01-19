import os
import unittest

from recipe_system.logic import eval_expr, truth_table
from recipe_system.manager import RecipeManager
from recipe_system.recipe import Recipe
from recipe_system.sorting import BubbleSort, MergeSort


class TestRecipeSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.join(os.path.dirname(__file__), "recipes.csv")

    def setUp(self):
        self.manager = RecipeManager()
        self.manager.load_csv(self.data_path)

    def test_load_csv(self):
        self.assertEqual(len(self.manager.recipes), 5)
        self.assertEqual(self.manager.recipes[0].name, "Chicken Salad")

    def test_search_methods(self):
        self.assertIsNotNone(self.manager.find_by_name("Pancakes"))
        mains = self.manager.search_by_category("main")
        self.assertEqual(len(mains), 2)
        chicken_matches = {r.name for r in self.manager.search_by_ingredient("chicken")}
        self.assertIn("Chicken Salad", chicken_matches)
        self.assertIn("Stir Fry Chicken", chicken_matches)

    def test_eval_expression(self):
        salad = self.manager.find_by_name("Chicken Salad")
        env = {
            "contains_chicken": any("chicken" in i.lower() for i in salad.ingredients),
            "cheap": salad.price < 4.0,
            "quick": salad.time_minutes <= 15,
            "healthy": salad.calories < 400,
        }
        self.assertTrue(eval_expr("(contains_chicken and quick) or healthy", env))

        pancakes = self.manager.find_by_name("Pancakes")
        env_pan = {
            "contains_chicken": any("chicken" in i.lower() for i in pancakes.ingredients),
            "cheap": pancakes.price < 4.0,
            "quick": pancakes.time_minutes <= 15,
            "healthy": pancakes.calories < 400,
        }
        self.assertFalse(eval_expr("(cheap or quick) and healthy", env_pan))

    def test_truth_table(self):
        vars_, rows = truth_table("A and B")
        expected = [([0, 0], 0), ([0, 1], 0), ([1, 0], 0), ([1, 1], 1)]
        self.assertEqual(vars_, ["A", "B"])
        self.assertEqual(rows, expected)

    def test_bubble_sort_by_time(self):
        sorter = BubbleSort()
        sorted_list = sorter.sort(self.manager.recipes, key_func=lambda r: r.time_minutes)
        times = [r.time_minutes for r in sorted_list]
        self.assertEqual(times, sorted(times))

    def test_merge_sort_matches_bubble(self):
        key = lambda r: r.price
        bubble = BubbleSort().sort(self.manager.recipes, key_func=key)
        merge = MergeSort().sort(self.manager.recipes, key_func=key)
        self.assertEqual([r.name for r in merge], [r.name for r in bubble])

    def test_secondary_key_sort(self):
        items = [
            Recipe("Healthy Tie", "main", 4.0, 30, ["veg"], ["cook"], 200, "Easy"),
            Recipe("Less Healthy", "main", 4.0, 30, ["veg"], ["cook"], 450, "Medium"),
            Recipe("Different Price", "main", 3.0, 25, ["veg"], ["cook"], 600, "Hard"),
        ]

        def key_func(r: Recipe):
            env = {
                "contains_chicken": any("chicken" in i.lower() for i in r.ingredients),
                "cheap": r.price < 4.0,
                "quick": r.time_minutes <= 15,
                "healthy": r.calories < 400,
            }
            secondary = 0 if eval_expr("healthy", env) else 1
            return (r.price, secondary)

        sorted_items = MergeSort().sort(items, key_func=key_func)
        self.assertEqual([r.name for r in sorted_items][:2], ["Different Price", "Healthy Tie"])


if __name__ == "__main__":
    unittest.main()
