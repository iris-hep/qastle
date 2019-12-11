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
                return Where(source=self.visit(node.func.value),
                             predicate=self.visit(node.args[0]))
            elif node.func.attr == 'Select':
                if len(node.args) != 1:
                    raise SyntaxError('Select() call must have exactly one argument')
                if isinstance(node.args[0], ast.Str):
                    node.args[0] = unwrap_ast(ast.parse(node.args[0].s))
                if not isinstance(node.args[0], ast.Lambda):
                    raise SyntaxError('Select() call argument must be a lambda')
                return Select(source=self.visit(node.func.value),
                              selector=self.visit(node.args[0]))
            elif node.func.attr == 'SelectMany':
                if len(node.args) != 1:
                    raise SyntaxError('SelectMany() call must have exactly one argument')
                if isinstance(node.args[0], ast.Str):
                    node.args[0] = unwrap_ast(ast.parse(node.args[0].s))
                if not isinstance(node.args[0], ast.Lambda):
                    raise SyntaxError('SelectMany() call argument must be a lambda')
                return SelectMany(source=self.visit(node.func.value),
                                  selector=self.visit(node.args[0]))
            elif node.func.attr == 'First':
                if len(node.args) != 0:
                    raise SyntaxError('First() call must have zero arguments')
                return First(source=self.visit(node.func.value))
            elif node.func.attr == 'Aggregate':
                if len(node.args) != 2:
                    raise SyntaxError('Aggregate() call must have exactly two arguments; found'
                                      + str(len(node.args)))
                if isinstance(node.args[1], ast.Str):
                    node.args[0] = unwrap_ast(ast.parse(node.args[0].s))
                if not isinstance(node.args[1], ast.Lambda):
                    raise SyntaxError('Second Aggregate() call argument must be a lambda')
                return Aggregate(source=self.visit(node.func.value),
                                 seed=self.visit(node.args[0]),
                                 func=self.visit(node.args[1]))
            elif node.func.attr == 'Count':
                if len(node.args) != 0:
                    raise SyntaxError('Count() call must have zero arguments')
                return Count(source=self.visit(node.func.value))
            elif node.func.attr == 'Max':
                if len(node.args) != 0:
                    raise SyntaxError('Max() call must have zero arguments')
                return Max(source=self.visit(node.func.value))
            elif node.func.attr == 'Min':
                if len(node.args) != 0:
                    raise SyntaxError('Min() call must have zero arguments')
                return Min(source=self.visit(node.func.value))
            elif node.func.attr == 'Sum':
                if len(node.args) != 0:
                    raise SyntaxError('Sum() call must have zero arguments')
                return Sum(source=self.visit(node.func.value))
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
