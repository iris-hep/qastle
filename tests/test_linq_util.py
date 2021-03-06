from .testing_util import *

from qastle import *

import ast

import pytest


def test_visit_call_attribute_generic():
    initial_ast = ast.parse('an_object.a_function()')
    final_ast = insert_linq_nodes(initial_ast)
    assert_ast_nodes_are_equal(final_ast, initial_ast)


def test_visit_call_attribute_linq_operator():
    initial_ast = ast.parse("the_source.Select('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Select(source=unwrap_ast(ast.parse('the_source')),
                                   selector=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_visit_call_name_generic():
    initial_ast = ast.parse('a_function()')
    final_ast = insert_linq_nodes(initial_ast)
    assert_ast_nodes_are_equal(final_ast, initial_ast)


def test_visit_call_name_linq_operator():
    initial_ast = ast.parse("Select(the_source, 'lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Select(source=unwrap_ast(ast.parse('the_source')),
                                   selector=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_visit_call_name_linq_operator_no_source():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse("First()"))


def test_visit_call_generic():
    initial_ast = ast.parse('None()')
    final_ast = insert_linq_nodes(initial_ast)
    assert_ast_nodes_are_equal(final_ast, initial_ast)


def test_where():
    initial_ast = ast.parse("the_source.Where('lambda row: True')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Where(source=unwrap_ast(ast.parse('the_source')),
                                  predicate=unwrap_ast(ast.parse('lambda row: True'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_where_composite():
    initial_ast = ast.parse("the_source.First().Where('lambda row: True')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Where(source=First(source=unwrap_ast(ast.parse('the_source'))),
                                  predicate=unwrap_ast(ast.parse('lambda row: True'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_where_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Where()'))
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Where(None)'))


def test_select():
    initial_ast = ast.parse("the_source.Select('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Select(source=unwrap_ast(ast.parse('the_source')),
                                   selector=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_select_composite():
    initial_ast = ast.parse("the_source.First().Select('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Select(source=First(source=unwrap_ast(ast.parse('the_source'))),
                                   selector=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_select_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Select()'))
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Select(None)'))


def test_selectmany():
    initial_ast = ast.parse("the_source.SelectMany('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(SelectMany(source=unwrap_ast(ast.parse('the_source')),
                                       selector=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_selectmany_composite():
    initial_ast = ast.parse("the_source.First().SelectMany('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(SelectMany(source=First(source=unwrap_ast(ast.parse('the_source'))),
                                       selector=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_selectmany_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.SelectMany()'))
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.SelectMany(None)'))


def test_first():
    initial_ast = ast.parse("the_source.First()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(First(source=unwrap_ast(ast.parse('the_source'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_first_composite():
    initial_ast = ast.parse("the_source.First().First()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(First(source=First(source=unwrap_ast(ast.parse('the_source')))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_first_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.First(None)'))


def test_aggregate():
    initial_ast = ast.parse("the_source.Aggregate(0, 'lambda total, next: total + next')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Aggregate(source=unwrap_ast(ast.parse('the_source')),
                                      seed=unwrap_ast(ast.parse('0')),
                                      func=unwrap_ast(ast.parse('lambda total, next:'
                                                                + ' total + next'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_aggregate_composite():
    initial_ast = ast.parse("the_source.First().Aggregate(0, 'lambda total, next: total + next')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Aggregate(source=First(source=unwrap_ast(ast.parse('the_source'))),
                                      seed=unwrap_ast(ast.parse('0')),
                                      func=unwrap_ast(ast.parse('lambda total, next:'
                                                                + ' total + next'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_aggregate_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Aggregate()'))
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Aggregate(None)'))
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Aggregate(None, None)'))


def test_count():
    initial_ast = ast.parse("the_source.Count()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Count(source=unwrap_ast(ast.parse('the_source'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_count_composite():
    initial_ast = ast.parse("the_source.First().Count()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Count(source=First(source=unwrap_ast(ast.parse('the_source')))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_count_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Count(None)'))


def test_max():
    initial_ast = ast.parse("the_source.Max()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Max(source=unwrap_ast(ast.parse('the_source'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_max_composite():
    initial_ast = ast.parse("the_source.First().Max()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Max(source=First(source=unwrap_ast(ast.parse('the_source')))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_max_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Max(None)'))


def test_min():
    initial_ast = ast.parse("the_source.Min()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Min(source=unwrap_ast(ast.parse('the_source'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_min_composite():
    initial_ast = ast.parse("the_source.First().Min()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Min(source=First(source=unwrap_ast(ast.parse('the_source')))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_min_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Min(None)'))


def test_sum():
    initial_ast = ast.parse("the_source.Sum()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Sum(source=unwrap_ast(ast.parse('the_source'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_sum_composite():
    initial_ast = ast.parse("the_source.First().Sum()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Sum(source=First(source=unwrap_ast(ast.parse('the_source')))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_sum_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Sum(None)'))


def test_zip():
    initial_ast = ast.parse("the_source.Zip()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Zip(source=unwrap_ast(ast.parse('the_source'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_zip_composite():
    initial_ast = ast.parse("the_source.First().Zip()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Zip(source=First(source=unwrap_ast(ast.parse('the_source')))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_zip_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Zip(None)'))
