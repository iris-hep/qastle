from .parse import parse
from .transform import PythonASTToTextASTTransformer, TextASTToPythonASTTransformer

import ast


def text_ast_to_python_ast(text_ast):
    tree = parse(text_ast)
    return TextASTToPythonASTTransformer().transform(tree)


def python_ast_to_text_ast(python_ast):
    return PythonASTToTextASTTransformer().visit(python_ast)


def python_source_to_text_ast(python_source):
    python_ast = ast.parse(python_source)
    return PythonASTToTextASTTransformer().visit(python_ast)
