# Recipe Selection System - Intelligent Console-Based Application

A comprehensive semester project implementing a console-based Recipe Selection System with advanced sorting algorithms, logical expression evaluation, and truth table analysis.

## Overview

This system demonstrates:
- **Object-Oriented Programming** with abstract classes and inheritance
- **Data Structures & Algorithms** with loop-based and recursion-based sorting
- **Logical Analysis** using truth tables and propositional logic
- **Performance Evaluation** comparing algorithm efficiency
- **Data Persistence** via CSV import/export

## Project Structure

\\\
RecipeSelectionSystem/
 main.py                      # Main console application
 test_demo.py                 # Comprehensive demo and tests
 recipes.csv                  # Sample recipe data
 recipe_system/
     __init__.py              # Package initialization
     recipe.py                # Recipe class definition
     manager.py               # RecipeManager class (load/save/search)
     sorting.py               # Abstract SortingAlgorithm + implementations
     logic.py                 # Logical expression evaluator & truth tables
\\\

## Key Features

### 1. Class Design (OOP)

**Recipe Class**
- Stores: name, category, price, time_minutes, ingredients, steps, calories, difficulty
- Methods: to_dict(), from_dict(), __str__()

**RecipeManager Class**
- load_csv(path) / save_csv(path)
- add_recipe(), delete_recipe(), find_by_name()
- search_by_category(), search_by_ingredient(), search_custom()

**SortingAlgorithm (Abstract)**
- BubbleSort: O(n) loop-based sorting
- MergeSort: O(n log n) recursion-based sorting

### 2. Logical Expression Evaluation

Supports complex boolean expressions:
- Variables: cheap, quick, healthy, contains_chicken
- Operators: and, or, not (, , )
- Full truth table generation

Example: \(cheap or quick) and healthy\

### 3. Data Management

CSV format with semicolon-separated lists:
\\\
name,category,price,time_minutes,ingredients,steps,calories,difficulty
Chicken Salad,main,5.5,15,chicken;lettuce;tomato,Chop;Mix;Serve,350,Easy
\\\

## Running the Application

### Interactive Menu
\\\ash
python main.py
\\\

### Run Tests and Demo
\\\ash
python test_demo.py
\\\

## Menu Options

1. View all recipes
2. View recipe details / Order
3. Add recipe
4. Edit recipe
5. Delete recipe
6. Search by name
7. Search by category
8. Search by ingredient
9. Logical search
10. Show truth table
11. Sort recipes
12. Performance test
13. Export CSV
0. Exit

## Example Workflows

### Find Quick & Cheap Meals
\\\
Menu: 9 (Logical search)
Expression: (cheap or quick) and healthy
Result: Recipes matching (price < 4 OR time <= 15) AND calories < 400
\\\

### Sort by Multiple Criteria
\\\
Menu: 11 (Sort recipes)
Primary key: price
Secondary: (quick or healthy)
Result: Sorted by price, cheap/healthy first
\\\

### Compare Algorithm Performance
\\\
Menu: 12 (Performance test)
Result: Shows timing for BubbleSort vs MergeSort
\\\

## Logical Variables

- \cheap\ - Price < \.00
- \quick\ - Cooking time  15 minutes
- \healthy\ - Calories < 400
- \contains_chicken\ - Contains \"chicken\" in ingredients

## Truth Table Example

For expression \A and B\:
\\\
A | B | Result
0 | 0 |   0
0 | 1 |   0
1 | 0 |   0
1 | 1 |   1
\\\

## Performance Analysis

**BubbleSort (Loop-based)**
- Time: O(n) best, O(n) avg/worst
- Space: O(1)

**MergeSort (Recursion-based)**
- Time: O(n log n) all cases
- Space: O(n)

Sample Results (5 recipes):
- Bubble: ~0.000001s
- Merge: ~0.000002s
- MergeSort dominates for n > 1000

## Sample Data

5 included recipes:
1. Chicken Salad (main) - \.50, 15 min, 350 cal
2. Pancakes (dessert) - \.00, 20 min, 450 cal
3. Tomato Soup (soup) - \.50, 25 min, 200 cal
4. Grilled Cheese (starter) - \.00, 10 min, 400 cal
5. Stir Fry Chicken (main) - \.00, 18 min, 500 cal

## Test Coverage

\	est_demo.py\ validates:
-  CSV loading
-  All search methods
-  Both sorting algorithms
-  Logical expression evaluation
-  Truth table generation
-  Secondary key sorting
-  Complex logical expressions

## Requirements

- Python 3.7+
- No external dependencies (stdlib only)

## Quick Start

\\\ash
# Test the system
python test_demo.py

# Run interactive app
python main.py
\\\

## Technical Architecture

**Sorting with Secondary Logic**
\\\python
def key_func(recipe):
    primary = recipe.price
    secondary = 0 if (recipe.price < 4 and recipe.time_minutes <= 15) else 1
    return (primary, secondary)

sorter = MergeSort()
sorted_recipes = sorter.sort(recipes, key_func=key_func)
\\\

**Logical Expression Parsing**
- Uses Python ast module for safe evaluation
- Supports: and, or, not with parentheses
- Validates against unsafe operations
- Converts symbols (, , ) to Python equivalents

**Truth Table Generation**
- Iterates 2^n combinations for n variables
- Evaluates expression for each state
- Returns: (variables, [(values, result), ...])

## Extensibility

Easy to extend:
- Add logical variables in main.py
- Implement new SortingAlgorithm subclasses
- Add search methods to RecipeManager
- Extend CSV with new fields

## Future Enhancements (Bonus)

- [ ] Rating/feedback system
- [ ] 7-day meal planning
- [ ] Ingredient availability checker
- [ ] Multi-file import
- [ ] GUI interface (Tkinter)
- [ ] Database storage (SQLite)

---

**Status**:  Complete - All core requirements implemented
**Last Updated**: January 2026
**Author**: Semester Project Group
