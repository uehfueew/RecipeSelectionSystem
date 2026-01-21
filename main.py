"""
Recipe Selection System - Command Line Interface (CLI)
═══════════════════════════════════════════════════════

This is the main entry point for the recipe selection system. It provides a text-based
menu interface for users to interact with the recipe system.

Features:
- View all recipes
- Search recipes (by name, category, ingredient)
- Add/edit/delete recipes
- Sort recipes using different algorithms
- Use logical expressions to filter recipes
- Generate truth tables for boolean expressions
- Performance testing of sorting algorithms
- Export recipes to CSV

Run this file to start the application:
    python main.py
"""

import time
from recipe_system.manager import RecipeManager
from recipe_system.recipe import Recipe
from recipe_system.sorting import BubbleSort, MergeSort
from recipe_system.logic import eval_expr, truth_table
import os

# Path to the CSV file containing recipes
DATA_PATH = os.path.join(os.path.dirname(__file__), 'recipes.csv')


def input_list(prompt: str):
    """
    Helper function: Gets a list of items from user input.
    
    Items should be separated by semicolons (;)
    Extra spaces are automatically trimmed from each item
    
    Args:
        prompt: The question to ask the user
        
    Returns:
        A list of strings, one for each item entered
        
    Example:
        input_list('Ingredients') with input "chicken; rice; oil" returns
        ['chicken', 'rice', 'oil']
    """
    s = input(prompt + " (separate items with ;): ")
    return [i.strip() for i in s.split(';') if i.strip()]


def show_recipe_detail(r: Recipe):
    """
    Displays detailed information about a recipe.
    
    Shows:
    - Recipe name and category
    - Price and cooking time
    - Full list of ingredients
    - Numbered cooking steps
    - Calories and difficulty level
    
    Args:
        r: A Recipe object to display
    """
    print(f"Name: {r.name}")
    print(f"Category: {r.category}")
    print(f"Price: ${r.price:.2f}")
    print(f"Time: {r.time_minutes} minutes")
    print(f"Ingredients: {', '.join(r.ingredients)}")
    print("Steps:")
    for i, s in enumerate(r.steps, 1):
        print(f"  {i}. {s}")
    print(f"Calories: {r.calories} | Difficulty: {r.difficulty}")


