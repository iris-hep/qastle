from .testing_util import *

from qastle import *

import ast


def test_insert_linq_nodes():
    initial_ast = ast.parse("the_source.Select('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Select(source=unwrap_ast(ast.parse('the_source')),
                                   selector=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)
