import ast


def unwrap_ast(module_node):
    expr_node = module_node.body[0]
    return expr_node.value


def wrap_ast(node):
    expr_node = ast.Expr(value=node)
    module_node = ast.Module(body=[expr_node])
    return module_node
