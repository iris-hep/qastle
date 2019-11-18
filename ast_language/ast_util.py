import ast
import sys


def unwrap_ast(module_node):
    if len(module_node.body) == 0:
        return None
    else:
        expr_node = module_node.body[0]
        return expr_node.value


def wrap_ast(node=None):
    if node is None:
        body_list = []
    else:
        expr_node = ast.Expr(value=node)
        body_list = [expr_node]
    if sys.version_info[0] < 3 or sys.version_info[0] == 3 and sys.version_info[1] < 8:
        module_node = ast.Module(body=body_list)
    else:
        module_node = ast.Module(body=body_list, type_ignores=[])
    return module_node
