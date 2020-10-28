from .linq_util import Where, Select, SelectMany, First, Aggregate, Count, Max, Min, Sum
from .ast_util import wrap_ast, unwrap_ast

import lark

import ast
import sys


UnaryOp_ops = {'+':   ast.UAdd,
               '-':   ast.USub,
               'not': ast.Not,
               '~':   ast.Invert}

BinOp_ops = {'+': ast.Add,
             '-': ast.Sub,
             '*': ast.Mult,
             '/': ast.Div,
             '%': ast.Mod,
             '**': ast.Pow,
             '//': ast.FloorDiv,
             '&': ast.BitAnd,
             '|': ast.BitOr,
             '^': ast.BitXor,
             '<<': ast.LShift,
             '>>': ast.RShift}

BoolOp_ops = {'and': ast.And,
              'or':  ast.Or}

Compare_ops = {'==': ast.Eq,
               '!=': ast.NotEq,
               '<':  ast.Lt,
               '<=': ast.LtE,
               '>':  ast.Gt,
               '>=': ast.GtE}

op_strings = {value: key
              for dictionary in [UnaryOp_ops, BinOp_ops, BoolOp_ops, Compare_ops]
              for key, value in dictionary.items()}

flexible_ops = ('+', '-')


class PythonASTToTextASTTransformer(ast.NodeVisitor):
    def visit_Module(self, node):
        n_children = len(node.body)
        if n_children == 0:
            return ''
        elif n_children == 1:
            return self.visit(node.body[0])
        else:
            raise SyntaxError('A record must contain zero or one expressions; found '
                              + str(n_children))

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Name(self, node):
        return node.id

    def visit_Constant(self, node):
        return repr(node.value)

    def visit_Num(self, node):
        return repr(node.n)

    def visit_Str(self, node):
        return repr(node.s)

    def visit_NameConstant(self, node):
        return repr(node.value)

    @staticmethod
    def make_composite_node_string(node_type, *fields):
        return '(' + node_type + ''.join([' ' + field for field in fields]) + ')'

    def visit_List(self, node):
        return self.make_composite_node_string('list',
                                               *[self.visit(element) for element in node.elts])

    def visit_Tuple(self, node):
        return self.visit_List(node)

    def visit_Dict(self, node):
        return self.make_composite_node_string('dict',
                                               self.visit(ast.List(elts=node.keys)),
                                               self.visit(ast.List(elts=node.values)))

    def visit_Attribute(self, node):
        return self.make_composite_node_string('attr', self.visit(node.value), repr(node.attr))

    def visit_Subscript(self, node):
        return self.make_composite_node_string('subscript',
                                               self.visit(node.value),
                                               self.visit(node.slice))

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Call(self, node):
        return self.make_composite_node_string('call',
                                               self.visit(node.func),
                                               *[self.visit(arg) for arg in node.args])

    def visit_IfExp(self, node):
        return self.make_composite_node_string('if',
                                               self.visit(node.test),
                                               self.visit(node.body),
                                               self.visit(node.orelse))

    def visit_UnaryOp(self, node):
        if (hasattr(ast, 'Constant') and isinstance(node.operand, ast.Constant)
           or isinstance(node.operand, ast.Num)):
            if isinstance(node.op, ast.UAdd):
                return self.visit(node.operand)
            elif isinstance(node.op, ast.USub):
                return self.visit(ast.Num(n=-node.operand.n))
        return self.make_composite_node_string(op_strings[type(node.op)],
                                               self.visit(node.operand))

    def visit_BinOp(self, node):
        return self.make_composite_node_string(op_strings[type(node.op)],
                                               self.visit(node.left),
                                               self.visit(node.right))

    def visit_BoolOp(self, node):
        if len(node.values) < 2:
            raise SyntaxError('Boolean operator must have at least 2 operands; found: '
                              + str(len(node.values)))
        rep = self.visit(node.values[0])
        for value in node.values[1:]:
            rep = self.make_composite_node_string(op_strings[type(node.op)],
                                                  rep,
                                                  self.visit(value))
        return rep

    def visit_Compare(self, node):
        if len(node.ops) < 1:
            raise SyntaxError('Compare node must have at least 1 operation; found: '
                              + str(len(node.ops)))
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        rep = self.make_composite_node_string(op_strings[type(node.ops[0])],
                                              left,
                                              right)
        for operator, comparator in zip(node.ops[1:], node.comparators[1:]):
            left = right
            right = self.visit(comparator)
            new_comparison = self.make_composite_node_string(op_strings[type(operator)],
                                                             left,
                                                             right)
            rep = self.make_composite_node_string('and', rep, new_comparison)
        return rep

    def visit_Lambda(self, node):
        return self.make_composite_node_string('lambda',
                                               self.visit(node.args),
                                               self.visit(node.body))

    def visit_arguments(self, node):
        return self.visit(ast.List(elts=node.args))

    def visit_arg(self, node):
        return node.arg

    def visit_Where(self, node):
        return self.make_composite_node_string('Where',
                                               self.visit(node.source),
                                               self.visit(node.predicate))

    def visit_Select(self, node):
        return self.make_composite_node_string('Select',
                                               self.visit(node.source),
                                               self.visit(node.selector))

    def visit_SelectMany(self, node):
        return self.make_composite_node_string('SelectMany',
                                               self.visit(node.source),
                                               self.visit(node.selector))

    def visit_First(self, node):
        return self.make_composite_node_string('First', self.visit(node.source))

    def visit_Aggregate(self, node):
        return self.make_composite_node_string('Aggregate',
                                               self.visit(node.source),
                                               self.visit(node.seed),
                                               self.visit(node.func))

    def visit_Count(self, node):
        return self.make_composite_node_string('Count', self.visit(node.source))

    def visit_Max(self, node):
        return self.make_composite_node_string('Max', self.visit(node.source))

    def visit_Min(self, node):
        return self.make_composite_node_string('Min', self.visit(node.source))

    def visit_Sum(self, node):
        return self.make_composite_node_string('Sum', self.visit(node.source))

    def generic_visit(self, node):
        raise SyntaxError('Unsupported node type: ' + str(type(node)))


