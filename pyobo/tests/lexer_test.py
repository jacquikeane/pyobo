import re
import unittest

import ply.lex as lex
from ply.lex import LexToken


class OBOLexerBuilder:
    t_WhiteSpaceChar = "[ \t\u0020\u0009]"
    # 9
    # ws::= WhiteSpaceChar
    # {WhiteSpaceChar}
    # NewlineChar::= \r | \n | U + 000
    # A | U + 000
    # C | U + 000
    # D
    # nl::= [ws]
    # NewLineChar
    # nl *::= {nl}

    tokens = ['NAME', 'WhiteSpaceChar']

    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def __init__(self):
        self.current_char_count = 0

    def t_newline(self, token):
        r"""\n+"""
        token.lexer.lineno += len(token.value)
        global current_char_count
        self.current_char_count = token.lexpos

    def t_error(self, token):
        print("Illegal character '%s' at line %s position %s" % (token.value[0], token.lineno,
                                                                 self.token_position(token)))
        token.lexer.skip(1)

    def token_position(self, token):
        return token.lexpos - self.current_char_count

    def new_lexer(self, **kwargs):
        return lex.lex(module=self, reflags=re.UNICODE, **kwargs)

    def new_generator(self, input):
        lexer = self.new_lexer()
        lexer.input(input)

        def token_generator():
            while True:
                tok = lexer.token()
                if not tok:
                    break
                yield tok

        return token_generator()


# test_modules_dir = os.path.dirname(os.path.realpath(__file__))
# data_dir = os.path.join(test_modules_dir, 'data','read')

def to_token(type, value, line, position):
    token = LexToken()
    token.type = type
    token.value = value
    token.lineno = line
    token.lexpos = position
    return token


def extract_dictionary(list):
    return [x.__dict__ for x in list]


class TestRead(unittest.TestCase):

    def test_initialise(self):
        token_generator = OBOLexerBuilder().new_generator(""" \u0020\u0009\t""")
        expected = [to_token("WhiteSpaceChar", " ", 1, 0),
                    to_token("WhiteSpaceChar", " ", 1, 1),
                    to_token("WhiteSpaceChar", "\t", 1, 2),
                    to_token("WhiteSpaceChar", "\t", 1, 3)
                    ]
        actual = list(token_generator)
        self.assertEqualsByContent(actual, expected)

    def assertEqualsByContent(self, actual, expected):
        actual_dict = extract_dictionary(actual)
        expected_dict = extract_dictionary(expected)
        self.assertEqual(actual_dict, expected_dict)
