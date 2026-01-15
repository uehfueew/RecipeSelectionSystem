#!/usr/bin/env python3
"""
Visual demonstration guide for the Recipe Selection System GUI
Shows screenshots and usage examples
"""

GUI_FEATURES = """
╔════════════════════════════════════════════════════════════════════════════╗
║           RECIPE SELECTION SYSTEM - GUI APPLICATION (PyQt6)                ║
║                     Visual Demonstration Guide                             ║
╚════════════════════════════════════════════════════════════════════════════╝

LAUNCH COMMAND:
───────────────
    python gui_app.py

This will open a modern GUI window with 6 tabs for complete recipe management.

═══════════════════════════════════════════════════════════════════════════════

TAB 1: BROWSE RECIPES
─────────────────────
Features:
  ✓ View all recipes in a sortable table
  ✓ Columns: Name | Category | Price | Time | Ingredients | Steps | Calories | Difficulty
  ✓ Click any recipe to see full details in the panel below
  ✓ Detail panel shows: Full recipe info, ingredients list, cooking steps

Table Features:
  • Alternating row colors for better readability
  • Stretchable columns to fit content
  • Click row to highlight and view details
  • Ingredients/steps shown with semicolon separators

Example Display:
┌─────────────────┬──────────┬──────┬──────┬──────────────────┬────────┬──────┬──────────┐
│ Name            │ Category │ Price│ Time │ Ingredients      │ Steps  │ Cal  │ Diff     │
├─────────────────┼──────────┼──────┼──────┼──────────────────┼────────┼──────┼──────────┤
│ Grilled Cheese  │ starter  │$2.00 │ 10   │ bread; cheese;.. │ Assem..│ 400  │ Easy     │
│ Tomato Soup     │ soup     │$2.50 │ 25   │ tomato; onion;.. │ Boil;..│ 200  │ Easy     │
│ Pancakes        │ dessert  │$3.00 │ 20   │ flour; milk;..   │ Mix;.. │ 450  │ Medium   │
│ Chicken Salad   │ main     │$5.50 │ 15   │ chicken; lettuc..│ Chop;..│ 350  │ Easy     │
│ Stir Fry Chicken│ main     │$6.00 │ 18   │ chicken; soy ..  │ Stir;..│ 500  │ Medium   │
└─────────────────┴──────────┴──────┴──────┴──────────────────┴────────┴──────┴──────────┘

Detail Panel (Selected Recipe - Grilled Cheese):
┌──────────────────────────────────────────────────────────────────────────────┐
│ Grilled Cheese                                                               │
│ Category: starter                                                            │
│ Price: $2.00                                                                 │
│ Time: 10 minutes                                                             │
│ Calories: 400                                                                │
│ Difficulty: Easy                                                             │
│                                                                              │
│ Ingredients: bread, cheese, butter                                          │
│                                                                              │
│ Steps: Assemble, Grill, Serve                                              │
└──────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

TAB 2: SEARCH RECIPES
─────────────────────
Three independent search methods:

1. SEARCH BY NAME
   ┌─────────────────────────────────┐
   │ Search by Name:  [Tomato Soup   ] [Search]
   └─────────────────────────────────┘
   Result: Shows exact match if found

2. SEARCH BY CATEGORY
   ┌─────────────────────────────────┐
   │ Search by Category: [main       ] [Search]
   └─────────────────────────────────┘
   Result: Shows all "main" category recipes
   (Chicken Salad, Stir Fry Chicken)

3. SEARCH BY INGREDIENT
   ┌─────────────────────────────────┐
   │ Search by Ingredient: [chicken  ] [Search]
   └─────────────────────────────────┘
   Result: Shows all recipes containing "chicken"
   (Chicken Salad, Stir Fry Chicken)

Results Table: Same format as Browse tab

═══════════════════════════════════════════════════════════════════════════════

TAB 3: SORT RECIPES
───────────────────
Sorting Configuration:

Algorithm Selection:
   ┌──────────────────────────────────────┐
   │ Algorithm: [BubbleSort (O(n²))    ▼] │  Choose sorting algorithm
   │            [MergeSort (O(n log n))▼] │
   └──────────────────────────────────────┘

Primary Key Selection:
   ┌──────────────────────────────────────┐
   │ Primary Key: [Price              ▼] │  Choose: Price / Time / Calories
   │              [Time               ▼] │
   │              [Calories           ▼] │
   └──────────────────────────────────────┘

Sort Order:
   ┌──────────────────────────────────────┐
   │ Order: [Ascending                ▼] │  Choose: Ascending / Descending
   │        [Descending               ▼] │
   └──────────────────────────────────────┘

Secondary Logic (Optional):
   ┌──────────────────────────────────────┐
   │ Secondary: [(cheap and quick)       │  Add logical expression for ties
   └──────────────────────────────────────┘

Example Sort by Price (Ascending):
┌──────────────────────────┬────────┐
│ Grilled Cheese           │ $2.00  │
│ Tomato Soup              │ $2.50  │
│ Pancakes                 │ $3.00  │
│ Chicken Salad            │ $5.50  │
│ Stir Fry Chicken         │ $6.00  │
└──────────────────────────┴────────┘

Example Sort by Time (Ascending):
┌──────────────────────────┬────────┐
│ Grilled Cheese           │ 10 min │
│ Chicken Salad            │ 15 min │
│ Stir Fry Chicken         │ 18 min │
│ Pancakes                 │ 20 min │
│ Tomato Soup              │ 25 min │
└──────────────────────────┴────────┘

═══════════════════════════════════════════════════════════════════════════════

TAB 4: LOGIC (Logical Analysis)
───────────────────────────────
Two main features: Logical Search and Truth Tables

1. LOGICAL SEARCH
   ┌────────────────────────────────────────────────────────────────┐
   │ Logical Search                                                 │
   │ Variables: cheap, quick, healthy, contains_chicken             │
   │                                                                │
   │ Expression: [(cheap or quick) and healthy    ] [Search]        │
   └────────────────────────────────────────────────────────────────┘

   Predefined Variables:
   • cheap = price < $4.00
   • quick = time ≤ 15 minutes
   • healthy = calories < 400
   • contains_chicken = has "chicken" in ingredients

   Example Results for "(cheap or quick) and healthy":
   ┌─────────────────────┬────────┬──────┬──────────┐
   │ Tomato Soup         │ $2.50  │ 25m  │ 200 cal  │ ✓ (cheap AND healthy)
   │ Chicken Salad       │ $5.50  │ 15m  │ 350 cal  │ ✓ (quick AND healthy)
   └─────────────────────┴────────┴──────┴──────────┘

2. TRUTH TABLE GENERATOR
   ┌────────────────────────────────────────────────────┐
   │ Truth Table Generator                              │
   │ Expression: [A and B                    ] [Generate]
   └────────────────────────────────────────────────────┘

   Generated Output:
   ┌─────────────────────────────┐
   │   A   │   B   │   Result    │
   ├───────┼───────┼─────────────┤
   │   0   │   0   │      0      │
   │   0   │   1   │      0      │
   │   1   │   0   │      0      │
   │   1   │   1   │      1      │
   └─────────────────────────────┘

   Supports:
   • Multiple variables (generates 2^n rows)
   • Operators: and, or, not
   • Symbols: ∧, ∨, ¬
   • Parentheses for grouping

═══════════════════════════════════════════════════════════════════════════════

TAB 5: MANAGE (Recipe Management)
──────────────────────────────────
Recipe Operations:

Button Bar:
┌──────────┬──────────────┬──────────────┬────────────────┬──────────────┐
│ Add      │ Edit         │ Delete       │ Export to CSV  │ Reload from  │
│ Recipe   │ Selected     │ Selected     │                │ CSV          │
└──────────┴──────────────┴──────────────┴────────────────┴──────────────┘

Actions:

ADD RECIPE
  • Opens dialog with form fields
  • Input: Name, Category, Price, Time, Ingredients, Steps, Calories, Difficulty
  • Ingredients/Steps: semicolon-separated
  • Auto-adds to current recipe list

EDIT RECIPE
  • Select recipe from table
  • Click "Edit Selected"
  • Form pre-filled with recipe data
  • Modify and save changes

DELETE RECIPE
  • Select recipe from table
  • Click "Delete Selected"
  • Confirms deletion
  • Removes from list

EXPORT CSV
  • Saves all recipes to "exported_recipes.csv"
  • Maintains all fields and formatting
  • Can be imported in another session

RELOAD CSV
  • Reloads from original recipes.csv
  • Discards all unsaved changes
  • Refreshes all displays

Status Label: Shows last action feedback

═══════════════════════════════════════════════════════════════════════════════

TAB 6: PERFORMANCE (Algorithm Analysis)
────────────────────────────────────────
Algorithm Information Panel:
┌────────────────────────────────────────────────────────────────────────────┐
│ Algorithm Performance Comparison:                                           │
│                                                                            │
│ BubbleSort (Loop-based):                                                  │
│   • Time: O(n²) average case                                              │
│   • Space: O(1)                                                           │
│   • Best for: Small datasets                                              │
│                                                                            │
│ MergeSort (Recursion-based):                                              │
│   • Time: O(n log n) all cases                                            │
│   • Space: O(n)                                                           │
│   • Best for: Large datasets                                              │
└────────────────────────────────────────────────────────────────────────────┘

Test Configuration:
┌──────────────────────────────────────────┐
│ Dataset Size (multiplier): [3 ▲▼]        │  1-10x multiplication of recipes
│ [Run Performance Test]                   │
└──────────────────────────────────────────┘

Example Results:
┌────────────────────────────────────────────────────────────────────────────┐
│ Dataset size: 10                                                           │
│   BubbleSort (O(n²)): 0.000042s                                           │
│   MergeSort (O(n log n)): 0.000058s                                       │
│   Ratio (Bubble/Merge): 0.72x                                             │
│                                                                            │
│ Dataset size: 50                                                           │
│   BubbleSort (O(n²)): 0.000891s                                           │
│   MergeSort (O(n log n)): 0.000215s                                       │
│   Ratio (Bubble/Merge): 4.14x                                             │
│                                                                            │
│ Dataset size: 100                                                          │
│   BubbleSort (O(n²)): 0.003562s                                           │
│   MergeSort (O(n log n)): 0.000398s                                       │
│   Ratio (Bubble/Merge): 8.95x                                             │
└────────────────────────────────────────────────────────────────────────────┘

Key Insights:
  • For small datasets (n < 20): Both similar performance
  • For medium datasets (n = 20-100): MergeSort starts winning
  • For large datasets (n > 100): MergeSort dominates (can be 10-50x faster)
  • O(n log n) significantly beats O(n²) as n grows

═══════════════════════════════════════════════════════════════════════════════

GUI INTERFACE COMPONENTS
────────────────────────

Main Window:
  • Title: "Recipe Selection System - GUI"
  • Size: 1200x700 pixels
  • Tab-based navigation (6 tabs)
  • Responsive layout - resizes with window

Tables:
  • Custom RecipeTableWidget for consistent formatting
  • 8 columns: Name, Category, Price, Time, Ingredients, Steps, Calories, Difficulty
  • Alternating row colors for readability
  • Column auto-stretch for content fit
  • Row selection for operations

Text Inputs:
  • QLineEdit for single-line text (names, expressions)
  • QTextEdit for multi-line content (ingredients, steps)
  • QSpinBox for numeric values
  • QDoubleSpinBox for prices

Dropdowns (QComboBox):
  • Algorithm selection: BubbleSort vs MergeSort
  • Sort key: Price, Time, Calories
  • Sort order: Ascending, Descending
  • Difficulty: Easy, Medium, Hard

Dialogs:
  • AddRecipeDialog: Form for adding/editing recipes
  • Confirmation dialogs for delete operations
  • Error/info message boxes

Status Bar:
  • Shows last action feedback
  • Auto-clears after 3 seconds
  • Green checkmarks for success

═══════════════════════════════════════════════════════════════════════════════

WORKFLOW EXAMPLES
─────────────────

SCENARIO 1: Find Quick & Healthy Meals
  1. Go to "Logic" tab
  2. Enter: (quick and healthy)
  3. Click Search
  4. Result: Shows recipes with time ≤ 15 min AND calories < 400

SCENARIO 2: Compare Algorithms
  1. Go to "Sort" tab
  2. Select "BubbleSort (O(n²))" → Primary: Price → Click Sort
  3. Note execution time
  4. Select "MergeSort (O(n log n))" → Primary: Price → Click Sort
  5. Compare timing in status bar

SCENARIO 3: Create a Meal Plan
  1. Browse tab: View all recipes
  2. Search tab: Find recipes by ingredient (e.g., "chicken")
  3. Sort tab: Sort by price (ascending) to find cheapest options
  4. Manage tab: Add new recipes for variety

SCENARIO 4: Analyze Sorting Performance
  1. Go to "Performance" tab
  2. Set multiplier to 10 (creates 50 recipes)
  3. Click "Run Performance Test"
  4. View timing comparison and understand Big-O complexity

═══════════════════════════════════════════════════════════════════════════════

COLOR & STYLING
───────────────
  • Alternating row colors: White and light gray
  • Header: Bold, larger font (14pt)
  • Read-only text: Light background
  • Buttons: Standard system style
  • Selected rows: Highlighted in blue
  • Status messages: Temporary display

═══════════════════════════════════════════════════════════════════════════════

KEYBOARD SHORTCUTS
──────────────────
  • Tab key: Navigate between fields
  • Enter key: Confirm in dialogs
  • Escape key: Cancel dialogs
  • Click cells: Copy cell content (triple-click selects all)

═══════════════════════════════════════════════════════════════════════════════

DATA PERSISTENCE
─────────────────
  • Loads from: recipes.csv (at application start)
  • Can add/edit recipes in GUI
  • Export to: exported_recipes.csv (manual action)
  • Reload: Resets to original CSV file
  • All changes in-memory only (not auto-saved to CSV)

═══════════════════════════════════════════════════════════════════════════════

REQUIREMENTS
────────────
  • Python 3.7+
  • PyQt6
  • Standard library only for backend

Installation:
  pip install PyQt6

Running:
  python gui_app.py

═══════════════════════════════════════════════════════════════════════════════
"""

print(GUI_FEATURES)
