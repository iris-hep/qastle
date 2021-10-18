from .testing_util import *

from qastle import *

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
    assert_equivalent_python_text_and_text_ast('[0]', '(list 0)')
    assert_equivalent_python_text_and_text_ast('[0, 1, 2]', '(list 0 1 2)')


def test_tuple():
    assert python_source_to_text_ast('()') == '(list)'
    assert python_source_to_text_ast('(0,)') == '(list 0)'
    assert python_source_to_text_ast('(0, 1, 2)') == '(list 0 1 2)'


def test_dict():
    assert_equivalent_python_text_and_text_ast('{}', '(dict (list) (list))')
    assert_equivalent_python_text_and_text_ast('{0: 0}', '(dict (list 0) (list 0))')
    assert_equivalent_python_text_and_text_ast("{0: 0, 1: 'a', 'b': 2, 'abc': 'abc'}",
                                               "(dict (list 0 1 'b' 'abc') (list 0 'a' 2 'abc'))")


def test_attr():
    assert_equivalent_python_text_and_text_ast('a.b', "(attr a 'b')")


def test_subscript():
    assert_equivalent_python_text_and_text_ast('a[0]', '(subscript a 0)')
    assert_equivalent_python_text_and_text_ast("a['b']", "(subscript a 'b')")


def test_call():
    assert_equivalent_python_text_and_text_ast('a()', '(call a)')
    assert_equivalent_python_text_and_text_ast('a(0, 1, 2)', '(call a 0 1 2)')


def test_if():
    assert_equivalent_python_text_and_text_ast('a if b else c', '(if b a c)')


def test_unary_operators():
    assert python_source_to_text_ast('+1') == '1'
    assert_ast_nodes_are_equal(text_ast_to_python_ast('+1'), ast.parse('1'))
    assert_equivalent_python_text_and_text_ast('+a', '(+ a)')
    assert_equivalent_python_text_and_text_ast('-1', '-1')
    assert_equivalent_python_text_and_text_ast('-a', '(- a)')
    assert_equivalent_python_text_and_text_ast('not True', '(not True)')
    assert_equivalent_python_text_and_text_ast('~1', '(~ 1)')


def test_binary_operators():
    assert_equivalent_python_text_and_text_ast('1 + 2', '(+ 1 2)')
    assert_equivalent_python_text_and_text_ast('1 - 2', '(- 1 2)')
    assert_equivalent_python_text_and_text_ast('1 * 2', '(* 1 2)')
    assert_equivalent_python_text_and_text_ast('1 / 2', '(/ 1 2)')
    assert_equivalent_python_text_and_text_ast('1 % 2', '(% 1 2)')
    assert_equivalent_python_text_and_text_ast('1 ** 2', '(** 1 2)')
    assert_equivalent_python_text_and_text_ast('1 // 2', '(// 1 2)')
    assert_equivalent_python_text_and_text_ast('1 & 2', '(& 1 2)')
    assert_equivalent_python_text_and_text_ast('1 | 2', '(| 1 2)')
    assert_equivalent_python_text_and_text_ast('1 ^ 2', '(^ 1 2)')
    assert_equivalent_python_text_and_text_ast('1 << 2', '(<< 1 2)')
    assert_equivalent_python_text_and_text_ast('1 >> 2', '(>> 1 2)')


def test_boolean_operators():
    assert_equivalent_python_text_and_text_ast('True and False', '(and True False)')
    assert_equivalent_python_text_and_text_ast('True or False', '(or True False)')
    assert python_source_to_text_ast('a and b and c') == '(and (and a b) c)'


def test_comparison_operators():
    assert_equivalent_python_text_and_text_ast('1 == 2', '(== 1 2)')
    assert_equivalent_python_text_and_text_ast('1 != 2', '(!= 1 2)')
    assert_equivalent_python_text_and_text_ast('1 < 2', '(< 1 2)')
    assert_equivalent_python_text_and_text_ast('1 <= 2', '(<= 1 2)')
    assert_equivalent_python_text_and_text_ast('1 > 2', '(> 1 2)')
    assert_equivalent_python_text_and_text_ast('1 >= 2', '(>= 1 2)')
    assert python_source_to_text_ast('1 < 2 < 3') == '(and (< 1 2) (< 2 3))'
    assert python_source_to_text_ast('1 < 2 < 3 < 4') == '(and (and (< 1 2) (< 2 3)) (< 3 4))'


