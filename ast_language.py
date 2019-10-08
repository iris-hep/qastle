import lark

import ast

grammar_pathname = 'grammar.lark'

with open(grammar_pathname) as grammar_file:
  parser = lark.Lark(grammar_file.read(), start='record')

class TextToPython(lark.Transformer):
  def record(self, record_tree):
    if len(record_tree) == 0 or isinstance(record[0], lark.Token) and record[0].type == 'WHITESPACE':
      return ast.Module(body=[])
    else:
      return ast.Module(body=[ast.Expr(value=record[0])])

  def expression(self, expression_tree):
    for element in expression_tree:
      if isinstance(element, lark.Token) and element.type == 'WHITESPACE':
        pass
      else:
        return element

  def atom(self, atom_tree):
    token = atom_tree[0]
    if token.type == 'NAME':
      return ast.Name(id=token.value, ctx=ast.Load())
    elif token.type == 'NUMERIC_LITERAL':
      return ast.Num(n=ast.literal_eval(token.value))
    elif token.type == 'STRING_LITERAL':
      return ast.Str(s=ast.literal_eval(token.value))
    else:
      raise Exception("Unknown atom token type")

  def composite(self, composite_tree):
    return composite_tree

class PythonToText(ast.NodeVisitor):
  def visit_Module(self, node):
    return '\n'.join([self.visit(child_node) for child_node in node.body])

  def visit_Expr(self, node):
    return self.visit(node.value)

  def visit_Name(self, node):
    return node.id

  def visit_Num(self, node):
    return repr(node.n)

  def visit_Str(self, node):
    return repr(node.s)
