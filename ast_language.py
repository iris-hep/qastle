import lark

import ast
import os

grammar_pathname = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'grammar.lark')

with open(grammar_pathname) as grammar_file:
  parser = lark.Lark(grammar_file.read(), start='record')

class TextASTToPythonAST(lark.Transformer):
  def record(self, children):
    if len(children) == 0 or isinstance(children[0], lark.Token) and children[0].type == 'WHITESPACE':
      return ast.Module(body=[])
    return ast.Module(body=[ast.Expr(value=children[0])])

  def expression(self, children):
    for child in children:
      if not (isinstance(child, lark.Token) and child.type == 'WHITESPACE'):
        return child
    raise SyntaxError('Expression does not contain a node')

  def atom(self, children):
    child = children[0]
    if child.type == 'IDENTIFIER':
      return ast.Name(id=child.value, ctx=ast.Load())
    elif child.type == 'STRING_LITERAL':
      return ast.Str(s=ast.literal_eval(child.value))
    elif child.type == 'NUMERIC_LITERAL':
      return ast.Num(n=ast.literal_eval(child.value))
    else:
      raise Exception("Unknown atom child type")

  #def composite(self, children):

class PythonASTToTextAST(ast.NodeVisitor):
  def visit_Module(self, node):
    n_children = len(node.body)
    if n_children == 0:
      return '';
    elif n_children == 1:
      return self.visit(node.body[0])
    else:
      raise SyntaxError('A record must contain zero or one expressions; found ' + str(n_children))

  def visit_Expr(self, node):
    return self.visit(node.value)

  def visit_Name(self, node):
    return node.id

  def visit_Num(self, node):
    return repr(node.n)

  def visit_Str(self, node):
    return repr(node.s)

def text_ast_to_python_ast(text_ast):
  tree = parser.parse(text_ast)
  return TextASTToPythonAST().transform(tree)

def python_ast_to_text_ast(python_ast):
  return PythonASTToTextAST().visit(python_ast)