def performance_test(manager: RecipeManager):
    """
    Runs a performance comparison test between Bubble Sort and Merge Sort.
    
    This function:
    1. Creates test datasets of sizes 10, 50, and 100 recipes
    2. Sorts each dataset with both Bubble Sort and Merge Sort
    3. Times each algorithm and displays the results
    4. Helps visualize the performance difference (Merge Sort is much faster!)
    
    Args:
        manager: The RecipeManager containing recipes to test
    """
    sizes = [10, 50, 100]
    print("Performance test (Bubble vs Merge):")
    for n in sizes:
        sample = (manager.recipes * ((n // max(1, len(manager.recipes))) + 1))[:n]
        b = BubbleSort()
        m = MergeSort()
        start = time.time()
        b.sort(sample, key_func=lambda r: r.time_minutes)
        t_b = time.time() - start
        start = time.time()
        m.sort(sample, key_func=lambda r: r.time_minutes)
        t_m = time.time() - start
        print(f"n={n}: Bubble {t_b:.6f}s, Merge {t_m:.6f}s")


def main():
    """
    Main menu loop for the Recipe Selection System.
    
    This function:
    1. Initializes the RecipeManager and loads recipes from CSV
    2. Displays a menu with 14 options
    3. Processes user choices in an infinite loop until user chooses 'Exit'
    
    Menu Options:
    1  - View all recipes (displays list of all loaded recipes)
    2  - View recipe details / Order (search by exact name and show full details)
    3  - Add recipe (create a new recipe by entering details)
    4  - Edit recipe (modify an existing recipe)
    5  - Delete recipe (remove a recipe from the system)
    6  - Search by name (find recipes with matching name)
    7  - Search by category (find recipes in a specific category)
    8  - Search by ingredient (find recipes containing an ingredient)
    9  - Logical search (use boolean expressions: "(contains_chicken and cheap) or quick")
    10 - Show truth table (display all combinations for a boolean expression)
    11 - Sort recipes (sort by price or time using Bubble/Merge sort)
    12 - Performance test (compare sorting algorithm speeds)
    13 - Export CSV (save current recipes to a CSV file)
    0  - Exit (quit the program)
    """
    manager = RecipeManager()
    
    # Try to load recipes from CSV file
    # First check the current working directory, then fall back to default location
    default_csv = os.path.join(os.getcwd(), 'recipes.csv')
    if os.path.exists(default_csv):
        path = default_csv
    else:
        path = DATA_PATH
    
    try:
        manager.load_csv(path)
        print(f"Loaded {len(manager.recipes)} recipes from {path}")
    except Exception as e:
        print("Could not load CSV:", e)

    while True:
        # Display the main menu
        print('\n--- Recipe Selection System ---')
        print('1) View all recipes')
        print('2) View recipe details / Order')
        print('3) Add recipe')
        print('4) Edit recipe')
        print('5) Delete recipe')
        print('6) Search by name')
        print('7) Search by category')
        print('8) Search by ingredient')
        print('9) Logical search')
        print('10) Show truth table for expression')
        print('11) Sort recipes')
        print('12) Performance test')
        print('13) Export CSV')
        print('0) Exit')
        choice = input('Choose an option: ').strip()

        # OPTION 1: View all recipes
        if choice == '1':
            if manager.recipes:
                for i, r in enumerate(manager.recipes, 1):
                    print(f"{i}. {r}")
            else:
                print("No recipes loaded.")

        # OPTION 2: View recipe details by name
        elif choice == '2':
            name = input('Recipe name: ')
            r = manager.find_by_name(name)
            if r:
                show_recipe_detail(r)
            else:
                print('Not found')

        # OPTION 3: Add a new recipe
        elif choice == '3':
            name = input('Name: ')
            category = input('Category: ')
            price = float(input('Price: '))
            time_m = int(input('Time minutes: '))
            ingredients = input_list('Ingredients')
            steps = input_list('Steps')
            calories = int(input('Calories (0 if unknown): '))
            diff = input('Difficulty: ')
            img_url = input('Image URL (optional): ')
            manager.add_recipe(Recipe(name, category, price, time_m, ingredients, steps, calories, diff, img_url))
            print('Added')

        # OPTION 4: Edit an existing recipe
        elif choice == '4':
            name = input('Recipe name to edit: ')
            r = manager.find_by_name(name)
            if not r:
                print('Not found')
                continue
            # Show current values and allow user to modify them
            print('Leave blank to keep current value')
            new_name = input(f'Name [{r.name}]: ') or r.name
            new_cat = input(f'Category [{r.category}]: ') or r.category
            new_price = input(f'Price [{r.price}]: ')
            new_time = input(f'Time minutes [{r.time_minutes}]: ')
            new_ings = input(f'Ingredients (;) [{";".join(r.ingredients)}]: ')
            new_steps = input(f'Steps (;) [{";".join(r.steps)}]: ')
            new_cal = input(f'Calories [{r.calories}]: ')
            new_diff = input(f'Difficulty [{r.difficulty}]: ') or r.difficulty
            new_img = input(f'Image URL [{getattr(r, "image_url", "")}]: ') or getattr(r, "image_url", "")
            
            # Update the recipe object with new values
            r.name = new_name
            r.category = new_cat
            if new_price: r.price = float(new_price)
            if new_time: r.time_minutes = int(new_time)
            if new_ings: r.ingredients = [i.strip() for i in new_ings.split(';') if i.strip()]
            if new_steps: r.steps = [s.strip() for s in new_steps.split(';') if s.strip()]
            if new_cal: r.calories = int(new_cal)
            r.difficulty = new_diff
            r.image_url = new_img
            print('Updated')

        # OPTION 5: Delete a recipe
        elif choice == '5':
            name = input('Recipe name to delete: ')
            ok = manager.delete_recipe(name)
            print('Deleted' if ok else 'Not found')

        # OPTION 6: Search by recipe name (exact match)
        elif choice == '6':
            name = input('Name to search: ')
            r = manager.find_by_name(name)
            if r: 
                print(r)
            else: 
                print('Not found')

        # OPTION 7: Search recipes by category
        elif choice == '7':
            cat = input('Category: ')
            res = manager.search_by_category(cat)
            if res:
                for r in res: 
                    print(r)
            else:
                print('No recipes in that category')

        # OPTION 8: Search recipes by ingredient
        elif choice == '8':
            ing = input('Ingredient: ')
            res = manager.search_by_ingredient(ing)
            if res:
                for r in res: 
                    print(r)
            else:
                print('No recipes with that ingredient')

        # OPTION 9: Logical search using boolean expressions
        elif choice == '9':
            expr = input('Enter logical expression (e.g. "(contains_chicken and cheap) or quick"): ')
            matched = []
            for r in manager.recipes:
                # Create environment with custom boolean variables for this recipe
                env = {
                    'contains_chicken': any('chicken' in i.lower() for i in r.ingredients),
                    'cheap': r.price < 4.0,
                    'quick': r.time_minutes <= 15,
                    'healthy': r.calories < 400,
                }
                try:
                    if eval_expr(expr, env):
                        matched.append(r)
                except Exception as e:
                    print('Error evaluating expression:', e)
                    matched = []
                    break
            # Display matching recipes
            if matched:
                for r in matched:
                    print(r)
            else:
                print('No recipes matched the expression')

        # OPTION 10: Show truth table for a boolean expression
        elif choice == '10':
            expr = input('Expression for truth table (use variable names): ')
            try:
                vars_, rows = truth_table(expr)
                # Print header row
                print(' | '.join(vars_) + ' | Result')
                # Print data rows
                for vals, res in rows:
                    print(' | '.join(str(v) for v in vals) + ' | ' + str(res))
            except Exception as e:
                print('Error:', e)

        # OPTION 11: Sort recipes
        elif choice == '11':
            # Get sorting preferences from user
            alg = input('Algorithm (bubble/merge): ').strip().lower()
            key = input('Primary key (price/time): ').strip().lower()
            expr = input('Optional logical expression for secondary key (leave blank to skip): ').strip()
            
            # Choose sorting algorithm
            sorter = BubbleSort() if alg == 'bubble' else MergeSort()
            
            # Define the key function for sorting
            def keyfunc(r):
                # Primary sort key (price or time)
                primary = r.price if key == 'price' else r.time_minutes
                # Optional secondary sort key using boolean expression
                secondary = 0
                if expr:
                    env = {
                        'contains_chicken': any('chicken' in i.lower() for i in r.ingredients),
                        'cheap': r.price < 4.0,
                        'quick': r.time_minutes <= 15,
                        'healthy': r.calories < 400,
                    }
                    try:
                        secondary = 0 if eval_expr(expr, env) else 1
                    except Exception:
                        secondary = 1
                return (primary, secondary)
            
            # Sort the recipes and update the manager
            sorted_list = sorter.sort(manager.recipes, key_func=keyfunc)
            manager.recipes = sorted_list
            print('Sorted')

        # OPTION 12: Performance test
        elif choice == '12':
            performance_test(manager)

        # OPTION 13: Export recipes to CSV
        elif choice == '13':
            path = input('Export path (filename.csv): ').strip()
            if not path:
                path = 'exported_recipes.csv'
            manager.save_csv(path)
            print('Saved to', path)

        # OPTION 0: Exit the program
        elif choice == '0':
            print("Goodbye!")
            break
        
        # Unknown option
        else:
            print('Unknown option')

if __name__ == '__main__':
    # This line ensures main() only runs when this file is executed directly,
    # not when it's imported as a module in another file
    main()
