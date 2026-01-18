import csv
import os
from typing import List, Callable, Optional
from .recipe import Recipe

class RecipeManager:
    """Handles the collection of recipes, file I/O, and searching."""
    
    def __init__(self):
        self.recipes: List[Recipe] = []

    def load_csv(self, path: str):
        """Loads recipes from a CSV file with basic error handling."""
        if not os.path.exists(path):
            return
            
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.recipes = [Recipe.from_dict(row) for row in reader]

    def save_csv(self, path: str):
        """Saves current recipes to CSV, maintaining format integrity."""
        if not self.recipes:
            return
            
        fieldnames = ["name", "category", "price", "time_minutes", 
                      "ingredients", "steps", "calories", "difficulty"]
        
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in self.recipes:
                writer.writerow(r.to_dict())

    def add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)

    def delete_recipe(self, name: str) -> bool:
        """Removes a recipe by name. Returns True if found and deleted."""
        initial_len = len(self.recipes)
        self.recipes = [r for r in self.recipes if r.name.lower() != name.lower()]
        return len(self.recipes) < initial_len

    def find_by_name(self, name: str) -> Optional[Recipe]:
        """Case-insensitive exact name lookup."""
        return next((r for r in self.recipes if r.name.lower() == name.lower()), None)

    def search_by_category(self, category: str) -> List[Recipe]:
        return [r for r in self.recipes if r.category.lower() == category.lower()]

    def search_by_ingredient(self, ingredient: str) -> List[Recipe]:
        """Returns recipes where the ingredient is found within any item in the list."""
        ing = ingredient.lower()
        return [r for r in self.recipes if any(ing in i.lower() for i in r.ingredients)]

    def search_custom(self, predicate: Callable[[Recipe], bool]) -> List[Recipe]:
        """Advanced: Allows passing a logic function to filter recipes."""
        return list(filter(predicate, self.recipes))
