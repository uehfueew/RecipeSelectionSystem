"""
Recipe Manager Module
─────────────────────
This module provides the RecipeManager class, which handles the collection of recipes
and provides functionality for searching, loading/saving recipes from/to CSV files.

The RecipeManager is the main interface for managing recipe data in this system.
"""

import pandas as pd
import os
from typing import List, Callable, Optional
from .recipe import Recipe

class RecipeManager:
    """
    Manages the collection of recipes and provides search/filter functionality.
    
    This class acts as the main controller for recipe data:
    - Stores all recipes in a list
    - Loads recipes from CSV files (using Pandas for efficient data handling)
    - Saves recipes to CSV files
    - Provides multiple search methods (by name, category, ingredient)
    - Allows adding, deleting, and finding recipes
    """
    
    def __init__(self):
        """Initialize an empty recipe manager (no recipes loaded yet)."""
        self.recipes: List[Recipe] = []

    def load_csv(self, path: str):
        """
        Loads recipes from a CSV file using Pandas for efficient data handling.
        
        How it works:
        1. Checks if the file exists at the given path
        2. Uses Pandas to read the CSV file
        3. Replaces any empty cells (NaN values) with empty strings
        4. Converts each CSV row into a Recipe object
        5. Stores all recipes in self.recipes list
        
        Args:
            path: Full file path to the CSV file containing recipes
            
        Example CSV format:
            name,category,price,time_minutes,ingredients,steps,calories,difficulty
            Chicken Salad,main,5.50,15,chicken;lettuce;dressing,Combine,350,Easy
        """
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
        """
        Saves all current recipes to a CSV file using Pandas.
        
        How it works:
        1. Converts each Recipe object to a dictionary using Recipe.to_dict()
        2. Creates a Pandas DataFrame from the list of dictionaries
        3. Writes the DataFrame to a CSV file
        
        Args:
            path: Full file path where the CSV file should be saved
            
        Note: If there are no recipes, the function returns early without creating a file.
        """
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
        """
        Adds a new recipe to the collection.
        
        Args:
            recipe: A Recipe object to add
        """
        self.recipes.append(recipe)

    def delete_recipe(self, name: str) -> bool:
        """
        Removes a recipe from the collection by its name (case-insensitive).
        
        Args:
            name: The name of the recipe to delete
            
        Returns:
            True if a recipe was found and deleted, False if no recipe with that name exists
        """
        initial_len = len(self.recipes)
        self.recipes = [r for r in self.recipes if r.name.lower() != name.lower()]
        return len(self.recipes) < initial_len

    def find_by_name(self, name: str) -> Optional[Recipe]:
        """
        Finds a single recipe by exact name (case-insensitive).
        
        Args:
            name: The exact name of the recipe to find
            
        Returns:
            The Recipe object if found, None otherwise
            
        Example: find_by_name("Chicken Salad") returns the Chicken Salad recipe or None
        """
        return next((r for r in self.recipes if r.name.lower() == name.lower()), None)

    def search_by_name(self, name: str) -> List[Recipe]:
        """
        Finds all recipes with names containing the search term (case-insensitive, partial match).
        
        Args:
            name: The partial name to search for
            
        Returns:
            A list of Recipe objects that contain the search term in their name
            
        Example: search_by_name("Salad") returns all recipes with "salad" in the name
        """
        return [r for r in self.recipes if name.lower() in r.name.lower()]

    def search_by_category(self, category: str) -> List[Recipe]:
        """
        Finds all recipes in a specific category (case-insensitive, exact match).
        
        Args:
            category: The category to search for (e.g., "main", "dessert", "soup")
            
        Returns:
            A list of Recipe objects in the specified category
            
        Example: search_by_category("main") returns all main course recipes
        """
        return [r for r in self.recipes if r.category.lower() == category.lower()]

    def search_by_ingredient(self, ingredient: str) -> List[Recipe]:
        """
        Finds all recipes that contain a specific ingredient (case-insensitive, partial match).
        
        How it works:
        - For each recipe, it checks if the ingredient appears in ANY of the recipe's ingredients
        - The search is partial and case-insensitive
        
        Args:
            ingredient: The ingredient to search for
            
        Returns:
            A list of Recipe objects that contain the specified ingredient
            
        Example: search_by_ingredient("chicken") returns all recipes with chicken
        """
        ing = ingredient.lower()
        return [r for r in self.recipes if any(ing in i.lower() for i in r.ingredients)]

    def search_custom(self, predicate: Callable[[Recipe], bool]) -> List[Recipe]:
        """
        Advanced search using a custom filter function (for expert users).
        
        This is a flexible method that allows you to write custom logic for filtering recipes.
        
        Args:
            predicate: A function that takes a Recipe and returns True/False
            
        Returns:
            A list of Recipe objects where predicate(recipe) returns True
            
        Example: search_custom(lambda r: r.price < 5.0 and r.time_minutes <= 15)
                 returns all recipes under $5 that take 15 minutes or less
        """
        return list(filter(predicate, self.recipes))