def test_lambda():
    assert_equivalent_python_text_and_text_ast('lambda: 0', '(lambda (list) 0)')
    assert_equivalent_python_text_and_text_ast('lambda x, y, z: x', '(lambda (list x y z) x)')


def test_Where():
    where_node = Where(source=unwrap_ast(ast.parse('data_source')),
                       predicate=unwrap_ast(ast.parse('lambda e: e')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(where_node),
                                              '(Where data_source (lambda (list e) e))')


def test_Select():
    select_node = Select(source=unwrap_ast(ast.parse('data_source')),
                         selector=unwrap_ast(ast.parse('lambda e: e')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(select_node),
                                              '(Select data_source (lambda (list e) e))')


def test_SelectMany():
    selectmany_node = SelectMany(source=unwrap_ast(ast.parse('data_source')),
                                 selector=unwrap_ast(ast.parse('lambda e: e')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(selectmany_node),
                                              '(SelectMany data_source (lambda (list e) e))')


def test_First():
    first_node = First(source=unwrap_ast(ast.parse('data_source')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(first_node),
                                              '(First data_source)')


def test_Last():
    first_node = Last(source=unwrap_ast(ast.parse('data_source')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(first_node),
                                              '(Last data_source)')


def test_ElementAt():
    first_node = ElementAt(source=unwrap_ast(ast.parse('data_source')),
                           index=unwrap_ast(ast.parse('2')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(first_node),
                                              '(ElementAt data_source 2)')


def test_Contains():
    first_node = Contains(source=unwrap_ast(ast.parse('data_source')),
                          value=unwrap_ast(ast.parse('element')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(first_node),
                                              '(Contains data_source element)')


def test_Aggregate():
    aggregate_node = Aggregate(source=unwrap_ast(ast.parse('data_source')),
                               seed=unwrap_ast(ast.parse('0')),
                               func=unwrap_ast(ast.parse('lambda v, e : v + e')))
    text_ast = '(Aggregate data_source 0 (lambda (list v e) (+ v e)))'
    assert_equivalent_python_ast_and_text_ast(wrap_ast(aggregate_node),
                                              text_ast)


def test_Count():
    first_node = Count(source=unwrap_ast(ast.parse('data_source')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(first_node),
                                              '(Count data_source)')


def test_Max():
    first_node = Max(source=unwrap_ast(ast.parse('data_source')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(first_node),
                                              '(Max data_source)')


def test_Min():
    first_node = Min(source=unwrap_ast(ast.parse('data_source')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(first_node),
                                              '(Min data_source)')


def test_Sum():
    first_node = Sum(source=unwrap_ast(ast.parse('data_source')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(first_node),
                                              '(Sum data_source)')


def test_All():
    select_node = All(source=unwrap_ast(ast.parse('data_source')),
                      predicate=unwrap_ast(ast.parse('lambda e: e')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(select_node),
                                              '(All data_source (lambda (list e) e))')


def test_Any():
    select_node = Any(source=unwrap_ast(ast.parse('data_source')),
                      predicate=unwrap_ast(ast.parse('lambda e: e')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(select_node),
                                              '(Any data_source (lambda (list e) e))')


def test_Concat():
    first_node = Concat(first=unwrap_ast(ast.parse('sequence1')),
                        second=unwrap_ast(ast.parse('sequence2')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(first_node),
                                              '(Concat sequence1 sequence2)')


def test_Zip():
    first_node = Zip(source=unwrap_ast(ast.parse('data_source')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(first_node),
                                              '(Zip data_source)')


def test_OrderBy():
    orderby_node = OrderBy(source=unwrap_ast(ast.parse('data_source')),
                           key_selector=unwrap_ast(ast.parse('lambda e: e')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(orderby_node),
                                              '(OrderBy data_source (lambda (list e) e))')


def test_OrderByDescending():
    orderbydescending_node = OrderByDescending(source=unwrap_ast(ast.parse('data_source')),
                                               key_selector=unwrap_ast(ast.parse('lambda e: e')))
    assert_equivalent_python_ast_and_text_ast(
        wrap_ast(orderbydescending_node),
        '(OrderByDescending data_source (lambda (list e) e))')


def test_Choose():
    choose_node = Choose(source=unwrap_ast(ast.parse('data_source')),
                         n=unwrap_ast(ast.parse('2')))
    assert_equivalent_python_ast_and_text_ast(wrap_ast(choose_node),
                                              '(Choose data_source 2)')
