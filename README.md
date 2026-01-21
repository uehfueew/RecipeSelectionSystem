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

```
RecipeSelectionSystem/
├── main.py                          # ⭐ Entry point - Console-based CLI application
├── gui_app.py                       # 🎨 PyQt6 graphical user interface
├── GUI_VISUAL_GUIDE.py              # 📖 Documentation for GUI features
├── test_demo.py                     # ✅ Unit tests and test cases (7 tests)
├── recipes.csv                      # 📊 Sample recipe data (5 recipes)
│
├── recipe_system/                   # 📦 Core system package
│   ├── __init__.py                  # Package initialization & imports
│   ├── recipe.py                    # 📋 Recipe class (data structure)
│   │   └── Stores: name, category, price, time, ingredients, steps, calories, difficulty
│   │   └── Methods: to_dict(), from_dict(), __str__()
│   │
│   ├── manager.py                   # 🔧 RecipeManager class (main controller)
│   │   └── Load/Save recipes from/to CSV
│   │   └── Search by: name, category, ingredient
│   │   └── Add, delete, and manage recipes
│   │
│   ├── sorting.py                   # 🔀 Sorting algorithms
│   │   ├── SortingAlgorithm (abstract base class)
│   │   ├── BubbleSort (O(n²) - loop-based)
│   │   └── MergeSort (O(n log n) - recursion-based)
│   │
│   └── logic.py                     # 🧠 Boolean logic evaluator
│       ├── eval_expr() - Evaluate boolean expressions safely
│       ├── truth_table() - Generate truth tables
│       ├── parse_vars() - Extract variables from expressions
│       └── Supports: AND, OR, NOT operators & parentheses
│
├── README.md                        # 📚 Project documentation
├── COMMENTS_GUIDE.md                # 🎓 Beginner-friendly learning guide
└── COMMENTS_COMPLETE.txt            # ✨ Summary of all comments added
```

### 📁 File Descriptions

**Root Level Files**
| File | Purpose | Type |
|------|---------|------|
| `main.py` | Interactive menu-driven CLI | Executable |
| `gui_app.py` | PyQt6 graphical interface | Executable |
| `test_demo.py` | 7 automated unit tests | Test Suite |
| `recipes.csv` | 5 sample recipes | Data |

**Core Package: `recipe_system/`**
| Module | Classes/Functions | Purpose |
|--------|-------------------|---------|
| `recipe.py` | `Recipe` class | Data structure for single recipe |
| `manager.py` | `RecipeManager` class | Collection management & search |
| `sorting.py` | `BubbleSort`, `MergeSort` | Algorithm implementations |
| `logic.py` | `eval_expr()`, `truth_table()` | Boolean expression handling |\

## Key Features

### 1. 📋 Class Design (OOP)

#### Recipe Class (`recipe_system/recipe.py`)
The fundamental data structure representing a single recipe.

**Attributes:**
- `name` - Recipe name (string)
- `category` - Type of dish (main, dessert, soup, starter)
- `price` - Cost in dollars (float, auto-validated ≥ 0)
- `time_minutes` - Cooking time (int, auto-validated ≥ 0)
- `ingredients` - List of items needed (list of strings)
- `steps` - Cooking instructions (list of strings)
- `calories` - Nutritional info (int, auto-validated ≥ 0)
- `difficulty` - Skill level (Easy, Medium, Hard)

**Methods:**
- `to_dict()` - Convert to dictionary for CSV export
- `from_dict(d)` - Static method to create Recipe from dictionary (CSV import)
- `__str__()` - Human-readable representation

---

#### RecipeManager Class (`recipe_system/manager.py`)
Central controller managing the collection of recipes.

**Data Management:**
- `load_csv(path)` - Load recipes from CSV file using Pandas
- `save_csv(path)` - Save recipes to CSV file using Pandas
- `add_recipe(recipe)` - Add new recipe to collection
- `delete_recipe(name)` - Remove recipe by name (case-insensitive)

**Search Methods:**
- `find_by_name(name)` - Exact name lookup (case-insensitive)
- `search_by_name(name)` - Partial name search
- `search_by_category(category)` - Filter by category
- `search_by_ingredient(ingredient)` - Find recipes containing ingredient
- `search_custom(predicate)` - Advanced filtering with custom logic

---

#### Sorting Algorithm Classes (`recipe_system/sorting.py`)

**SortingAlgorithm (Abstract Base Class)**
- Defines interface all sorting algorithms must implement
- Ensures consistent method signatures

**BubbleSort Implementation**
- Time Complexity: O(n²) best/average/worst
- Space Complexity: O(1)
- Algorithm: Compare adjacent elements, swap if needed, repeat
- Best for: Learning and small datasets
- Code type: Loop-based iterative approach

