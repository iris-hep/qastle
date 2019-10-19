import ast


def unwrap_ast(module_node):
    if len(module_node.body) == 0:
        return None
    else:
        expr_node = module_node.body[0]
        return expr_node.value


def wrap_ast(node=None):
    if node is None:
        module_node = ast.Module(body=[])
    else:
        expr_node = ast.Expr(value=node)
        module_node = ast.Module(body=[expr_node])
    return module_node
