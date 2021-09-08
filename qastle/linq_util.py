from .ast_util import unwrap_ast

import ast


class Where(ast.AST):
    _fields = ['source', 'predicate']


class Select(ast.AST):
    _fields = ['source', 'selector']


class SelectMany(ast.AST):
    _fields = ['source', 'selector']


class First(ast.AST):
    _fields = ['source']


class Last(ast.AST):
    _fields = ['source']


class Aggregate(ast.AST):
    _fields = ['source', 'seed', 'func']


class Count(ast.AST):
    _fields = ['source']


class Max(ast.AST):
    _fields = ['source']


class Min(ast.AST):
    _fields = ['source']


class Sum(ast.AST):
    _fields = ['source']


class Zip(ast.AST):
    _fields = ['source']


class OrderBy(ast.AST):
    _fields = ['source', 'key_selector']


class Choose(ast.AST):
    _fields = ['source', 'n']


linq_operator_names = ('Where',
                       'Select',
                       'SelectMany',
                       'First',
                       'Last',
                       'Aggregate',
                       'Count',
                       'Max',
                       'Min',
                       'Sum',
                       'Zip',
                       'OrderBy',
                       'Choose')


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
            if len(node.args) == 0:
                raise SyntaxError('LINQ operators must specify a data source to operate on')
            source = node.args[0]
            args = node.args[1:]
        else:
            return self.generic_visit(node)

        if function_name == 'Where':
            if len(args) != 1:
                raise SyntaxError('Where() call must have exactly one argument')
            if isinstance(args[0], ast.Str):
                args[0] = unwrap_ast(ast.parse(args[0].s))
            if not isinstance(args[0], ast.Lambda):
                raise SyntaxError('Where() call argument must be a lambda')
            return Where(source=self.visit(source),
                         predicate=self.visit(args[0]))
        elif function_name == 'Select':
            if len(args) != 1:
                raise SyntaxError('Select() call must have exactly one argument')
            if isinstance(args[0], ast.Str):
                args[0] = unwrap_ast(ast.parse(args[0].s))
            if not isinstance(args[0], ast.Lambda):
                raise SyntaxError('Select() call argument must be a lambda')
            return Select(source=self.visit(source),
                          selector=self.visit(args[0]))
        elif function_name == 'SelectMany':
            if len(args) != 1:
                raise SyntaxError('SelectMany() call must have exactly one argument')
            if isinstance(args[0], ast.Str):
                args[0] = unwrap_ast(ast.parse(args[0].s))
            if not isinstance(args[0], ast.Lambda):
                raise SyntaxError('SelectMany() call argument must be a lambda')
            return SelectMany(source=self.visit(source),
                              selector=self.visit(args[0]))
        elif function_name == 'First':
            if len(args) != 0:
                raise SyntaxError('First() call must have zero arguments')
            return First(source=self.visit(source))
        elif function_name == 'Last':
            if len(args) != 0:
                raise SyntaxError('Last() call must have zero arguments')
            return Last(source=self.visit(source))
        elif function_name == 'Aggregate':
            if len(args) != 2:
                raise SyntaxError('Aggregate() call must have exactly two arguments; found'
                                  + str(len(args)))
            if isinstance(args[1], ast.Str):
                args[1] = unwrap_ast(ast.parse(args[1].s))
            if not isinstance(args[1], ast.Lambda):
                raise SyntaxError('Second Aggregate() call argument must be a lambda')
            return Aggregate(source=self.visit(source),
                             seed=self.visit(args[0]),
                             func=self.visit(args[1]))
        elif function_name == 'Count':
            if len(args) != 0:
                raise SyntaxError('Count() call must have zero arguments')
            return Count(source=self.visit(source))
        elif function_name == 'Max':
            if len(args) != 0:
                raise SyntaxError('Max() call must have zero arguments')
            return Max(source=self.visit(source))
        elif function_name == 'Min':
            if len(args) != 0:
                raise SyntaxError('Min() call must have zero arguments')
            return Min(source=self.visit(source))
        elif function_name == 'Sum':
            if len(args) != 0:
                raise SyntaxError('Sum() call must have zero arguments')
            return Sum(source=self.visit(source))
        elif function_name == 'Zip':
            if len(args) != 0:
                raise SyntaxError('Zip() call must have zero arguments')
            return Zip(source=self.visit(source))
        elif function_name == 'OrderBy':
            if len(args) != 1:
                raise SyntaxError('OrderBy() call must have exactly one argument')
            if isinstance(args[0], ast.Str):
                args[0] = unwrap_ast(ast.parse(args[0].s))
            if not isinstance(args[0], ast.Lambda):
                raise SyntaxError('OrderBy() call argument must be a lambda')
            return OrderBy(source=self.visit(source),
                           key_selector=self.visit(args[0]))
        elif function_name == 'Choose':
            if len(args) != 1:
                raise SyntaxError('Choose() call must have exactly one argument')
            return Choose(source=self.visit(source), n=self.visit(args[0]))
        else:
            raise NameError('Unhandled LINQ operator: ' + function_name)


def insert_linq_nodes(python_ast):
    return InsertLINQNodesTransformer().visit(python_ast)


class RemoveLINQNodesTransformer(ast.NodeTransformer):
    pass


def remove_linq_nodes(python_ast):
    return RemoveLINQNodesTransformer().visit(python_ast)
