from .ast_util import unwrap_ast

import ast


class Select(ast.AST):
    def __init__(self, source, selector):
        self._fields = ['source', 'selector']
        self.source = source
        self.selector = selector


class InsertLINQNodesTransformer(ast.NodeTransformer):
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'Select':
            if len(node.args) != 1:
                raise SyntaxError('Select() call must have exactly one argument')
            if isinstance(node.args[0], ast.Str):
                node.args[0] = unwrap_ast(ast.parse(node.args[0].s))
            if not isinstance(node.args[0], ast.Lambda):
                raise SyntaxError('Select() call argument must be a lambda')
            return Select(source=node.func.value, selector=node.args[0])
        else:
            return self.generic_visit(node)


def insert_linq_nodes(python_ast):
    return InsertLINQNodesTransformer().visit(python_ast)


class RemoveLINQNodesTransformer(ast.NodeTransformer):
    pass


def remove_linq_nodes(python_ast):
    return RemoveLINQNodesTransformer().visit(python_ast)
