import lark

import os


syntax_specification_pathname = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             'syntax.lark')

with open(syntax_specification_pathname) as syntax_specification_file:
    Parser = lark.Lark(syntax_specification_file.read(), start='record')


def parse(text):
    return Parser.parse(text)
