import ast

import pytest

from qastle import python_ast_to_text_ast, text_ast_to_python_ast, unwrap_ast


@pytest.mark.parametrize(
    "source",
    [
        "Select(Where(EventDataset(['input.root'], 'events'), "
        "lambda event: event['pt'] > 20), lambda event: event['pt'])",
        "Take(Skip(EventDataset(['input.root'], 'events'), 2), 3)",
    ],
)
def test_query_roundtrip(source):
    original = ast.parse(source).body[0].value
    text = python_ast_to_text_ast(original)
    restored = unwrap_ast(text_ast_to_python_ast(text))
    assert ast.dump(restored) == ast.dump(original)
    assert python_ast_to_text_ast(restored) == text
