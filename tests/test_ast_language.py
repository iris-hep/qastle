from .testing_util import *

from ast_language import *

import ast


def assert_identical_atom(initial_text):
    initial_python_ast = ast.parse(initial_text)
    final_text_ast = python_ast_to_text_ast(initial_python_ast)
    assert final_text_ast == initial_text.strip(' \t\r\n')
    final_python_ast = text_ast_to_python_ast(initial_text)
    assert_ast_nodes_are_equal(final_python_ast, initial_python_ast)


def assert_equivalent_literal(initial_text):
    initial_python_ast = ast.parse(initial_text)
    final_text_ast = python_ast_to_text_ast(initial_python_ast)
    assert ast.literal_eval(final_text_ast) == ast.literal_eval(initial_text)
    final_python_ast = text_ast_to_python_ast(initial_text)
    assert_ast_nodes_are_equal(final_python_ast, initial_python_ast)


def assert_equivalent_python_ast_and_text_ast(initial_python_ast, initial_text_ast):
    final_text_ast = python_ast_to_text_ast(initial_python_ast)
    assert final_text_ast == initial_text_ast
    final_python_ast = text_ast_to_python_ast(initial_text_ast)
    assert_ast_nodes_are_equal(final_python_ast, initial_python_ast)


def assert_equivalent_python_text_and_text_ast(python_text, initial_text_ast):
    initial_python_ast = ast.parse(python_text)
    assert_equivalent_python_ast_and_text_ast(initial_python_ast, initial_text_ast)


def test_empty():
    assert_identical_atom('')


def test_whitespace():
    assert_identical_atom(' \t\r\n')


def test_identifiers():
    assert_identical_atom('xyz')


def test_string_literals():
    assert_identical_atom("''")
    assert_identical_atom("'as\"df'")
    assert_identical_atom('"as\'df"')


def test_numeric_literals():
    assert_identical_atom('0')
    assert_identical_atom('1.2')
    assert_identical_atom('3e+21')
    assert_identical_atom('4e-22')
    assert_identical_atom('5.6e+23')
    assert_identical_atom('7.8e-24')

    assert_equivalent_literal('1.')
    assert_equivalent_literal('.2')
    assert_equivalent_literal('3.e4')
    assert_equivalent_literal('5.e+6')
    assert_equivalent_literal('7.e-8')
    assert_equivalent_literal('.9e10')
    assert_equivalent_literal('.11e+12')
    assert_equivalent_literal('.13e-14')


def test_list():
    assert_equivalent_python_text_and_text_ast('[]', '(list)')
    assert_equivalent_python_text_and_text_ast('[0, 1, 2]', '(list 0 1 2)')


def test_tuple():
    assert python_source_to_text_ast('()') == '(list)'
    assert python_source_to_text_ast('(0, 1, 2)') == '(list 0 1 2)'


def test_attr():
    assert_equivalent_python_text_and_text_ast('a.b', "(attr a 'b')")


def test_call():
    assert_equivalent_python_text_and_text_ast('a()', "(call a)")
    assert_equivalent_python_text_and_text_ast('a(0, 1, 2)', "(call a 0 1 2)")


def test_unary_operators():
    assert python_source_to_text_ast('+1') == '1'
    assert_ast_nodes_are_equal(text_ast_to_python_ast('+1'), ast.parse('1'))
    assert python_source_to_text_ast('-1') == '-1'
    assert_ast_nodes_are_equal(text_ast_to_python_ast('-1'), ast.parse('-1'))


def test_binary_operators():
    assert_equivalent_python_text_and_text_ast('1 + 2', "(+ 1 2)")
    assert_equivalent_python_text_and_text_ast('1 - 2', "(- 1 2)")
    assert_equivalent_python_text_and_text_ast('1 * 2', "(* 1 2)")
    assert_equivalent_python_text_and_text_ast('1 / 2', "(/ 1 2)")


def test_comparison_operators():
    assert_equivalent_python_text_and_text_ast('1 == 2', "(== 1 2)")
    assert_equivalent_python_text_and_text_ast('1 != 2', "(!= 1 2)")
    assert_equivalent_python_text_and_text_ast('1 < 2', "(< 1 2)")
    assert_equivalent_python_text_and_text_ast('1 <= 2', "(<= 1 2)")
    assert_equivalent_python_text_and_text_ast('1 > 2', "(> 1 2)")
    assert_equivalent_python_text_and_text_ast('1 >= 2', "(>= 1 2)")


def test_lambda():
    assert_equivalent_python_text_and_text_ast('lambda: 0', "(lambda (list) 0)")
    assert_equivalent_python_text_and_text_ast('lambda x, y, z: x', "(lambda (list x y z) x)")


def test_Select():
    select_node = Select(source=ast.parse('data_source').body[0].value,
                         selector=ast.parse('lambda e: e').body[0].value)
    assert_equivalent_python_ast_and_text_ast(ast.Module(body=[ast.Expr(value=select_node)]),
                                              '(Select data_source (lambda (list e) e))')