**MergeSort Implementation**
- Time Complexity: O(n log n) all cases (guaranteed)
- Space Complexity: O(n)
- Algorithm: Divide list in half recursively, merge sorted halves
- Best for: Large datasets (n > 1000)
- Code type: Recursion-based divide-and-conquer

---

#### Logic Evaluator (`recipe_system/logic.py`)
Safe evaluation of boolean expressions for complex filtering.

**Functions:**
- `eval_expr(expr, env)` - Evaluate expression with variable values
- `truth_table(expr)` - Generate all True/False combinations (2^n rows)
- `parse_vars(expr)` - Extract variable names from expression

**Supported Operations:**
- `AND` / `and` / `∧` - Both values must be True
- `OR` / `or` / `∨` - At least one value must be True
- `NOT` / `not` / `¬` - Negate the value
- Parentheses for grouping expressions

### 2. 🎯 Application Entry Points

**CLI Version (`main.py`)**
- 13 interactive menu options
- Text-based user interface
- Supports all features: search, sort, logical filtering
- Run: `python main.py`

**GUI Version (`gui_app.py`)**
- 6-tab PyQt6 interface
- Visual recipe browser
- Dark theme "Cyber Chef" styling
- Advanced search and sorting
- Run: `python gui_app.py`

---

## 🏗️ Architecture & Component Interaction

### Data Flow Diagram

```
CSV File (recipes.csv)
    ↓
RecipeManager.load_csv() → [Recipe objects in memory]
    ↓
User Interface (CLI or GUI)
    ├→ Display recipes
    ├→ Search recipes
    │   ├→ Search by name/category/ingredient (manager.py)
    │   └→ Logical search using eval_expr() (logic.py)
    ├→ Sort recipes
    │   ├→ BubbleSort or MergeSort (sorting.py)
    │   └→ Primary + secondary sort keys
    └→ Add/Edit/Delete recipes
    ↓
RecipeManager.save_csv() → Updated CSV File
```

### Module Dependencies

```
main.py / gui_app.py (User Interface)
    ↓
recipe_system.manager (RecipeManager)
    ├→ recipe_system.recipe (Recipe class)
    ├→ recipe_system.sorting (BubbleSort, MergeSort)
    ├→ recipe_system.logic (eval_expr, truth_table)
    └→ pandas (CSV handling)
```

### How Components Work Together

**Example: Search for cheap & quick meals**
1. User enters: `(cheap or quick) and healthy`
2. `main.py` → calls `manager.search_custom(predicate)`
3. For each recipe, create environment dict with:
   - `cheap` = price < 4.0
   - `quick` = time ≤ 15 minutes
   - `healthy` = calories < 400
4. `logic.eval_expr()` → evaluates expression for each recipe
5. Returns matching recipes
6. Display results to user

**Example: Sort by price, then by health**
1. User selects: Primary=price, Secondary=healthy
2. Define key function:
   ```python
   def key_func(recipe):
       primary = recipe.price
       secondary = 0 if healthy else 1
       return (primary, secondary)
   ```
3. Choose sorting algorithm (BubbleSort or MergeSort)
4. `sorter.sort(recipes, key_func=key_func)`
5. Returns sorted recipes (cheap first, then healthy)

---

## 📂 Directory Layout Summary

| Directory | Contents | Purpose |
|-----------|----------|---------|
| Root | `main.py`, `gui_app.py`, `test_demo.py`, `README.md` | Entry points & documentation |
| `recipe_system/` | `recipe.py`, `manager.py`, `sorting.py`, `logic.py` | Core business logic |
| Root | `recipes.csv` | Sample data |
| Root | `COMMENTS_GUIDE.md`, `COMMENTS_COMPLETE.txt` | Learning resources |

---

## 🔄 Data Format: CSV Structure

All recipes stored in comma-separated format with semicolon-separated lists:

```csv
name,category,price,time_minutes,ingredients,steps,calories,difficulty
Chicken Salad,main,5.5,15,chicken;lettuce;tomato;dressing,Chop;Mix;Serve,350,Easy
Pancakes,dessert,3.0,20,flour;milk;eggs;butter,Mix;Cook;Plate,450,Medium
Tomato Soup,soup,2.5,25,tomato;onion;broth;cream,Sauté;Simmer;Blend,200,Easy
Grilled Cheese,starter,2.0,10,bread;cheese;butter,Assemble;Grill;Serve,400,Easy
Stir Fry Chicken,main,6.0,18,chicken;soy;vegetables;oil,Prepare;Stir;Serve,500,Medium
```

**Format Rules:**
- Ingredients separated by `;` (no spaces)
- Steps separated by `;` (no spaces)
- Fields must match column headers exactly
- All numeric values must be valid
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
