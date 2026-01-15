#!/usr/bin/env python3
"""
Recipe Selection System - PyQt6 GUI Application
Provides a visual interface for recipe management, sorting, searching, and logical analysis
"""

import sys
import time
from typing import List
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QMessageBox, QDialog,
    QFormLayout, QDialogButtonBox, QHeaderView, QListWidget, QListWidgetItem,
    QSplitter, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QIcon

from recipe_system.manager import RecipeManager
from recipe_system.recipe import Recipe
from recipe_system.sorting import BubbleSort, MergeSort
from recipe_system.logic import eval_expr, truth_table, LogicEvalError
import os


class RecipeTableWidget(QTableWidget):
    """Custom table widget for displaying recipes"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(8)
        self.setHorizontalHeaderLabels([
            "Name", "Category", "Price", "Time (min)", "Ingredients", "Steps", "Calories", "Difficulty"
        ])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)

    def load_recipes(self, recipes: List[Recipe]):
        """Load recipes into the table"""
        self.setRowCount(len(recipes))
        for row, recipe in enumerate(recipes):
            self.setItem(row, 0, QTableWidgetItem(recipe.name))
            self.setItem(row, 1, QTableWidgetItem(recipe.category))
            self.setItem(row, 2, QTableWidgetItem(f"${recipe.price:.2f}"))
            self.setItem(row, 3, QTableWidgetItem(str(recipe.time_minutes)))
            self.setItem(row, 4, QTableWidgetItem("; ".join(recipe.ingredients)))
            self.setItem(row, 5, QTableWidgetItem("; ".join(recipe.steps)))
            self.setItem(row, 6, QTableWidgetItem(str(recipe.calories)))
            self.setItem(row, 7, QTableWidgetItem(recipe.difficulty))


class AddRecipeDialog(QDialog):
    """Dialog for adding/editing recipes"""
    def __init__(self, parent=None, recipe=None):
        super().__init__(parent)
        self.recipe = recipe
        self.init_ui()
        if recipe:
            self.load_recipe()

    def init_ui(self):
        self.setWindowTitle("Add/Edit Recipe")
        self.setGeometry(100, 100, 400, 300)
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.category_input = QLineEdit()
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 100)
        self.time_input = QSpinBox()
        self.time_input.setRange(0, 1000)
        self.ingredients_input = QTextEdit()
        self.steps_input = QTextEdit()
        self.calories_input = QSpinBox()
        self.calories_input.setRange(0, 5000)
        self.difficulty_input = QComboBox()
        self.difficulty_input.addItems(["Easy", "Medium", "Hard"])

        layout.addRow("Name:", self.name_input)
        layout.addRow("Category:", self.category_input)
        layout.addRow("Price:", self.price_input)
        layout.addRow("Time (minutes):", self.time_input)
        layout.addRow("Ingredients (semicolon-separated):", self.ingredients_input)
        layout.addRow("Steps (semicolon-separated):", self.steps_input)
        layout.addRow("Calories:", self.calories_input)
        layout.addRow("Difficulty:", self.difficulty_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        self.setLayout(layout)

    def load_recipe(self):
        """Load recipe data into form"""
        if self.recipe:
            self.name_input.setText(self.recipe.name)
            self.category_input.setText(self.recipe.category)
            self.price_input.setValue(self.recipe.price)
            self.time_input.setValue(self.recipe.time_minutes)
            self.ingredients_input.setText("; ".join(self.recipe.ingredients))
            self.steps_input.setText("; ".join(self.recipe.steps))
            self.calories_input.setValue(self.recipe.calories)
            self.difficulty_input.setCurrentText(self.recipe.difficulty)

    def get_recipe(self):
        """Get recipe data from form"""
        ingredients = [i.strip() for i in self.ingredients_input.toPlainText().split(";") if i.strip()]
        steps = [s.strip() for s in self.steps_input.toPlainText().split(";") if s.strip()]
        return Recipe(
            name=self.name_input.text(),
            category=self.category_input.text(),
            price=self.price_input.value(),
            time_minutes=self.time_input.value(),
            ingredients=ingredients,
            steps=steps,
            calories=self.calories_input.value(),
            difficulty=self.difficulty_input.currentText()
        )


class RecipeGUI(QMainWindow):
    """Main GUI application"""
    def __init__(self):
        super().__init__()
        self.manager = RecipeManager()
        self.current_recipes = []
        self.init_ui()
        self.load_data()

    def init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle("Recipe Selection System - GUI")
        self.setGeometry(50, 50, 1200, 700)

        # Create tab widget
        tabs = QTabWidget()
        tabs.addTab(self.create_browse_tab(), "Browse")
        tabs.addTab(self.create_search_tab(), "Search")
        tabs.addTab(self.create_sort_tab(), "Sort")
        tabs.addTab(self.create_logic_tab(), "Logic")
        tabs.addTab(self.create_manage_tab(), "Manage")
        tabs.addTab(self.create_performance_tab(), "Performance")

        self.setCentralWidget(tabs)

    def create_browse_tab(self):
        """Create recipe browsing tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("All Recipes")
        title_font = title.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Recipe table
        self.recipe_table = RecipeTableWidget()
        layout.addWidget(self.recipe_table)

        # Detail view
        detail_layout = QHBoxLayout()
        detail_layout.addWidget(QLabel("Recipe Details:"))
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setMaximumHeight(150)
        detail_layout.addWidget(self.detail_text)
        layout.addLayout(detail_layout)

        # Connect selection
        self.recipe_table.selectionModel().selectionChanged.connect(self.on_recipe_selected)

        widget.setLayout(layout)
        return widget

    def create_search_tab(self):
        """Create search tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Search Recipes")
        title_font = title.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Search options
        search_layout = QGridLayout()
        search_layout.addWidget(QLabel("Search by Name:"), 0, 0)
        self.search_name_input = QLineEdit()
        search_layout.addWidget(self.search_name_input, 0, 1)
        search_by_name_btn = QPushButton("Search")
        search_by_name_btn.clicked.connect(self.search_by_name)
        search_layout.addWidget(search_by_name_btn, 0, 2)

        search_layout.addWidget(QLabel("Search by Category:"), 1, 0)
        self.search_category_input = QLineEdit()
        search_layout.addWidget(self.search_category_input, 1, 1)
        search_by_cat_btn = QPushButton("Search")
        search_by_cat_btn.clicked.connect(self.search_by_category)
        search_layout.addWidget(search_by_cat_btn, 1, 2)

        search_layout.addWidget(QLabel("Search by Ingredient:"), 2, 0)
        self.search_ingredient_input = QLineEdit()
        search_layout.addWidget(self.search_ingredient_input, 2, 1)
        search_by_ing_btn = QPushButton("Search")
        search_by_ing_btn.clicked.connect(self.search_by_ingredient)
        search_layout.addWidget(search_by_ing_btn, 2, 2)

        layout.addLayout(search_layout)

        # Results
        layout.addWidget(QLabel("Results:"))
        self.search_results_table = RecipeTableWidget()
        layout.addWidget(self.search_results_table)

        widget.setLayout(layout)
        return widget

    def create_sort_tab(self):
        """Create sorting tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Sort Recipes")
        title_font = title.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Sort options
        sort_layout = QGridLayout()
        sort_layout.addWidget(QLabel("Algorithm:"), 0, 0)
        self.sort_algo = QComboBox()
        self.sort_algo.addItems(["BubbleSort (O(n²))", "MergeSort (O(n log n))"])
        sort_layout.addWidget(self.sort_algo, 0, 1)

        sort_layout.addWidget(QLabel("Primary Key:"), 1, 0)
        self.sort_key = QComboBox()
        self.sort_key.addItems(["Price", "Time", "Calories"])
        sort_layout.addWidget(self.sort_key, 1, 1)

        sort_layout.addWidget(QLabel("Order:"), 2, 0)
        self.sort_order = QComboBox()
        self.sort_order.addItems(["Ascending", "Descending"])
        sort_layout.addWidget(self.sort_order, 2, 1)

        sort_layout.addWidget(QLabel("Secondary Logic (optional):"), 3, 0)
        self.sort_logic_input = QLineEdit()
        self.sort_logic_input.setPlaceholderText("e.g., (cheap and quick)")
        sort_layout.addWidget(self.sort_logic_input, 3, 1)

        sort_btn = QPushButton("Sort")
        sort_btn.clicked.connect(self.apply_sort)
        sort_layout.addWidget(sort_btn, 4, 1)

        layout.addLayout(sort_layout)

        # Results
        layout.addWidget(QLabel("Sorted Results:"))
        self.sort_results_table = RecipeTableWidget()
        layout.addWidget(self.sort_results_table)

        widget.setLayout(layout)
        return widget

    def create_logic_tab(self):
        """Create logical analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Logical Analysis")
        title_font = title.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Logic search
        logic_layout = QVBoxLayout()
        logic_layout.addWidget(QLabel("Logical Search (Variables: cheap, quick, healthy, contains_chicken):"))
        self.logic_expr_input = QLineEdit()
        self.logic_expr_input.setPlaceholderText("e.g., (cheap or quick) and healthy")
        logic_layout.addWidget(self.logic_expr_input)

        logic_btn = QPushButton("Search")
        logic_btn.clicked.connect(self.logic_search)
        logic_layout.addWidget(logic_btn)

        layout.addLayout(logic_layout)

        # Results
        layout.addWidget(QLabel("Matching Recipes:"))
        self.logic_results_table = RecipeTableWidget()
        layout.addWidget(self.logic_results_table)

        # Truth table
        layout.addWidget(QLabel("\nTruth Table Generator:"))
        tt_layout = QHBoxLayout()
        tt_layout.addWidget(QLabel("Expression:"))
        self.tt_expr_input = QLineEdit()
        self.tt_expr_input.setPlaceholderText("e.g., A and B")
        tt_layout.addWidget(self.tt_expr_input)
        tt_btn = QPushButton("Generate")
        tt_btn.clicked.connect(self.generate_truth_table)
        tt_layout.addWidget(tt_btn)
        layout.addLayout(tt_layout)

        # Truth table display
        self.tt_display = QTextEdit()
        self.tt_display.setReadOnly(True)
        self.tt_display.setMaximumHeight(200)
        layout.addWidget(self.tt_display)

        widget.setLayout(layout)
        return widget

    def create_manage_tab(self):
        """Create recipe management tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Manage Recipes")
        title_font = title.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Recipe")
        add_btn.clicked.connect(self.add_recipe)
        btn_layout.addWidget(add_btn)

        edit_btn = QPushButton("Edit Selected")
        edit_btn.clicked.connect(self.edit_recipe)
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_recipe)
        btn_layout.addWidget(delete_btn)

        export_btn = QPushButton("Export to CSV")
        export_btn.clicked.connect(self.export_csv)
        btn_layout.addWidget(export_btn)

        reload_btn = QPushButton("Reload from CSV")
        reload_btn.clicked.connect(self.reload_csv)
        btn_layout.addWidget(reload_btn)

        layout.addLayout(btn_layout)

        # Recipe list
        layout.addWidget(QLabel("Current Recipes:"))
        self.manage_table = RecipeTableWidget()
        layout.addWidget(self.manage_table)

        # Status
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        widget.setLayout(layout)
        return widget

    def create_performance_tab(self):
        """Create performance analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Performance Analysis")
        title_font = title.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Info
        info = QLabel(
            "Algorithm Performance Comparison:\n\n"
            "BubbleSort (Loop-based):\n"
            "  • Time: O(n²) average case\n"
            "  • Space: O(1)\n"
            "  • Best for: Small datasets\n\n"
            "MergeSort (Recursion-based):\n"
            "  • Time: O(n log n) all cases\n"
            "  • Space: O(n)\n"
            "  • Best for: Large datasets"
        )
        info_font = info.font()
        info_font.setPointSize(10)
        info.setFont(info_font)
        layout.addWidget(info)

        # Test parameters
        test_layout = QGridLayout()
        test_layout.addWidget(QLabel("Dataset Size (multiplier):"), 0, 0)
        self.perf_size = QSpinBox()
        self.perf_size.setRange(1, 10)
        self.perf_size.setValue(3)
        test_layout.addWidget(self.perf_size, 0, 1)

        test_btn = QPushButton("Run Performance Test")
        test_btn.clicked.connect(self.run_performance_test)
        test_layout.addWidget(test_btn, 1, 1)

        layout.addLayout(test_layout)

        # Results
        layout.addWidget(QLabel("Results:"))
        self.perf_results = QTextEdit()
        self.perf_results.setReadOnly(True)
        layout.addWidget(self.perf_results)

        widget.setLayout(layout)
        return widget

    def load_data(self):
        """Load recipes from CSV"""
        try:
            csv_path = os.path.join(os.path.dirname(__file__), 'recipes.csv')
            if not os.path.exists(csv_path):
                csv_path = 'recipes.csv'
            self.manager.load_csv(csv_path)
            self.current_recipes = self.manager.recipes
            self.refresh_all_views()
            self.show_status(f"Loaded {len(self.current_recipes)} recipes")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load recipes: {e}")

    def refresh_all_views(self):
        """Refresh all recipe displays"""
        self.recipe_table.load_recipes(self.current_recipes)
        self.manage_table.load_recipes(self.current_recipes)

    def on_recipe_selected(self):
        """Handle recipe selection in browse tab"""
        row = self.recipe_table.currentRow()
        if row >= 0 and row < len(self.current_recipes):
            recipe = self.current_recipes[row]
            details = (
                f"<b>{recipe.name}</b><br>"
                f"Category: {recipe.category}<br>"
                f"Price: ${recipe.price:.2f}<br>"
                f"Time: {recipe.time_minutes} minutes<br>"
                f"Calories: {recipe.calories}<br>"
                f"Difficulty: {recipe.difficulty}<br><br>"
                f"<b>Ingredients:</b><br>"
                f"{', '.join(recipe.ingredients)}<br><br>"
                f"<b>Steps:</b><br>"
                f"{', '.join(recipe.steps)}"
            )
            self.detail_text.setHtml(details)

    def search_by_name(self):
        """Search recipes by name"""
        name = self.search_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a name")
            return
        recipe = self.manager.find_by_name(name)
        results = [recipe] if recipe else []
        self.search_results_table.load_recipes(results)
        self.show_status(f"Found {len(results)} recipe(s)")

    def search_by_category(self):
        """Search recipes by category"""
        category = self.search_category_input.text().strip()
        if not category:
            QMessageBox.warning(self, "Input Error", "Please enter a category")
            return
        results = self.manager.search_by_category(category)
        self.search_results_table.load_recipes(results)
        self.show_status(f"Found {len(results)} recipe(s) in category '{category}'")

    def search_by_ingredient(self):
        """Search recipes by ingredient"""
        ingredient = self.search_ingredient_input.text().strip()
        if not ingredient:
            QMessageBox.warning(self, "Input Error", "Please enter an ingredient")
            return
        results = self.manager.search_by_ingredient(ingredient)
        self.search_results_table.load_recipes(results)
        self.show_status(f"Found {len(results)} recipe(s) with '{ingredient}'")

    def apply_sort(self):
        """Apply sorting to recipes"""
        algo = BubbleSort() if "Bubble" in self.sort_algo.currentText() else MergeSort()
        key_name = self.sort_key.currentText().lower()
        reverse = self.sort_order.currentText() == "Descending"

        def key_func(r):
            if key_name == "price":
                primary = r.price
            elif key_name == "time":
                primary = r.time_minutes
            else:
                primary = r.calories

            secondary = 0
            logic_expr = self.sort_logic_input.text().strip()
            if logic_expr:
                env = {
                    'cheap': r.price < 4.0,
                    'quick': r.time_minutes <= 15,
                    'healthy': r.calories < 400,
                }
                try:
                    secondary = 0 if eval_expr(logic_expr, env) else 1
                except Exception:
                    secondary = 1

            return (primary, secondary)

        try:
            sorted_recipes = algo.sort(self.current_recipes, key_func=key_func, reverse=reverse)
            self.sort_results_table.load_recipes(sorted_recipes)
            algo_name = "BubbleSort" if "Bubble" in self.sort_algo.currentText() else "MergeSort"
            self.show_status(f"Sorted {len(sorted_recipes)} recipes using {algo_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Sorting failed: {e}")

    def logic_search(self):
        """Search using logical expressions"""
        expr = self.logic_expr_input.text().strip()
        if not expr:
            QMessageBox.warning(self, "Input Error", "Please enter a logical expression")
            return

        results = []
        for recipe in self.current_recipes:
            env = {
                'cheap': recipe.price < 4.0,
                'quick': recipe.time_minutes <= 15,
                'healthy': recipe.calories < 400,
                'contains_chicken': any('chicken' in i.lower() for i in recipe.ingredients),
            }
            try:
                if eval_expr(expr, env):
                    results.append(recipe)
            except LogicEvalError as e:
                QMessageBox.critical(self, "Logic Error", f"Invalid expression: {e}")
                return

        self.logic_results_table.load_recipes(results)
        self.show_status(f"Found {len(results)} recipes matching '{expr}'")

    def generate_truth_table(self):
        """Generate and display truth table"""
        expr = self.tt_expr_input.text().strip()
        if not expr:
            QMessageBox.warning(self, "Input Error", "Please enter an expression")
            return

        try:
            vars_, rows = truth_table(expr)
            # Format as table
            header = " | ".join(f"{v:^3}" for v in vars_) + " | Result"
            separator = "-" * len(header)
            table_str = header + "\n" + separator + "\n"
            for vals, res in rows:
                table_str += " | ".join(f"{v:^3}" for v in vals) + f" |   {res}\n"
            self.tt_display.setText(table_str)
            self.show_status(f"Generated truth table for '{expr}'")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not generate truth table: {e}")

    def add_recipe(self):
        """Add new recipe"""
        dialog = AddRecipeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                recipe = dialog.get_recipe()
                self.manager.add_recipe(recipe)
                self.current_recipes = self.manager.recipes
                self.refresh_all_views()
                self.show_status(f"Added recipe: {recipe.name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not add recipe: {e}")

    def edit_recipe(self):
        """Edit selected recipe"""
        row = self.manage_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a recipe")
            return

        recipe = self.current_recipes[row]
        dialog = AddRecipeDialog(self, recipe)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                updated = dialog.get_recipe()
                self.current_recipes[row] = updated
                self.refresh_all_views()
                self.show_status(f"Updated recipe: {updated.name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not update recipe: {e}")

    def delete_recipe(self):
        """Delete selected recipe"""
        row = self.manage_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a recipe")
            return

        recipe = self.current_recipes[row]
        reply = QMessageBox.question(self, "Confirm Delete", f"Delete '{recipe.name}'?")
        if reply == QMessageBox.StandardButton.Yes:
            del self.current_recipes[row]
            self.refresh_all_views()
            self.show_status(f"Deleted recipe: {recipe.name}")

    def export_csv(self):
        """Export recipes to CSV"""
        try:
            export_path = "exported_recipes.csv"
            self.manager.recipes = self.current_recipes
            self.manager.save_csv(export_path)
            QMessageBox.information(self, "Success", f"Recipes exported to {export_path}")
            self.show_status(f"Exported {len(self.current_recipes)} recipes")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not export: {e}")

    def reload_csv(self):
        """Reload recipes from CSV"""
        try:
            csv_path = os.path.join(os.path.dirname(__file__), 'recipes.csv')
            if not os.path.exists(csv_path):
                csv_path = 'recipes.csv'
            self.manager.load_csv(csv_path)
            self.current_recipes = self.manager.recipes
            self.refresh_all_views()
            self.show_status(f"Reloaded {len(self.current_recipes)} recipes")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not reload: {e}")

    def run_performance_test(self):
        """Run performance comparison test"""
        multiplier = self.perf_size.value()
        base_size = len(self.current_recipes)
        if base_size == 0:
            QMessageBox.warning(self, "Error", "No recipes to test")
            return

        # Create test data by repeating recipes
        test_data = (self.current_recipes * multiplier)[:base_size * multiplier]

        results = []
        for dataset_size in [10, 50, 100]:
            sample = test_data[:min(dataset_size, len(test_data))]
            if not sample:
                continue

            bs = BubbleSort()
            ms = MergeSort()

            # BubbleSort timing
            start = time.time()
            bs.sort(sample, key_func=lambda r: r.price)
            bubble_time = time.time() - start

            # MergeSort timing
            start = time.time()
            ms.sort(sample, key_func=lambda r: r.price)
            merge_time = time.time() - start

            results.append(
                f"Dataset size: {len(sample)}\n"
                f"  BubbleSort (O(n²)): {bubble_time:.6f}s\n"
                f"  MergeSort (O(n log n)): {merge_time:.6f}s\n"
                f"  Ratio (Bubble/Merge): {bubble_time/merge_time if merge_time > 0 else 0:.2f}x\n"
            )

        self.perf_results.setText("\n".join(results))
        self.show_status("Performance test completed")

    def show_status(self, message: str):
        """Update status label"""
        self.status_label.setText(message)
        QTimer.singleShot(3000, lambda: self.status_label.setText("Ready"))


def main():
    app = QApplication(sys.argv)
    gui = RecipeGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
