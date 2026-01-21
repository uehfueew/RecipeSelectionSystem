from typing import List, Dict

class Recipe:
    """Represents a single recipe with all its nutritional and cooking details."""
    
    def __init__(self, name: str, category: str, price: float, time_minutes: int,
                 ingredients: List[str], steps: List[str], calories: int = 0, difficulty: str = ""):
        self.name = name
        self.category = category
        self.price = max(0.0, float(price))
        self.time_minutes = max(0, int(time_minutes))
        self.ingredients = ingredients
        self.steps = steps
        self.calories = max(0, int(calories))
        self.difficulty = difficulty

    def to_dict(self) -> Dict[str, str]:
        
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
    
    #“I have recipe data stored as a dictionary (for example from a CSV file).
    #How do I turn that dictionary into a Recipe object?”
    @staticmethod
    
    def from_dict(d: Dict[str, str]) -> "Recipe": #“This method belongs to the Recipe class,but it does NOT belong to a specific recipe object.”
        #The class is still being defined
        #Python hasn’t fully created Recipe yet
        #This is called a forward reference.
        """Creates a Recipe object from a dictionary (used for CSV loading)."""
        ingredients = [i.strip() for i in d.get("ingredients", "").split(";") if i.strip()]
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
        return f"{self.name} [{self.category}] - ${self.price:.2f} ({self.time_minutes} min)"

