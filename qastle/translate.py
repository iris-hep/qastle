from .transform import PythonASTToTextASTTransformer, TextASTToPythonASTTransformer
from .parse import parse

import ast


def python_source_to_python_ast(python_source):
    return ast.parse(python_source)


def python_source_to_text_ast(python_source):
    python_ast = python_source_to_python_ast(python_source)
    return python_ast_to_text_ast(python_ast)


def python_ast_to_text_ast(python_ast):
    """
    Create a qastle text AST from a native Python AST

    Parameters
    ----------
    python_ast : ast.AST
        Python AST to translate

    Returns
    -------
    str
        Translated qastle AST as a text string
    """
    return PythonASTToTextASTTransformer().visit(python_ast)


def text_ast_to_python_ast(text_ast):
    """
    Create a native Python AST from a qastle text AST

    Parameters
    ----------
    test_ast : str
        qastle AST to translate

    Returns
    -------
    ast.AST
        Translated Python AST
    """
    tree = parse(text_ast)
    return TextASTToPythonASTTransformer().transform(tree)
