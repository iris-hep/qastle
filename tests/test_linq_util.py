from .testing_util import *

from qastle import *

import ast
import copy

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


def test_select_copy():
    select = Select('src', 'slctr')
    select_copy = copy.copy(select)
    assert select_copy.source == select.source and select_copy.selector == select.selector


def test_select_deepcopy():
    select = Select('src', 'slctr')
    select_copy = copy.deepcopy(select)
    assert select_copy.source == select.source and select_copy.selector == select.selector
    select.source = 'src2'
    select.selector = 'slctr2'
    assert select_copy.source == 'src' and select_copy.selector == 'slctr'


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


def test_last():
    initial_ast = ast.parse("the_source.Last()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Last(source=unwrap_ast(ast.parse('the_source'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_last_composite():
    initial_ast = ast.parse("the_source.First().Last()")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Last(source=First(source=unwrap_ast(ast.parse('the_source')))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_last_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Last(None)'))


def test_elementat():
    initial_ast = ast.parse("the_source.ElementAt(2)")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(ElementAt(source=unwrap_ast(ast.parse('the_source')),
                                      index=unwrap_ast(ast.parse('2'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_elementat_composite():
    initial_ast = ast.parse("the_source.First().ElementAt(2)")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(ElementAt(source=First(source=unwrap_ast(ast.parse('the_source'))),
                                      index=unwrap_ast(ast.parse('2'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_elementat_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.ElementAt()'))


def test_contains():
    initial_ast = ast.parse("the_source.Contains(element)")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Contains(source=unwrap_ast(ast.parse('the_source')),
                                     value=unwrap_ast(ast.parse('element'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_contains_composite():
    initial_ast = ast.parse("the_source.First().Contains(element)")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Contains(source=First(source=unwrap_ast(ast.parse('the_source'))),
                                     value=unwrap_ast(ast.parse('element'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_contains_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Contains()'))


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


def test_all():
    initial_ast = ast.parse("the_source.All('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(All(source=unwrap_ast(ast.parse('the_source')),
                                predicate=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_all_composite():
    initial_ast = ast.parse("the_source.First().All('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(All(source=First(source=unwrap_ast(ast.parse('the_source'))),
                                predicate=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_all_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.All()'))
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.All(None)'))


def test_any():
    initial_ast = ast.parse("the_source.Any('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Any(source=unwrap_ast(ast.parse('the_source')),
                                predicate=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_any_composite():
    initial_ast = ast.parse("the_source.First().Any('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Any(source=First(source=unwrap_ast(ast.parse('the_source'))),
                                predicate=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_any_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Any()'))
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Any(None)'))


def test_concat():
    initial_ast = ast.parse("sequence1.Concat(sequence2)")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Concat(first=unwrap_ast(ast.parse('sequence1')),
                                   second=unwrap_ast(ast.parse('sequence2'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_concat_composite():
    initial_ast = ast.parse("the_source.First().Concat(sequence)")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Concat(first=First(source=unwrap_ast(ast.parse('the_source'))),
                                   second=unwrap_ast(ast.parse('sequence'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_concat_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Concat()'))


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


def test_orderby():
    initial_ast = ast.parse("the_source.OrderBy('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(OrderBy(source=unwrap_ast(ast.parse('the_source')),
                                    key_selector=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_orderby_composite():
    initial_ast = ast.parse("the_source.First().OrderBy('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(OrderBy(source=First(source=unwrap_ast(ast.parse('the_source'))),
                                    key_selector=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_orderby_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.OrderBy()'))
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.OrderBy(None)'))


def test_orderbydescending():
    initial_ast = ast.parse("the_source.OrderByDescending('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(
        OrderByDescending(source=unwrap_ast(ast.parse('the_source')),
                          key_selector=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_orderbydescending_composite():
    initial_ast = ast.parse("the_source.First().OrderByDescending('lambda row: row')")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(
        OrderByDescending(source=First(source=unwrap_ast(ast.parse('the_source'))),
                          key_selector=unwrap_ast(ast.parse('lambda row: row'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_orderbydescending_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.OrderByDescending()'))
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.OrderByDescending(None)'))


def test_choose():
    initial_ast = ast.parse("the_source.Choose(2)")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Choose(source=unwrap_ast(ast.parse('the_source')),
                                   n=unwrap_ast(ast.parse('2'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_choose_composite():
    initial_ast = ast.parse("the_source.First().Choose(2)")
    final_ast = insert_linq_nodes(initial_ast)
    expected_ast = wrap_ast(Choose(source=First(source=unwrap_ast(ast.parse('the_source'))),
                                   n=unwrap_ast(ast.parse('2'))))
    assert_ast_nodes_are_equal(final_ast, expected_ast)


def test_choose_bad():
    with pytest.raises(SyntaxError):
        insert_linq_nodes(ast.parse('the_source.Choose()'))
