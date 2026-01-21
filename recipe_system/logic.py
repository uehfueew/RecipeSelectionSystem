"""
Logic Module - Boolean Expression Evaluator
─────────────────────────────────────────────
This module provides tools for working with boolean (True/False) logic expressions.

It allows you to:
1. Evaluate expressions like: "(healthy AND cheap) OR quick"
2. Generate truth tables showing all possible combinations of variables
3. Parse and validate boolean expressions safely

This is useful for creating flexible filters in the recipe system.
Examples:
- "(price < 5) AND (time < 20)"
- "healthy OR (quick AND cheap)"
"""

import ast
from typing import Dict, List, Tuple


class LogicEvalError(Exception):
    """Exception raised when there's an error in evaluating a logical expression."""
    pass


def _collect_vars(node, vars_set: set):
    """
    Helper function: Recursively extracts all variable names from an AST node.
    
    This function walks through an Abstract Syntax Tree (AST) and collects all
    variable names found in the expression.
    
    For example: "(A AND B) OR C" -> collects {'A', 'B', 'C'}
    
    Args:
        node: An AST node to analyze
        vars_set: A set that will be populated with variable names
    """
    # If this node is a variable name, add it to the set
    if isinstance(node, ast.Name):
        vars_set.add(node.id)
    # Recursively check all child nodes
    for child in ast.iter_child_nodes(node):
        _collect_vars(child, vars_set)


def parse_vars(expr: str) -> List[str]:
    """
    Extracts and returns a sorted list of all variable names in an expression.
    
    Args:
        expr: A boolean expression string (e.g., "A AND B OR C")
        
    Returns:
        A sorted list of unique variable names found in the expression
        
    Raises:
        LogicEvalError: If the expression cannot be parsed
        
    Examples:
        parse_vars("A AND B") -> ["A", "B"]
        parse_vars("(healthy OR quick) AND cheap") -> ["cheap", "healthy", "quick"]
    """
    # Normalize operators to Python syntax
    expr = expr.replace('∧', ' and ').replace('∨', ' or ').replace('¬', ' not ')
    expr = expr.replace('AND', 'and').replace('OR', 'or').replace('NOT', 'not')
    
    try:
        # Parse the expression into an Abstract Syntax Tree
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise LogicEvalError(f"Syntax error in expression: {e}")
    
    # Collect all variable names from the tree
    vars_set = set()
    _collect_vars(tree, vars_set)
    
    # Return sorted list for consistent ordering
    return sorted(vars_set)


def _eval_node(node, env: Dict[str, bool]):
    """
    Helper function: Recursively evaluates an AST node given variable values.
    
    This function processes the Abstract Syntax Tree and computes the result by:
    1. Looking up variable values from the environment dict
    2. Applying logical operators (AND, OR, NOT)
    3. Returning the boolean result
    
    Args:
        node: The AST node to evaluate
        env: Dictionary mapping variable names to True/False values
        
    Returns:
        The boolean result of evaluating the node
        
    Raises:
        LogicEvalError: If there's an unknown variable or unsupported operator
    """
    # Handle Expression wrapper nodes
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, env)
    
    # Handle variable names - look up their value in the environment
    if isinstance(node, ast.Name):
        if node.id in env:
            return bool(env[node.id])
        raise LogicEvalError(f"Unknown variable: {node.id}")
    
    # Handle NOT operator (unary operation)
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.Not):
            return not _eval_node(node.operand, env)
        # Reject unsupported unary operators like negation (-)
        raise LogicEvalError("Unsupported operator")
    
    # Handle AND and OR operators (boolean operations)
    if isinstance(node, ast.BoolOp):
        # AND: all values must be True
        if isinstance(node.op, ast.And):
            return all(_eval_node(v, env) for v in node.values)
        # OR: at least one value must be True
        if isinstance(node.op, ast.Or):
            return any(_eval_node(v, env) for v in node.values)
    
    # Handle boolean constants (True/False literals)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            return node.value
    
    # Reject any other node types as unsupported
    raise LogicEvalError(f"Unsupported operation: {type(node).__name__}")


