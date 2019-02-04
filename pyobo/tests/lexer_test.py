import unittest

from ply.lex import LexToken

from pyobo.obo_lexer import OboLexerBuilder


def to_token(lexer, type, value, line, position):
    token = LexToken()
    token.type = type
    token.value = value
    token.lineno = line
    token.lexpos = position
    token.lexer = lexer
    return token


def extract_dictionary(list):
    return [x.__dict__ for x in list]


class TestLexer(unittest.TestCase):

    def test_should_recognise_tags(self):
        lexer = OboLexerBuilder().new_lexer();
        actual = OboLexerBuilder().tokenize(lexer, """a_valid_tag-AZ_8:""")
        expected = [to_token(lexer, "TAG", "a_valid_tag-AZ_8", 1, 0)]
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_obo_strings(self):
        lexer = OboLexerBuilder().new_lexer();
        actual = OboLexerBuilder().tokenize(lexer, """It can contain any characters but new lines \u0145 \\a""")
        expected = [to_token(lexer, "OBO_UNQUOTED_STRING",
                             "It can contain any characters but new lines \u0145 \\a", 1, 0)]
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_new_lines(self):
        lexer = OboLexerBuilder().new_lexer();
        actual = OboLexerBuilder().tokenize(lexer, """
        a_valid_tag-AZ_8:""")
        expected = [to_token(lexer, "TAG", "a_valid_tag-AZ_8", 2, 9)]
        self.assertEqualsByContent(actual, expected)

    def test_should_ignore_spaces_and_tab(self):
        lexer = OboLexerBuilder().new_lexer();
        actual = OboLexerBuilder().tokenize(lexer, """  a_valid_tag-AZ_8: \t"""
                                            + """It can contain any characters but new lines \u0145 \\a""")
        expected = [
            to_token(lexer, "TAG", "a_valid_tag-AZ_8", 1, 2),
            to_token(lexer, "OBO_UNQUOTED_STRING", "It can contain any characters but new lines \u0145 \\a", 1, 21)]
        self.assertEqualsByContent(actual, expected)

    def assertEqualsByContent(self, actual, expected):
        actual_dict = extract_dictionary(actual)
        expected_dict = extract_dictionary(expected)
        self.assertEqual(actual_dict, expected_dict)
