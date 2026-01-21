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
    QSplitter, QGroupBox, QGridLayout, QStackedWidget, QFrame, QGraphicsDropShadowEffect,
    QSizePolicy, QAbstractItemView, QStyle
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap, QLinearGradient, QPalette

from recipe_system.manager import RecipeManager
from recipe_system.recipe import Recipe
from recipe_system.sorting import BubbleSort, MergeSort
from recipe_system.logic import eval_expr, truth_table, LogicEvalError
import os

# "Cyber Chef" Dark Theme - High Performance Visuals
GLOBAL_STYLE = """
QWidget {
    color: #cad3f5;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
}

QMainWindow, QDialog {
    background-color: #24273a;  /* Base Dark */
}

/* --- Sidebar --- */
#sidebar {
    background-color: #1e2030; /* Darker Sidebar */
    border-right: 1px solid #363a4f;
    min-width: 240px;
    max-width: 240px;
}

#sidebar_title {
    color: #8aadf4; /* Blue Accent */
    font-size: 22px;
    font-weight: 900;
    padding: 30px 20px;
    border-bottom: 2px solid #363a4f;
    margin-bottom: 15px;
    letter-spacing: 1px;
}

QPushButton[class="nav_btn"] {
    background-color: transparent;
    color: #a5adcb; /* Subtext */
    text-align: left;
    padding: 10px 20px; /* Reduced from 15px 25px */
    border-radius: 10px; /* Slightly tighter radius */
    margin: 4px 15px; /* Reduced margin */
    font-size: 14px; /* Slightly smaller font */
    font-weight: 600;
    border: 1px solid transparent;
}

QPushButton[class="nav_btn"]:hover {
    background-color: #363a4f; /* Surface 0 */
    color: #ffffff;
    border: 1px solid #494d64;
}

QPushButton[class="nav_btn"][active="true"] {
    background-color: #363a4f;
    color: #8aadf4; /* Blue Accent */
    border-left: 4px solid #8aadf4; /* Blue Accent Line */
    padding-left: 16px; /* Adjust for border (20px - 4px = 16px) */
}

/* --- Content Area --- */
#content_area {
    background-color: #24273a;
}

QGroupBox {
    background-color: #181926; /* Deep Surface */
    border: 1px solid #363a4f;
    border-radius: 16px;
    margin-top: 30px;
    font-weight: 700;
    font-size: 15px;
    color: #8aadf4; /* Blue Title */
    padding-top: 10px; /* Reduced from 35px to fix empty space */
    padding-bottom: 5px;
    padding-left: 5px;
    padding-right: 5px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 5px 15px;
    left: 15px;
    top: 5px; /* Added to vertically align title if needed */
    background-color: #24273a;
    border: 1px solid #363a4f;
    border-radius: 8px;
    color: #8aadf4;
}

QLabel#title_label {
    color: #ffffff;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 15px;
    padding-left: 5px;
}

/* --- Modern Table --- */
QTableWidget {
    background-color: #181926;
    color: #cad3f5;
    border: 1px solid #363a4f;
    border-radius: 12px;
    gridline-color: transparent;
    selection-background-color: #363a4f;
    selection-color: #8aadf4;
    outline: none;
    alternate-background-color: #1e2030;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #24273a;
    outline: none;
}

QTableWidget::item:focus {
    outline: none;
    border: none;
}

QTableWidget::item:selected {
    background-color: #363a4f;
    color: #8aadf4;
    border-bottom: 1px solid #8aadf4;
}

QHeaderView {
    background-color: transparent;
    border: none;
}

QHeaderView::section {
    background-color: #24273a;
    color: #a5adcb;
    padding: 12px;
    border: none;
    border-bottom: 2px solid #8aadf4;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 12px;
    letter-spacing: 0.5px;
}

QHeaderView::section:horizontal:first {
    border-top-left-radius: 12px;
}

QHeaderView::section:horizontal:last {
    border-top-right-radius: 12px;
}

/* --- Buttons --- */
QPushButton, QPushButton[class="primary_btn"] {
    background-color: #8aadf4; /* Blue accent color */
    color: #1e2030;            /* Dark text for contrast */
    border-radius: 8px;
    padding: 12px 20px;
    font-weight: 700;
    font-size: 13px;
    border: 1px solid #8aadf4;
}

QPushButton:hover, QPushButton[class="primary_btn"]:hover {
    background-color: #b7cbf8; /* Slightly lighter blue, definitely not green */
    border-color: #b7cbf8;
}

QPushButton:pressed, QPushButton[class="primary_btn"]:pressed {
    background-color: #7dc4e4;
    border-color: #7dc4e4;
    padding-top: 14px; /* Press down effect */
    padding-bottom: 10px;
}

QPushButton[class="secondary_btn"] {
    background-color: #363a4f;
    color: #cad3f5;
    border-radius: 8px;
    padding: 12px 20px;
    font-weight: 600;
    border: 1px solid #494d64;
}

QPushButton[class="secondary_btn"]:hover {
    background-color: #494d64;
    color: #ffffff;
    border: 1px solid #5b6078;
}

QPushButton[class="secondary_btn"]:pressed {
    background-color: #24273a;
    border-color: #363a4f;
}

QPushButton#delete_btn {
    background-color: #363a4f; /* Dark background default */
    color: #ed8796;            /* Red text */
    border: 1px solid #ed8796;
}

QPushButton#delete_btn:hover {
    background-color: #ed8796; /* Red background on hover */
    color: #1e2030;            /* Dark text */
}

/* --- Inputs --- */
QLineEdit, QSpinBox, QDoubleSpinBox {
    border: 1px solid #494d64;
    border-radius: 8px;
    padding: 10px 12px;
    background-color: #181926;
    color: #cad3f5;
    font-size: 14px;
    selection-background-color: #8aadf4;
    selection-color: #1e2030;
}

QTextEdit {
    border: 1px solid #494d64;
    border-radius: 8px;
    padding: 10px 12px;
    background-color: #1e2030;
    color: #cad3f5;
    font-size: 14px;
    selection-background-color: #8aadf4;
    selection-color: #1e2030;
}

QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    border: 1px solid #5b6078;
    background-color: #1e2030;
}

QTextEdit:hover {
    border: 1px solid #5b6078;
    background-color: #1e2030;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {
    border: 2px solid #8aadf4;
    background-color: #1e2030;
    color: #ffffff;
}

/* --- Combo Box --- */
QComboBox {
    border: 1px solid #494d64;
    border-radius: 8px;
    padding: 10px 12px;
    background-color: #181926;
    color: #cad3f5;
    min-width: 6em;
}

QComboBox:hover {
    border: 1px solid #5b6078;
    background-color: #1e2030;
}

QComboBox:on {
    border: 2px solid #8aadf4;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
    border-left-width: 0px;
}

/* POPUP MENU STYLING */
QComboBox QAbstractItemView {
    background-color: #1e2030; 
    color: #cad3f5;           
    border: 1px solid #8aadf4;
    border-radius: 8px;
    selection-background-color: #363a4f;
    selection-color: #8aadf4;
    outline: none;
    padding: 5px;
}

/* --- Scrollbars --- */
QScrollBar:vertical {
    border: none;
    background: #24273a;
    width: 12px;
    margin: 0px; 
}

QScrollBar::handle:vertical {
    background: #494d64;
    min-height: 20px;
    border-radius: 6px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background: #8aadf4;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
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
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False)  # Hide vertical row numbers

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
        self.setWindowTitle("Recipe Editor")
        self.setMinimumWidth(700)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 40, 30, 30)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("Recipe Details")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #f5a97f; margin-bottom: 5px;")
        main_layout.addWidget(title)

        # Helper to style labels
        def create_label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("font-weight: 700; color: #a5adcb; font-size: 14px;")
            return lbl

        # Name
        name_layout = QVBoxLayout()
        name_layout.setSpacing(8)
        name_layout.addWidget(create_label("Recipe Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Grandma's Apple Pie")
        name_layout.addWidget(self.name_input)
        main_layout.addLayout(name_layout)

        # Category
        cat_layout = QVBoxLayout()
        cat_layout.setSpacing(8)
        cat_layout.addWidget(create_label("Category:"))
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("e.g. Dessert")
        cat_layout.addWidget(self.category_input)
        main_layout.addLayout(cat_layout)

        # Metrics Row (Price, Time, Cal, Diff)
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(15)

        # Price
        price_group = QVBoxLayout()
        price_group.setSpacing(8)
        price_group.addWidget(create_label("Price ($)"))
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 1000)
        self.price_input.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.price_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        price_group.addWidget(self.price_input)
        metrics_layout.addLayout(price_group)

        # Time
        time_group = QVBoxLayout()
        time_group.setSpacing(8)
        time_group.addWidget(create_label("Time (min)"))
        self.time_input = QSpinBox()
        self.time_input.setRange(0, 10000)
        self.time_input.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.time_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        time_group.addWidget(self.time_input)
        metrics_layout.addLayout(time_group)

        # Calories
        cal_group = QVBoxLayout()
        cal_group.setSpacing(8)
        cal_group.addWidget(create_label("Calories"))
        self.calories_input = QSpinBox()
        self.calories_input.setRange(0, 10000)
        self.calories_input.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.calories_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        cal_group.addWidget(self.calories_input)
        metrics_layout.addLayout(cal_group)

        # Difficulty
        diff_group = QVBoxLayout()
        diff_group.setSpacing(8)
        diff_group.addWidget(create_label("Difficulty"))
        self.difficulty_input = QComboBox()
        self.difficulty_input.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        diff_group.addWidget(self.difficulty_input)
        metrics_layout.addLayout(diff_group)

        main_layout.addLayout(metrics_layout)

        # Text Areas
        text_layout = QVBoxLayout()
        text_layout.setSpacing(15)
        
        text_layout.addWidget(create_label("Ingredients (semicolon separated):"))
        self.ingredients_input = QTextEdit()
        self.ingredients_input.setPlaceholderText("Flour; Sugar; Eggs; Milk")
        self.ingredients_input.setMinimumHeight(80)
        text_layout.addWidget(self.ingredients_input)

        text_layout.addWidget(create_label("Steps (semicolon separated):"))
        self.steps_input = QTextEdit()
        self.steps_input.setPlaceholderText("Mix ingredients; Bake at 350F; Serve warm")
        self.steps_input.setMinimumHeight(80)
        text_layout.addWidget(self.steps_input)

        main_layout.addLayout(text_layout)
        main_layout.addSpacing(10)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        ok_btn = buttons.button(QDialogButtonBox.StandardButton.Ok)
        ok_btn.setText("Save Recipe")
        ok_btn.setProperty("class", "primary_btn")
        
        cancel_btn = buttons.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_btn.setProperty("class", "secondary_btn")

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
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
            btn.setProperty("class", "nav_btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=index: self.change_page(idx))
            # btn.setObjectName("nav_btn") # Replaced by class property for better CSS handling
            btn.setMinimumHeight(50)
            # Removed setCheckable(True) to fix the "sticky" selection issue
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()
        
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
        subtitle.setStyleSheet("color: #ffffff; margin-bottom: 20px; font-size: 13px;")
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
        self.detail_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.detail_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.detail_text.setStyleSheet("QScrollBar {height:0px; width:0px;}") # Force hide
        detail_layout.addWidget(self.detail_text)
        detail_group.setLayout(detail_layout)
        
        # Splitter for adjustable table/detail ratio
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.recipe_table)
        splitter.addWidget(detail_group)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2) # Give Spotlight twice the space
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
        search_by_name_btn.setStyleSheet("background-color: #8aadf4; color: #1e2030; border-radius: 6px; padding: 10px; font-weight: bold;")
        search_by_name_btn.clicked.connect(self.search_by_name)
        search_layout.addWidget(search_by_name_btn, 0, 2)

        search_layout.addWidget(QLabel("By Category:"), 1, 0)
        self.search_category_input = QLineEdit()
        self.search_category_input.setPlaceholderText("e.g., starter, main, soup...")
        search_layout.addWidget(self.search_category_input, 1, 1)
        search_by_cat_btn = QPushButton("Search Category")
        search_by_cat_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_by_cat_btn.setFixedWidth(150)
        search_by_cat_btn.setStyleSheet("background-color: #8aadf4; color: #1e2030; border-radius: 6px; padding: 10px; font-weight: bold;")
        search_by_cat_btn.clicked.connect(self.search_by_category)
        search_layout.addWidget(search_by_cat_btn, 1, 2)

        search_layout.addWidget(QLabel("By Ingredient:"), 2, 0)
        self.search_ingredient_input = QLineEdit()
        self.search_ingredient_input.setPlaceholderText("e.g., chicken, tomato...")
        search_layout.addWidget(self.search_ingredient_input, 2, 1)
        search_by_ing_btn = QPushButton("Search Ingredient")
        search_by_ing_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_by_ing_btn.setFixedWidth(150)
        search_by_ing_btn.setStyleSheet("background-color: #8aadf4; color: #1e2030; border-radius: 6px; padding: 10px; font-weight: bold;")
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
        # Using consistent blue theme
        sort_btn.setStyleSheet("background-color: #8aadf4; color: #1e2030; border-radius: 8px; padding: 12px; font-weight: bold; border: 1px solid #8aadf4;")
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
        
        # Horizontal layout for Input + Button
        input_layout = QHBoxLayout()
        self.logic_expr_input = QLineEdit()
        self.logic_expr_input.setPlaceholderText("e.g., (cheap or quick) and healthy")
        input_layout.addWidget(self.logic_expr_input)

        logic_btn = QPushButton("Filter Recipes")
        logic_btn.setFixedWidth(140)
        logic_btn.clicked.connect(self.logic_search)
        input_layout.addWidget(logic_btn)

        logic_layout.addLayout(input_layout)
        logic_card.setLayout(logic_layout)
        layout.addWidget(logic_card)

        # Results
        results_group = QGroupBox("Filtered Recipes")
        results_layout = QVBoxLayout()
        results_layout.setContentsMargins(10, 15, 10, 10)
        self.logic_results_table = RecipeTableWidget()
        results_layout.addWidget(self.logic_results_table)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group, 1)  # Stretch factor 1 to maximize space

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
        self.tt_display.setMaximumHeight(100)
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
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header Row (Title + Icons)
        header_layout = QHBoxLayout()
        
        title = QLabel("Recipe Inventory")
        title.setObjectName("title_label")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Icon Button Style
        icon_btn_style = """
            QPushButton {
                background-color: #363a4f; /* Darker background for visibility */
                border: 1px solid #494d64;
                border-radius: 8px;
                padding: 8px;
                min-width: 32px;
                min-height: 32px;
            }
            QPushButton:hover {
                background-color: #494d64;
                border-color: #5b6078;
            }
        """

        # Delete Icon
        delete_btn = QPushButton()
        delete_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
        delete_btn.setIconSize(QSize(20, 20))
        delete_btn.setToolTip("Delete Selected")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # Unique hover for delete (Reddish)
        delete_btn.setStyleSheet(icon_btn_style + "QPushButton:hover { background-color: #ed8796; border-color: #ed8796; }")
        delete_btn.clicked.connect(self.delete_recipe)
        header_layout.addWidget(delete_btn)

        layout.addLayout(header_layout)

        # Main Table Area
        self.manage_table = RecipeTableWidget()
        layout.addWidget(self.manage_table)

        # Footer Buttons
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(15)
        
        # Consistent Blue Style for Action Buttons
        btn_style = """
            QPushButton {
                background-color: #8aadf4; 
                color: #1e2030;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: 700;
                font-size: 13px;
                border: 1px solid #8aadf4;
            }
            QPushButton:hover {
                background-color: #b7cbf8; /* Periwinkle hover (Not Green) */
                border-color: #b7cbf8;
            }
            QPushButton:pressed {
                background-color: #7dc4e4;
                border-color: #7dc4e4;
            }
        """

        add_btn = QPushButton("Add New Recipe")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(btn_style)
        add_btn.clicked.connect(self.add_recipe)
        footer_layout.addWidget(add_btn)

        edit_btn = QPushButton("Edit Selected")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet(btn_style)
        edit_btn.clicked.connect(self.edit_recipe)
        footer_layout.addWidget(edit_btn)

        export_btn = QPushButton("Export CSV")
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.setStyleSheet(btn_style)
        export_btn.clicked.connect(self.export_csv)
        footer_layout.addWidget(export_btn)

        layout.addLayout(footer_layout)

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
        
        # Single row layout
        test_layout = QHBoxLayout()
        test_layout.setContentsMargins(15, 20, 15, 15)
        test_layout.setSpacing(10)
        
        test_layout.addWidget(QLabel("Dataset Size Factor:"))
        
        self.perf_size = QSpinBox()
        self.perf_size.setRange(1, 10000)
        self.perf_size.setValue(3)
        self.perf_size.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons) # Remove arrows
        test_layout.addWidget(self.perf_size)

        test_btn = QPushButton("Run Comparison Test")
        test_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        test_btn.clicked.connect(self.run_performance_test)
        test_layout.addWidget(test_btn)
        
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
            # Advanced HTML with dynamic coloring for difficulty in Dark Mode
            diff_color = "#a6da95" if recipe.difficulty == "Easy" else ("#eed49f" if recipe.difficulty == "Medium" else "#ed8796")
            # Using Catppuccin-inspired Dark Theme colors for internal HTML
            # Using HTML Tables instead of Flex/Grid for compatibility with QTextEdit
            details = f"""
                <div style='font-family: "Segoe UI", sans-serif; background: #1e2030; border-radius: 12px; padding: 10px; color: #cad3f5;'>
                    <table width="100%" cellspacing="0" cellpadding="0">
                        <tr>
                            <td align="left">
                                <h1 style='color: #8aadf4; margin: 0; font-size: 22px;'>{recipe.name}</h1>
                            </td>
                            <td align="right">
                                <span style='background: {diff_color}; color: #1e2030; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px;'>{recipe.difficulty.upper()}</span>
                            </td>
                        </tr>
                    </table>
                    <p style='color: #a5adcb; margin-top: 2px; font-weight: 500; font-size: 13px;'>{recipe.category} • ${recipe.price:.2f}</p>
                    
                    <table width="100%" cellspacing="5" cellpadding="0" style="margin: 10px 0;">
                        <tr>
                            <td width="33%" style='background: #24273a; padding: 10px; border-radius: 8px; border: 1px solid #363a4f;'>
                                <div style='color: #f5a97f; font-size: 18px; font-weight: bold; text-align: left;'>{recipe.time_minutes}</div>
                                <div style='color: #a5adcb; font-size: 10px; text-align: left;'>MINUTES</div>
                            </td>
                            <td width="33%" style='background: #24273a; padding: 10px; border-radius: 8px; border: 1px solid #363a4f;'>
                                <div style='color: #f5a97f; font-size: 18px; font-weight: bold; text-align: left;'>{recipe.calories}</div>
                                <div style='color: #a5adcb; font-size: 10px; text-align: left;'>CALORIES</div>
                            </td>
                            <td width="33%" style='background: #24273a; padding: 10px; border-radius: 8px; border: 1px solid #363a4f;'>
                                <div style='color: #f5a97f; font-size: 18px; font-weight: bold; text-align: left;'>{len(recipe.ingredients)}</div>
                                <div style='color: #a5adcb; font-size: 10px; text-align: left;'>INGREDIENTS</div>
                            </td>
                        </tr>
                    </table>

                    <div style='margin-bottom: 10px;'>
                        <h3 style='color: #f5bde6; border-bottom: 2px solid #363a4f; display: inline-block; padding-bottom: 2px; font-size: 13px; margin: 0;'>Required Ingredients</h3>
                        <p style='color: #cad3f5; line-height: 1.4; font-size: 12px; margin-top: 5px;'>{", ".join(recipe.ingredients)}</p>
                    </div>
                    <div>
                        <h3 style='color: #f5bde6; border-bottom: 2px solid #363a4f; display: inline-block; padding-bottom: 2px; font-size: 13px; margin: 0;'>How to Cook</h3>
                        <p style='color: #cad3f5; line-height: 1.4; font-size: 12px; margin-top: 5px;'>{", ".join(recipe.steps)}</p>
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
        results = self.manager.search_by_name(name)
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
        print(f"Status: {message}")
        # self.status_label.setText(message)
        # QTimer.singleShot(3000, lambda: self.status_label.setText("Ready"))


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
