import lark
import ast

grammar_file_pathname = 'grammar.lark'

with open(grammar_file_pathname) as grammar_file:
  parser = lark.Lark(grammar_file.read(), start='expression')

class Transformer(lark.Transformer):
  def expression(self, expression_tree):
    for element in expression_tree:
      if isinstance(element, lark.Token) and element.type == 'WHITESPACE':
        pass
      else:
        return ast.Module(body=[ast.Expr(value=element)])

  def atom(self, atom_tree):
    token = atom_tree[0]
    if token.type == 'NUMERIC_LITERAL':
      return ast.Num(n=ast.literal_eval(token.value))
    elif token.type == 'STRING_LITERAL':
      return ast.Str(s=ast.literal_eval(token.value))
    elif token.type == 'NAME':
      return ast.Name(id=token.value, ctx=ast.Load())
    else:
      raise Exception("Unknown atom token type")

  def composite(self, composite_tree):
    return composite_tree
