"""
Recipe Module
─────────────
This module defines the Recipe class, which represents a single recipe with all its details
like name, category, price, cooking time, ingredients, steps, calories, and difficulty level.

The Recipe class is used throughout the system to store and manage recipe information.
"""

from typing import List, Dict

class Recipe:
    """
    Represents a single recipe with all its nutritional and cooking details.
    
    Attributes:
        name (str): The name of the recipe (e.g., "Chicken Salad")
        category (str): The category (e.g., "main", "dessert", "soup", "starter")
        price (float): The cost to prepare the recipe in dollars
        time_minutes (int): How long it takes to cook in minutes
        ingredients (List[str]): List of ingredients needed for the recipe
        steps (List[str]): List of cooking instructions/steps
        calories (int): Nutritional information - total calories
        difficulty (str): Difficulty level (e.g., "Easy", "Medium", "Hard")
    """
    
    def __init__(self, name: str, category: str, price: float, time_minutes: int,
                 ingredients: List[str], steps: List[str], calories: int = 0, difficulty: str = ""):
        """
        Initialize a new Recipe object.
        
        Notes:
        - price and time_minutes are ensured to be non-negative (0 or greater)
        - calories is ensured to be non-negative
        """
        self.name = name
        self.category = category
        self.price = max(0.0, float(price))  # Ensure price is never negative
        self.time_minutes = max(0, int(time_minutes))  # Ensure time is never negative
        self.ingredients = ingredients
        self.steps = steps
        self.calories = max(0, int(calories))  # Ensure calories is never negative
        self.difficulty = difficulty

    def to_dict(self) -> Dict[str, str]:
        """
        Converts the Recipe object to a dictionary format for CSV exporting.
        
        This method transforms a Recipe object into a dictionary where:
        - Ingredients list is joined with ";" separator (e.g., "chicken;rice;oil")
        - Steps list is joined with ";" separator
        - Price is formatted to 2 decimal places (e.g., "3.99")
        
        Returns:
            A dictionary ready to be saved to CSV file
        """
        return {
            "name": self.name,
            "category": self.category,
            "price": f"{self.price:.2f}",
            "time_minutes": str(self.time_minutes),
            "ingredients": ";".join(self.ingredients),
            "steps": ";".join(self.steps),
            "calories": str(self.calories),
            "difficulty": self.difficulty,
        }

    @staticmethod
    def from_dict(d: Dict[str, str]) -> "Recipe":
        """
        Creates a Recipe object from a dictionary (used for CSV loading).
        
        This is the opposite of to_dict(). It takes a dictionary (usually from a CSV row)
        and converts it back into a Recipe object:
        - Splits ingredients string on ";" to create a list
        - Splits steps string on ";" to create a list
        - Converts numeric strings to appropriate types
        - Handles missing values with defaults
        
        Args:
            d: Dictionary containing recipe data from CSV
            
        Returns:
            A new Recipe object populated from the dictionary
        """
        # Split the ingredients string (separated by semicolons) into a list, removing extra spaces
        ingredients = [i.strip() for i in d.get("ingredients", "").split(";") if i.strip()]
        # Split the steps string (separated by semicolons) into a list, removing extra spaces
        steps = [s.strip() for s in d.get("steps", "").split(";") if s.strip()]
        
        return Recipe(
            name=d.get("name", "Unknown"),
            category=d.get("category", "General"),
            price=float(d.get("price", 0.0)),
            time_minutes=int(d.get("time_minutes", 0)),
            ingredients=ingredients,
            steps=steps,
            calories=int(d.get("calories", 0)),
            difficulty=d.get("difficulty", "Medium")
        )

    def __str__(self) -> str:
        """
        Returns a simple string representation of the recipe for printing.
        
        Example output: "Chicken Salad [main] - $5.50 (15 min)"
        """
        return f"{self.name} [{self.category}] - ${self.price:.2f} ({self.time_minutes} min)"

