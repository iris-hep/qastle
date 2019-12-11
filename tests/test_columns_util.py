from .testing_util import *

from qastle import *

import ast


def test_remove_source():
    initial_node = ast.Attribute(value=ast.Name(id='a_source_name', ctx=ast.Load()),
                                 attr='not_the_source',
                                 ctx=ast.Load())
    final_node = remove_source(initial_node, 'a_source_name')
    assert_ast_nodes_are_equal(final_node, ast.Name(id='not_the_source', ctx=ast.Load()))


def test_python_ast_to_columns():
    node = wrap_ast(Select(source=unwrap_ast(ast.parse('the_source')),
                           selector=unwrap_ast(ast.parse('lambda row:\
                                                          (row.collection_i.column_1(),\
                                                           row.collection_ii.column_2())'))))
    assert python_ast_to_columns(node) == 'collection_i.column_1(), collection_ii.column_2()'
