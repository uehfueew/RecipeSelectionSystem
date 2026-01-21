import pandas as pd
import os
from typing import List, Callable, Optional
from .recipe import Recipe

class RecipeManager:
    """Handles the collection of recipes, file I/O, and searching using Pandas."""
    
    def __init__(self):
        self.recipes: List[Recipe] = []

    def load_csv(self, path: str):
        """Loads recipes from a CSV file using Pandas for data handling."""
        if not os.path.exists(path):
            return
            
        try:
            # Use Pandas to read the CSV
            df = pd.read_csv(path)
            # Ensure any NaN values are handled (converted to empty strings)
            df = df.fillna("")
            # Convert DataFrame to a list of dictionaries and then to Recipe objects
            records = df.to_dict('records')
            self.recipes = [Recipe.from_dict(row) for row in records]
        except Exception as e:
            print(f"Error loading CSV with Pandas: {e}")

    def save_csv(self, path: str):
        """Saves current recipes to CSV using Pandas DataFrame functionality."""
        """It takes the Recipe objects, converts them into DataFrames, and then saves them as a CSV file."""
        if not self.recipes:
            return
            
        try:
            # Convert list of Recipe objects to a list of dictionaries
            data = [r.to_dict() for r in self.recipes]
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)
            # Save to CSV using Pandas
            df.to_csv(path, index=False, encoding='utf-8')
        except Exception as e:
            print(f"Error saving CSV with Pandas: {e}")

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
