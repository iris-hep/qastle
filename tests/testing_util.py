import ast


def are_ast_nodes_equal(ast_1, ast_2):
    return ast.dump(ast_1) == ast.dump(ast_2)


def assert_ast_nodes_are_equal(ast_1, ast_2):
    assert are_ast_nodes_equal(ast_1, ast_2), ('ast_1 = ' + ast.dump(ast_1)
                                               + ', ast_2 = ' + ast.dump(ast_2))
