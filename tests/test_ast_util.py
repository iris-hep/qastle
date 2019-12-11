from .testing_util import *

from qastle import *

import ast


def test_unwrap_ast():
    assert unwrap_ast(ast.parse('')) is None
    parsed_node = ast.parse('a')
    name_node = ast.Name(id='a', ctx=ast.Load())
    assert_ast_nodes_are_equal(unwrap_ast(parsed_node), name_node)


def test_wrap_ast():
    assert_ast_nodes_are_equal(wrap_ast(), ast.parse(''))
    assert_ast_nodes_are_equal(wrap_ast(None), ast.parse(''))
    parsed_node = ast.parse('a')
    name_node = ast.Name(id='a', ctx=ast.Load())
    assert_ast_nodes_are_equal(wrap_ast(name_node), parsed_node)
