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
    QSplitter, QGroupBox, QGridLayout, QStackedWidget, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap, QLinearGradient, QPalette

from recipe_system.manager import RecipeManager
from recipe_system.recipe import Recipe
from recipe_system.sorting import BubbleSort, MergeSort
from recipe_system.logic import eval_expr, truth_table, LogicEvalError
import os

# Premium Modern "Chef's Kitchen" theme
GLOBAL_STYLE = """
QMainWindow {
    background-color: #ffffff;
}

/* Sidebar Styling */
#sidebar {
    background-color: #2d3436;
    min-width: 220px;
    max-width: 220px;
    border-right: 1px solid #dfe6e9;
}

#sidebar_title {
    color: #fab1a0;
    font-size: 18px;
    font-weight: bold;
    padding: 25px 15px;
    border-bottom: 1px solid #3d4548;
    margin-bottom: 10px;
}

QPushButton.nav_btn {
    background-color: transparent;
    color: #b2bec3;
    text-align: left;
    padding: 12px 20px;
    border-radius: 0px;
    font-size: 14px;
    font-weight: 500;
    border-left: 4px solid transparent;
}

QPushButton.nav_btn:hover {
    background-color: #3d4548;
    color: white;
}

QPushButton.nav_btn[active="true"] {
    background-color: #3d4548;
    color: #fab1a0;
    border-left: 4px solid #fab1a0;
}

/* Main Content Styling */
#content_area {
    background-color: #f9f9f9;
}

QGroupBox {
    background-color: white;
    border: 1px solid #e1e8ed;
    border-radius: 12px;
    margin-top: 20px;
    font-weight: bold;
    font-size: 14px;
    color: #2d3436;
    padding-top: 25px;
}

QLabel#title_label {
    color: #2d3436;
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 5px;
}

/* Table Styling */
QTableWidget {
    background-color: white;
    border: none;
    gridline-color: #f1f2f6;
    border-radius: 8px;
    selection-background-color: #fff4f2;
    selection-color: #e17055;
    alternate-background-color: #fafafa;
}

QHeaderView::section {
    background-color: white;
    padding: 12px;
    border: none;
    border-bottom: 2px solid #f1f2f6;
    font-weight: bold;
    color: #636e72;
    text-transform: uppercase;
    font-size: 11px;
}

/* Action Buttons */
QPushButton.primary_btn {
    background-color: #e17055;
    color: white;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton.primary_btn:hover {
    background-color: #d35400;
}

QPushButton.secondary_btn {
    background-color: #dfe6e9;
    color: #2d3436;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 600;
}

QPushButton.secondary_btn:hover {
    background-color: #b2bec3;
}

QPushButton#delete_btn {
    background-color: #ff7675;
}

/* Inputs */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
    border: 2px solid #dfe6e9;
    border-radius: 8px;
    padding: 10px;
    background-color: white;
    color: #2d3436;
}

QLineEdit:focus, QComboBox:focus {
    border: 2px solid #fab1a0;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 8px;
}

QScrollBar::handle:vertical {
    background: #dfe6e9;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #b2bec3;
}
"""


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
        self.setWindowTitle("Recipe Details")
        self.setMinimumWidth(500)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.name_input = QLineEdit()
        self.category_input = QLineEdit()
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 100)
        self.time_input = QSpinBox()
        self.time_input.setRange(0, 1000)
        self.ingredients_input = QTextEdit()
        self.ingredients_input.setMinimumHeight(80)
        self.steps_input = QTextEdit()
        self.steps_input.setMinimumHeight(80)
        self.calories_input = QSpinBox()
        self.calories_input.setRange(0, 5000)
        self.difficulty_input = QComboBox()
        self.difficulty_input.addItems(["Easy", "Medium", "Hard"])

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Price ($):", self.price_input)
        form_layout.addRow("Time (min):", self.time_input)
        form_layout.addRow("Ingredients (;):", self.ingredients_input)
        form_layout.addRow("Steps (;):", self.steps_input)
        form_layout.addRow("Calories (kcal):", self.calories_input)
        form_layout.addRow("Difficulty:", self.difficulty_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(10)
        main_layout.addWidget(buttons)

        self.setLayout(main_layout)
        
        # Apply style to dialog as well
        self.setStyleSheet(GLOBAL_STYLE)

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
        """Initialize modern sidebar-based UI"""
        self.setWindowTitle("Chef's Selection System")
        self.setGeometry(50, 50, 1300, 800)

        # Main Layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(5)

        title = QLabel("🍳 CHEF'S APP")
        title.setObjectName("sidebar_title")
        sidebar_layout.addWidget(title)

        self.nav_buttons = []
        nav_items = [
            ("🏠 Browse", 0),
            ("🔍 Search", 1),
            ("📊 Sort", 2),
            ("🧠 Logic", 3),
            ("📋 Manage", 4),
            ("⚡ Performance", 5)
        ]

        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setProperty("active", "false")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=index: self.change_page(idx))
            btn.setObjectName("nav_btn")
            btn.setMinimumHeight(50)
            btn.setCheckable(True) # Just for styling convenience
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()
        
        # User feedback status in sidebar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #636e72; padding: 20px; font-size: 11px;")
        sidebar_layout.addWidget(self.status_label)
        
        self.sidebar.setLayout(sidebar_layout)
        main_layout.addWidget(self.sidebar)

        # Content Area
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_area")
        
        self.content_stack.addWidget(self.create_browse_tab())
        self.content_stack.addWidget(self.create_search_tab())
        self.content_stack.addWidget(self.create_sort_tab())
        self.content_stack.addWidget(self.create_logic_tab())
        self.content_stack.addWidget(self.create_manage_tab())
        self.content_stack.addWidget(self.create_performance_tab())

        main_layout.addWidget(self.content_stack)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Set first page active
        self.change_page(0)

    def change_page(self, index):
        """Switch between pages and update sidebar styling"""
        self.content_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", str(i == index).lower())
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def create_browse_tab(self):
        """Create recipe browsing tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)

        # Title
        title = QLabel("Menu Exploration")
        title.setObjectName("title_label")
        layout.addWidget(title)
        
        subtitle = QLabel("Select a recipe below to view detailed cooking instructions and nutrition facts.")
        subtitle.setStyleSheet("color: #636e72; margin-bottom: 20px; font-size: 13px;")
        layout.addWidget(subtitle)

        # Recipe table
        self.recipe_table = RecipeTableWidget()
        layout.addWidget(self.recipe_table)

        # Detail view
        detail_group = QGroupBox("Recipe Spotlight")
        detail_layout = QVBoxLayout()
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setMinimumHeight(350)
        self.detail_text.setFrameStyle(0)
        detail_layout.addWidget(self.detail_text)
        detail_group.setLayout(detail_layout)
        
        # Splitter for adjustable table/detail ratio
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.recipe_table)
        splitter.addWidget(detail_group)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)

        # Connect selection
        self.recipe_table.selectionModel().selectionChanged.connect(self.on_recipe_selected)

        widget.setLayout(layout)
        return widget

    def create_search_tab(self):
        """Create search tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("Find Your Perfect Dish")
        title.setObjectName("title_label")
        layout.addWidget(title)

        # Search options
        search_card = QGroupBox("Search Options")
        search_layout = QGridLayout()
        search_layout.setContentsMargins(15, 20, 15, 15)
        search_layout.setSpacing(10)
        
        search_layout.addWidget(QLabel("By Name:"), 0, 0)
        self.search_name_input = QLineEdit()
        self.search_name_input.setPlaceholderText("Enter dish name...")
        search_layout.addWidget(self.search_name_input, 0, 1)
        search_by_name_btn = QPushButton("Search Name")
        search_by_name_btn.setObjectName("search_btn")
        search_by_name_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_by_name_btn.setFixedWidth(150)
        search_by_name_btn.setStyleSheet("background-color: #e17055; color: white; border-radius: 6px; padding: 8px; font-weight: bold;")
        search_by_name_btn.clicked.connect(self.search_by_name)
        search_layout.addWidget(search_by_name_btn, 0, 2)

        search_layout.addWidget(QLabel("By Category:"), 1, 0)
        self.search_category_input = QLineEdit()
        self.search_category_input.setPlaceholderText("e.g., starter, main, soup...")
        search_layout.addWidget(self.search_category_input, 1, 1)
        search_by_cat_btn = QPushButton("Search Category")
        search_by_cat_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_by_cat_btn.setFixedWidth(150)
        search_by_cat_btn.setStyleSheet("background-color: #e17055; color: white; border-radius: 6px; padding: 8px; font-weight: bold;")
        search_by_cat_btn.clicked.connect(self.search_by_category)
        search_layout.addWidget(search_by_cat_btn, 1, 2)

        search_layout.addWidget(QLabel("By Ingredient:"), 2, 0)
        self.search_ingredient_input = QLineEdit()
        self.search_ingredient_input.setPlaceholderText("e.g., chicken, tomato...")
        search_layout.addWidget(self.search_ingredient_input, 2, 1)
        search_by_ing_btn = QPushButton("Search Ingredient")
        search_by_ing_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_by_ing_btn.setFixedWidth(150)
        search_by_ing_btn.setStyleSheet("background-color: #e17055; color: white; border-radius: 6px; padding: 8px; font-weight: bold;")
        search_by_ing_btn.clicked.connect(self.search_by_ingredient)
        search_layout.addWidget(search_by_ing_btn, 2, 2)

        search_card.setLayout(search_layout)
        layout.addWidget(search_card)

        # Results
        results_group = QGroupBox("Search Results")
        results_layout = QVBoxLayout()
        self.search_results_table = RecipeTableWidget()
        results_layout.addWidget(self.search_results_table)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        widget.setLayout(layout)
        return widget

    def create_sort_tab(self):
        """Create sorting tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("Organize Recipes")
        title.setObjectName("title_label")
        layout.addWidget(title)

        # Sort options
        sort_card = QGroupBox("Sorting Configuration")
        sort_layout = QGridLayout()
        sort_layout.setContentsMargins(15, 20, 15, 15)
        sort_layout.setSpacing(12)

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

        sort_btn = QPushButton("Apply Sorting")
        sort_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        sort_btn.setStyleSheet("background-color: #fab1a0; color: #d35400; border-radius: 8px; padding: 12px; font-weight: bold; border: 1px solid #e17055;")
        sort_btn.clicked.connect(self.apply_sort)
        sort_layout.addWidget(sort_btn, 4, 1)

        sort_card.setLayout(sort_layout)
        layout.addWidget(sort_card)

        # Results
        results_group = QGroupBox("Sorted Results")
        results_layout = QVBoxLayout()
        self.sort_results_table = RecipeTableWidget()
        results_layout.addWidget(self.sort_results_table)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        widget.setLayout(layout)
        return widget

    def create_logic_tab(self):
        """Create logical analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("Logical Filtering")
        title.setObjectName("title_label")
        layout.addWidget(title)

        # Logic search
        logic_card = QGroupBox("Recipe Logic Search")
        logic_layout = QVBoxLayout()
        logic_layout.setContentsMargins(15, 20, 15, 15)
        logic_layout.setSpacing(10)
        
        logic_layout.addWidget(QLabel("Expression (Variables: cheap, quick, healthy, contains_chicken):"))
        self.logic_expr_input = QLineEdit()
        self.logic_expr_input.setPlaceholderText("e.g., (cheap or quick) and healthy")
        logic_layout.addWidget(self.logic_expr_input)

        logic_btn = QPushButton("Filter Recipes")
        logic_btn.clicked.connect(self.logic_search)
        logic_layout.addWidget(logic_btn)
        logic_card.setLayout(logic_layout)
        layout.addWidget(logic_card)

        # Results
        results_group = QGroupBox("Filtered Recipes")
        results_layout = QVBoxLayout()
        self.logic_results_table = RecipeTableWidget()
        results_layout.addWidget(self.logic_results_table)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        # Truth table
        tt_card = QGroupBox("Truth Table Generator")
        tt_main_layout = QVBoxLayout()
        tt_main_layout.setContentsMargins(15, 20, 15, 15)
        tt_main_layout.setSpacing(10)
        
        tt_input_layout = QHBoxLayout()
        tt_input_layout.addWidget(QLabel("Logic Expression:"))
        self.tt_expr_input = QLineEdit()
        self.tt_expr_input.setPlaceholderText("e.g., A and B")
        tt_input_layout.addWidget(self.tt_expr_input)
        tt_btn = QPushButton("Generate")
        tt_btn.clicked.connect(self.generate_truth_table)
        tt_input_layout.addWidget(tt_btn)
        tt_main_layout.addLayout(tt_input_layout)

        # Truth table display
        self.tt_display = QTextEdit()
        self.tt_display.setReadOnly(True)
        self.tt_display.setMaximumHeight(200)
        self.tt_display.setFont(QFont("Consolas", 10))
        tt_main_layout.addWidget(self.tt_display)
        
        tt_card.setLayout(tt_main_layout)
        layout.addWidget(tt_card)

        widget.setLayout(layout)
        return widget

    def create_manage_tab(self):
        """Create recipe management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("Recipe Inventory")
        title.setObjectName("title_label")
        layout.addWidget(title)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        add_btn = QPushButton("Add New Recipe")
        add_btn.clicked.connect(self.add_recipe)
        btn_layout.addWidget(add_btn)

        edit_btn = QPushButton("Edit Selected")
        edit_btn.clicked.connect(self.edit_recipe)
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete Selected")
        delete_btn.setObjectName("delete_btn")
        delete_btn.clicked.connect(self.delete_recipe)
        btn_layout.addWidget(delete_btn)

        export_btn = QPushButton("Export CSV")
        export_btn.clicked.connect(self.export_csv)
        btn_layout.addWidget(export_btn)

        reload_btn = QPushButton("Reload All")
        reload_btn.clicked.connect(self.reload_csv)
        btn_layout.addWidget(reload_btn)

        layout.addLayout(btn_layout)

        # Recipe list
        manage_group = QGroupBox("Current Recipe Database")
        manage_layout = QVBoxLayout()
        self.manage_table = RecipeTableWidget()
        manage_layout.addWidget(self.manage_table)
        manage_group.setLayout(manage_layout)
        layout.addWidget(manage_group)

        # Status
        self.status_label = QLabel("Database Ready")
        self.status_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(self.status_label)

        widget.setLayout(layout)
        return widget

    def create_performance_tab(self):
        """Create performance analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("Efficiency Analysis")
        title.setObjectName("title_label")
        layout.addWidget(title)

        # Info
        info_card = QGroupBox("Algorithm Comparison")
        info_layout = QVBoxLayout()
        info = QLabel(
            "<b>BubbleSort (Loop-based):</b><br>"
            "&nbsp;&nbsp;• Time: O(n²) average case<br>"
            "&nbsp;&nbsp;• Best for: Small datasets<br><br>"
            "<b>MergeSort (Recursion-based):</b><br>"
            "&nbsp;&nbsp;• Time: O(n log n) all cases<br>"
            "&nbsp;&nbsp;• Best for: Large datasets"
        )
        info_layout.addWidget(info)
        info_card.setLayout(info_layout)
        layout.addWidget(info_card)

        # Test parameters
        test_card = QGroupBox("Benchmarking Tool")
        test_layout = QGridLayout()
        test_layout.setContentsMargins(15, 20, 15, 15)
        test_layout.setSpacing(10)
        
        test_layout.addWidget(QLabel("Dataset Size Factor:"), 0, 0)
        self.perf_size = QSpinBox()
        self.perf_size.setRange(1, 10)
        self.perf_size.setValue(3)
        test_layout.addWidget(self.perf_size, 0, 1)

        test_btn = QPushButton("Run Comparison Test")
        test_btn.clicked.connect(self.run_performance_test)
        test_layout.addWidget(test_btn, 1, 1)

        test_card.setLayout(test_layout)
        layout.addWidget(test_card)

        # Results
        results_group = QGroupBox("Performance Data")
        results_layout = QVBoxLayout()
        self.perf_results = QTextEdit()
        self.perf_results.setReadOnly(True)
        self.perf_results.setFont(QFont("Consolas", 10))
        results_layout.addWidget(self.perf_results)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

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
            # Advanced HTML with dynamic coloring for difficulty
            diff_color = "#2ecc71" if recipe.difficulty == "Easy" else ("#f1c40f" if recipe.difficulty == "Medium" else "#e74c3c")
            details = f"""
                <div style='font-family: "Segoe UI", sans-serif; background: #fff; border-radius: 12px;'>
                    <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                        <h1 style='color: #2d3436; margin: 0; font-size: 24px;'>{recipe.name}</h1>
                        <span style='background: {diff_color}; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 12px;'>{recipe.difficulty.upper()}</span>
                    </div>
                    <p style='color: #636e72; margin-top: 5px; font-weight: 500;'>{recipe.category} • ${recipe.price:.2f}</p>
                    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin: 20px 0;'>
                        <div style='background: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center;'>
                            <div style='color: #e17055; font-size: 20px; font-weight: bold;'>{recipe.time_minutes}</div>
                            <div style='color: #b2bec3; font-size: 11px;'>MINUTES</div>
                        </div>
                        <div style='background: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center;'>
                            <div style='color: #e17055; font-size: 20px; font-weight: bold;'>{recipe.calories}</div>
                            <div style='color: #b2bec3; font-size: 11px;'>CALORIES</div>
                        </div>
                        <div style='background: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center;'>
                            <div style='color: #e17055; font-size: 20px; font-weight: bold;'>{len(recipe.ingredients)}</div>
                            <div style='color: #b2bec3; font-size: 11px;'>INGREDIENTS</div>
                        </div>
                    </div>
                    <div style='margin-bottom: 20px;'>
                        <h3 style='color: #2d3436; border-bottom: 2px solid #fab1a0; display: inline-block; padding-bottom: 3px; font-size: 14px;'>Required Ingredients</h3>
                        <p style='color: #636e72; line-height: 1.6; font-size: 13px;'>{", ".join(recipe.ingredients)}</p>
                    </div>
                    <div>
                        <h3 style='color: #2d3436; border-bottom: 2px solid #fab1a0; display: inline-block; padding-bottom: 3px; font-size: 14px;'>How to Cook</h3>
                        <p style='color: #636e72; line-height: 1.6; font-size: 13px;'>{", ".join(recipe.steps)}</p>
                    </div>
                </div>
            """
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
                    'contains_chicken': any('chicken' in i.lower() for i in r.ingredients),
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
    app.setStyleSheet(GLOBAL_STYLE)
    
    # Set a default font for the whole app
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    gui = RecipeGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
