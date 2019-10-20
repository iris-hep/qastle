from .transform import PythonASTToTextASTTransformer, TextASTToPythonASTTransformer
from .parse import parse

import ast


def python_source_to_python_ast(python_source):
    return ast.parse(python_source)


def python_source_to_text_ast(python_source):
    python_ast = python_source_to_python_ast(python_source)
    return python_ast_to_text_ast(python_ast)


def python_ast_to_text_ast(python_ast):
    return PythonASTToTextASTTransformer().visit(python_ast)


def text_ast_to_python_ast(text_ast):
    tree = parse(text_ast)
    return TextASTToPythonASTTransformer().transform(tree)