class TextASTToPythonASTTransformer(lark.Transformer):
    def record(self, children):
        if (len(children) == 0
           or isinstance(children[0], lark.Token) and children[0].type == 'WHITESPACE'):
            return wrap_ast()
        else:
            return wrap_ast(children[0])

    def expression(self, children):
        for child in children:
            if not (isinstance(child, lark.Token) and child.type == 'WHITESPACE'):
                return child
        raise SyntaxError('Expression does not contain a node')

    def atom(self, children):
        child = children[0]
        if child.type == 'NUMERIC_LITERAL':
            if child.value[0] == '+':
                child.value = child.value[1:]
        return unwrap_ast(ast.parse(child.value))

    def composite(self, children):
        fields = []
        for child in children:
            if isinstance(child, lark.Token):
                if child.type == 'NODE_TYPE':
                    node_type = child.value
                else:
                    pass
            elif isinstance(child, ast.AST):
                fields.append(child)
            else:
                pass

        if node_type == 'list':
            return ast.List(elts=fields, ctx=ast.Load())

        if node_type == 'dict':
            if len(fields) != 2:
                raise SyntaxError('Dictionary node must have two fields; found '
                                  + str(len(fields)))
            for field_index in range(2):
                if not isinstance(fields[field_index], ast.List):
                    raise SyntaxError('Dictionary fields must be lists; found '
                                      + str(type(fields[field_index])))
            return ast.Dict(keys=fields[0].elts, values=fields[1].elts)

        elif node_type == 'attr':
            if len(fields) != 2:
                raise SyntaxError('Attribute node must have two fields; found ' + str(len(fields)))
            if not isinstance(fields[1], ast.Str):
                raise SyntaxError('Attribute name must be a string; found ' + str(type(fields[1])))
            return ast.Attribute(value=fields[0], attr=fields[1].s, ctx=ast.Load())

        elif node_type == 'subscript':
            if len(fields) != 2:
                raise SyntaxError('Subscript node must have two fields; found ' + str(len(fields)))
            if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 9):
                return ast.Subscript(value=fields[0],
                                     slice=ast.Index(value=fields[1]),
                                     ctx=ast.Load())
            else:
                return ast.Subscript(value=fields[0], slice=fields[1], ctx=ast.Load())

        elif node_type == 'call':
            if len(fields) < 1:
                raise SyntaxError('Call node must have at least one field; found '
                                  + str(len(fields)))
            if sys.version_info[0] < 3:
                return ast.Call(func=fields[0],
                                args=fields[1:],
                                keywords=[],
                                starargs=None,
                                kwargs=None)
            else:
                return ast.Call(func=fields[0], args=fields[1:], keywords=[])

        elif node_type == 'if':
            if len(fields) != 3:
                raise SyntaxError('If node must have three fields; found '
                                  + str(len(fields)))
            return ast.IfExp(test=fields[0], body=fields[1], orelse=fields[2])

        elif node_type in UnaryOp_ops:
            if len(fields) == 1:
                return ast.UnaryOp(op=UnaryOp_ops[node_type](), operand=fields[0])
            elif node_type not in flexible_ops:
                raise SyntaxError(UnaryOp_ops[node_type].__name__
                                  + ' operator only supported for one operand; found '
                                  + str(len(fields)))

        if node_type in BinOp_ops:
            if len(fields) == 2:
                return ast.BinOp(left=fields[0], op=BinOp_ops[node_type](), right=fields[1])
            else:
                raise SyntaxError(BinOp_ops[node_type].__name__
                                  + ' operator only supported for two operands; found '
                                  + str(len(fields)))

        elif node_type in BoolOp_ops:
            if len(fields) == 2:
                return ast.BoolOp(op=BoolOp_ops[node_type](), values=fields)
            else:
                raise SyntaxError(BoolOp_ops[node_type].__name__
                                  + ' operator only supported for two operands; found '
                                  + str(len(fields)))

        elif node_type in Compare_ops:
            if len(fields) == 2:
                return ast.Compare(left=fields[0],
                                   ops=[Compare_ops[node_type]()],
                                   comparators=[fields[1]])
            else:
                raise SyntaxError(Compare_ops[node_type].__name__
                                  + ' operator only supported for two operands; found '
                                  + str(len(fields)))

        elif node_type == 'lambda':
            if len(fields) != 2:
                raise SyntaxError('Lambda node must have two fields; found ' + str(len(fields)))
            if not isinstance(fields[0], ast.List):
                raise SyntaxError('Lambda arguments must be in a list; found '
                                  + str(type(fields[0])))
            for arg in fields[0].elts:
                if not isinstance(arg, ast.Name):
                    raise SyntaxError('Lambda arguments must variable names; found '
                                      + str(type(arg)))
            if sys.version_info[0] < 3:
                return ast.Lambda(args=ast.arguments(args=[ast.Name(id=name.id, ctx=ast.Param())
                                                           for name in fields[0].elts],
                                                     vararg=None,
                                                     kwarg=None,
                                                     defaults=[]),
                                  body=fields[1])
            elif sys.version_info[0] == 3 and sys.version_info[1] < 8:
                return ast.Lambda(args=ast.arguments(args=[ast.arg(arg=name.id, annotation=None)
                                                           for name in fields[0].elts],
                                                     vararg=None,
                                                     kwonlyargs=[],
                                                     kw_defaults=[],
                                                     kwarg=None,
                                                     defaults=[]),
                                  body=fields[1])
            else:
                return ast.Lambda(args=ast.arguments(posonlyargs=[],
                                                     args=[ast.arg(arg=name.id,
                                                                   annotation=None,
                                                                   type_comment=None)
                                                           for name in fields[0].elts],
                                                     vararg=None,
                                                     kwonlyargs=[],
                                                     kw_defaults=[],
                                                     kwarg=None,
                                                     defaults=[]),
                                  body=fields[1])

        elif node_type == 'Where':
            if len(fields) != 2:
                raise SyntaxError('Where node must have two fields; found ' + str(len(fields)))
            if not isinstance(fields[1], ast.Lambda):
                raise SyntaxError('Where predicate must be a lambda; found '
                                  + str(type(fields[1])))
            if len(fields[1].args.args) != 1:
                raise SyntaxError('Where predicate must have exactly one argument; found '
                                  + str(len(fields[1].args.args)))
            return Where(source=fields[0], predicate=fields[1])

        elif node_type == 'Select':
            if len(fields) != 2:
                raise SyntaxError('Select node must have two fields; found ' + str(len(fields)))
            if not isinstance(fields[1], ast.Lambda):
                raise SyntaxError('Select selector must be a lambda; found '
                                  + str(type(fields[1])))
            if len(fields[1].args.args) != 1:
                raise SyntaxError('Select selector must have exactly one argument; found '
                                  + str(len(fields[1].args.args)))
            return Select(source=fields[0], selector=fields[1])

        elif node_type == 'SelectMany':
            if len(fields) != 2:
                raise SyntaxError('SelectMany node must have two fields; found '
                                  + str(len(fields)))
            if not isinstance(fields[1], ast.Lambda):
                raise SyntaxError('SelectMany selector must be a lambda; found '
                                  + str(type(fields[1])))
            if len(fields[1].args.args) != 1:
                raise SyntaxError('SelectMany selector must have exactly one argument; found '
                                  + str(len(fields[1].args.args)))
            return SelectMany(source=fields[0], selector=fields[1])

        elif node_type == 'First':
            if len(fields) != 1:
                raise SyntaxError('First node must have one field; found ' + str(len(fields)))
            return First(source=fields[0])

        elif node_type == 'Aggregate':
            if len(fields) != 3:
                raise SyntaxError('Aggregate node must have three fields; found '
                                  + str(len(fields)))
            if not isinstance(fields[2], ast.Lambda):
                raise SyntaxError('Aggregate func must be a lambda; found ' + str(type(fields[1])))
            if len(fields[2].args.args) != 2:
                raise SyntaxError('Aggregate func must have exactly two arguments; found '
                                  + str(len(fields[2].args.args)))
            return Aggregate(source=fields[0], seed=fields[1], func=fields[2])

        elif node_type == 'Count':
            if len(fields) != 1:
                raise SyntaxError('Count node must have one field; found ' + str(len(fields)))
            return Count(source=fields[0])

        elif node_type == 'Max':
            if len(fields) != 1:
                raise SyntaxError('Max node must have one field; found ' + str(len(fields)))
            return Max(source=fields[0])

        elif node_type == 'Min':
            if len(fields) != 1:
                raise SyntaxError('Min node must have one field; found ' + str(len(fields)))
            return Min(source=fields[0])

        elif node_type == 'Sum':
            if len(fields) != 1:
                raise SyntaxError('Sum node must have one field; found ' + str(len(fields)))
            return Sum(source=fields[0])

        else:
            raise SyntaxError('Unknown composite node type: ' + node_type)