def eval_expr(expr: str, env: Dict[str, bool]) -> bool:
    """
    Evaluates a boolean expression with given variable values.
    
    This is the main function for evaluating expressions. It safely evaluates
    logical expressions without allowing dangerous operations.
    
    Supported operators:
    - AND / ∧ (logical AND)
    - OR / ∨ (logical OR)
    - NOT / ¬ (logical NOT)
    - Parentheses for grouping
    
    Args:
        expr: A boolean expression string (e.g., "(healthy AND cheap) OR quick")
        env: Dictionary mapping variable names to boolean values
             Example: {"healthy": True, "cheap": False, "quick": True}
        
    Returns:
        The boolean result of evaluating the expression
        
    Raises:
        LogicEvalError: If the expression is invalid or contains unsupported operations
        
    Examples:
        eval_expr("A AND B", {"A": True, "B": False}) -> False
        eval_expr("A OR B", {"A": True, "B": False}) -> True
        eval_expr("NOT A", {"A": True}) -> False
    """
    # Normalize operators to Python-friendly syntax
    # Support special symbols: ∧ (AND), ∨ (OR), ¬ (NOT)
    expr = expr.replace('∧', ' and ').replace('∨', ' or ').replace('¬', ' not ')
    # Support uppercase versions too
    expr = expr.replace('AND', 'and').replace('OR', 'or').replace('NOT', 'not')
    
    try:
        # Parse the expression into an Abstract Syntax Tree (AST)
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise LogicEvalError(f"Syntax error: {e}")
    
    # Security check: validate that only safe operations are used
    # Block arithmetic, comparisons, function calls, etc.
    invalid_nodes = [ast.BinOp, ast.Compare, ast.Attribute, ast.Subscript, ast.Assign]
    
    # Also block number and string literals (for older Python versions)
    for legacy in ("Num", "Str"):
        legacy_type = getattr(ast, legacy, None)
        if legacy_type:
            invalid_nodes.append(legacy_type)
    
    # Scan the entire AST for forbidden node types
    for node in ast.walk(tree):
        if isinstance(node, tuple(invalid_nodes)):
            raise LogicEvalError("Only boolean expressions with variables, and/or/not, and parentheses are allowed")
    
    # Evaluate the validated expression
    return bool(_eval_node(tree, env))


def truth_table(expr: str, env_template: Dict[str, bool] = None) -> Tuple[List[str], List[Tuple[List[int], int]]]:
    """
    Generates a complete truth table for a boolean expression.
    
    A truth table shows the result of an expression for ALL possible combinations
    of True/False values for each variable.
    
    Args:
        expr: A boolean expression (e.g., "A AND B")
        env_template: Optional template dict (not typically used)
        
    Returns:
        A tuple of:
        - variables: Sorted list of variable names in the expression
        - rows: List of (values, result) tuples representing all combinations
                Each row is ([bit1, bit2, ...], result)
                Where 1=True, 0=False
    
    Example:
        truth_table("A AND B") returns:
        (
            ["A", "B"],
            [
                ([0, 0], 0),  # False AND False = False
                ([0, 1], 0),  # False AND True = False
                ([1, 0], 0),  # True AND False = False
                ([1, 1], 1)   # True AND True = True
            ]
        )
    """
    # Get all variables in the expression (sorted alphabetically)
    vars_ = parse_vars(expr)
    rows = []
    n = len(vars_)
    
    # Generate all possible combinations of True/False
    # Using a bitmask: 0 to 2^n - 1 (e.g., for 2 vars: 0,1,2,3 = 00,01,10,11 in binary)
    for mask in range(1 << n):
        # Create environment dictionary for this combination
        env = {}
        vals = []  # Track bit values for this combination
        
        # Extract bit values for each variable
        for i, v in enumerate(vars_):
            # Get the i-th bit from the mask
            bit = (mask >> (n - i - 1)) & 1
            env[v] = bool(bit)
            vals.append(bit)
        
        # Evaluate the expression with this combination
        res = 1 if eval_expr(expr, env) else 0
        rows.append((vals, res))
    
    return vars_, rows
