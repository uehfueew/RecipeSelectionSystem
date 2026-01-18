import ast
from typing import Dict, List, Tuple


class LogicEvalError(Exception):
    pass


def _collect_vars(node, vars_set: set):
    if isinstance(node, ast.Name):
        vars_set.add(node.id)
    for child in ast.iter_child_nodes(node):
        _collect_vars(child, vars_set)


def parse_vars(expr: str) -> List[str]:
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError:
        raise LogicEvalError("Invalid expression syntax")
    vars_set = set()
    _collect_vars(tree, vars_set)
    return sorted(vars_set)


def _eval_node(node, env: Dict[str, bool]):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, env)
    if isinstance(node, ast.Name):
        if node.id in env:
            return bool(env[node.id])
        raise LogicEvalError(f"Unknown variable: {node.id}")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not _eval_node(node.operand, env)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        raise LogicEvalError("Unsupported operator")
    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            return all(_eval_node(v, env) for v in node.values)
        if isinstance(node.op, ast.Or):
            return any(_eval_node(v, env) for v in node.values)
    if isinstance(node, ast.Call):
        raise LogicEvalError("Function calls not allowed")
    if isinstance(node, ast.Constant):
        return bool(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not _eval_node(node.operand, env)
    raise LogicEvalError(f"Unsupported AST node: {type(node)}")


def eval_expr(expr: str, env: Dict[str, bool]) -> bool:
    # normalize operators to python ast friendly words
    expr = expr.replace('∧', ' and ').replace('∨', ' or ').replace('¬', ' not ')
    expr = expr.replace('AND', 'and').replace('OR', 'or').replace('NOT', 'not')
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError:
        raise LogicEvalError("Invalid expression syntax")
    # validate AST
    invalid_nodes = [ast.BinOp, ast.Compare, ast.Attribute, ast.Subscript, ast.Assign]
    for legacy in ("Num", "Str"):
        legacy_type = getattr(ast, legacy, None)
        if legacy_type:
            invalid_nodes.append(legacy_type)
    for node in ast.walk(tree):
        if isinstance(node, tuple(invalid_nodes)):
            raise LogicEvalError("Only boolean expressions with variables, and/or/not, and parentheses are allowed")
    return bool(_eval_node(tree, env))


def truth_table(expr: str, env_template: Dict[str, bool] = None) -> Tuple[List[str], List[Tuple[List[int], int]]]:
    vars_ = parse_vars(expr)
    rows = []
    n = len(vars_)
    for mask in range(1 << n):
        env = {}
        vals = []
        for i, v in enumerate(vars_):
            bit = (mask >> (n - i - 1)) & 1
            env[v] = bool(bit)
            vals.append(bit)
        res = 1 if eval_expr(expr, env) else 0
        rows.append((vals, res))
    return vars_, rows
