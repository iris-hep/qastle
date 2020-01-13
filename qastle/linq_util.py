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


class Aggregate(ast.AST):
    def __init__(self, source, seed, func):
        self._fields = ['source', 'seed', 'func']
        self.source = source
        self.seed = seed
        self.func = func


class Count(ast.AST):
    def __init__(self, source):
        self._fields = ['source']
        self.source = source


class Max(ast.AST):
    def __init__(self, source):
        self._fields = ['source']
        self.source = source


class Min(ast.AST):
    def __init__(self, source):
        self._fields = ['source']
        self.source = source


class Sum(ast.AST):
    def __init__(self, source):
        self._fields = ['source']
        self.source = source


linq_operator_names = ('Where',
                       'Select',
                       'SelectMany',
                       'First',
                       'Aggregate',
                       'Count',
                       'Max',
                       'Min',
                       'Sum')


class InsertLINQNodesTransformer(ast.NodeTransformer):
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            function_name = node.func.attr
            if function_name not in linq_operator_names:
                return self.generic_visit(node)
            source = node.func.value
            args = node.args
        elif isinstance(node.func, ast.Name):
            function_name = node.func.id
            if function_name not in linq_operator_names:
                return self.generic_visit(node)
            source = node.args[0]
            args = node.args[1:]
        if function_name in ('Where', 'Select', 'SelectMany') and isinstance(args[0], ast.Str):
            args[0] = unwrap_ast(ast.parse(node.args[0].s))
        elif function_name == 'Aggregate' and isinstance(args[1], ast.Str):
            args[1] = unwrap_ast(ast.parse(args[1].s))
        source = self.visit(source)
        args = [self.visit(arg) for arg in args]
        return globals()[function_name](source, *args)


def insert_linq_nodes(python_ast):
    return InsertLINQNodesTransformer().visit(python_ast)


class RemoveLINQNodesTransformer(ast.NodeTransformer):
    pass


def remove_linq_nodes(python_ast):
    return RemoveLINQNodesTransformer().visit(python_ast)
