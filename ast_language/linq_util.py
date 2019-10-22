from .ast_util import unwrap_ast

import ast


class Where(ast.AST):
    def __init__(self, source, predicate):
        self._fields = ['source', 'predicate']
        self.source = source
        self.predicate = predicate


class Select(ast.AST):
    def __init__(self, source, selector):
        self._fields = ['source', 'selector']
        self.source = source
        self.selector = selector


class SelectMany(ast.AST):
    def __init__(self, source, selector):
        self._fields = ['source', 'selector']
        self.source = source
        self.selector = selector


class First(ast.AST):
    def __init__(self, source):
        self._fields = ['source']
        self.source = source


class InsertLINQNodesTransformer(ast.NodeTransformer):
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == 'Where':
                if len(node.args) != 1:
                    raise SyntaxError('Where() call must have exactly one argument')
                if isinstance(node.args[0], ast.Str):
                    node.args[0] = unwrap_ast(ast.parse(node.args[0].s))
                if not isinstance(node.args[0], ast.Lambda):
                    raise SyntaxError('Where() call argument must be a lambda')
                return Where(source=node.func.value, predicate=node.args[0])
            elif node.func.attr == 'Select':
                if len(node.args) != 1:
                    raise SyntaxError('Select() call must have exactly one argument')
                if isinstance(node.args[0], ast.Str):
                    node.args[0] = unwrap_ast(ast.parse(node.args[0].s))
                if not isinstance(node.args[0], ast.Lambda):
                    raise SyntaxError('Select() call argument must be a lambda')
                return Select(source=node.func.value, selector=node.args[0])
            elif node.func.attr == 'SelectMany':
                if len(node.args) != 1:
                    raise SyntaxError('SelectMany() call must have exactly one argument')
                if isinstance(node.args[0], ast.Str):
                    node.args[0] = unwrap_ast(ast.parse(node.args[0].s))
                if not isinstance(node.args[0], ast.Lambda):
                    raise SyntaxError('SelectMany() call argument must be a lambda')
                return SelectMany(source=node.func.value, selector=node.args[0])
            elif node.func.attr == 'First':
                if len(node.args) != 0:
                    raise SyntaxError('First() call must have zero arguments')
                return First(source=node.func.value)
            else:
                return self.generic_visit(node)
        else:
            return self.generic_visit(node)


def insert_linq_nodes(python_ast):
    return InsertLINQNodesTransformer().visit(python_ast)


class RemoveLINQNodesTransformer(ast.NodeTransformer):
    pass


def remove_linq_nodes(python_ast):
    return RemoveLINQNodesTransformer().visit(python_ast)
