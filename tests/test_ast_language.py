from ast_language import *

import ast

def check_python_round_trip(initial_python_text):
  initial_python_ast = ast.parse(initial_python_text)
  text_ast = python_ast_to_text_ast(initial_python_ast)
  final_python_ast = text_ast_to_python_ast(text_ast)
  assert ast.dump(final_python_ast) == ast.dump(initial_python_ast)

def get_text_ast_round_trip(initial_text_ast):
  python_ast = text_ast_to_python_ast(initial_text_ast)
  return python_ast_to_text_ast(python_ast)

def check_text_ast_round_trip(initial_text_ast):
  assert get_text_ast_round_trip(initial_text_ast) == initial_text_ast.strip(' \t\r\n')

def check_round_trip_both_ways(text):
  check_python_round_trip(text)
  check_text_ast_round_trip(text)

def check_text_ast_round_trip_eval(initial_text_ast):
  assert ast.literal_eval(get_text_ast_round_trip(initial_text_ast)) == ast.literal_eval(initial_text_ast)

def check_round_trip_both_ways_eval(text):
  check_python_round_trip(text)
  check_text_ast_round_trip_eval(text)


def test_empty():
  check_round_trip_both_ways('')

def test_whitespace():
  check_round_trip_both_ways(' \t\r\n')

def test_identifiers():
  check_round_trip_both_ways('x')

def test_numeric_literals():
  check_round_trip_both_ways('0')
  check_round_trip_both_ways('1.2')
  check_round_trip_both_ways('3e+21')
  check_round_trip_both_ways('4e-22')
  check_round_trip_both_ways('5.6e+23')
  check_round_trip_both_ways('7.8e-24')

  check_round_trip_both_ways_eval('1.')
  check_round_trip_both_ways_eval('.2')
  check_round_trip_both_ways_eval('3.e4')
  check_round_trip_both_ways_eval('5.e+6')
  check_round_trip_both_ways_eval('7.e-8')
  check_round_trip_both_ways_eval('.9e10')
  check_round_trip_both_ways_eval('.11e+12')
  check_round_trip_both_ways_eval('.13e-14')

def test_string_literals():
  check_round_trip_both_ways("''")
  check_round_trip_both_ways("'as\"df'")
  check_round_trip_both_ways('"as\'df"')
