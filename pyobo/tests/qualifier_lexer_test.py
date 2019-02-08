import unittest

from pyobo.obo_lexer import OboLexerBuilder, QualifierLexer
from pyobo.tests.base_test_for_lexer import BaseTestForLexer


class QualifierLexerTest(BaseTestForLexer, unittest.TestCase):

    def setUp(self):
        BaseTestForLexer.setUp(self)
        self.under_test.in_header = False

    def lexing_module(self):
        return QualifierLexer()

    def begin_state(self):
        return OboLexerBuilder.QUALIFIER

    def test_should_recognise_qualifier_ids(self):
        actual = self.tokenize("""AvalidId""")
        self.assert_lexing(actual, [["QUALIFIER_ID", "AvalidId", 1, 0]])

    def test_should_recognise_qualifier_end_block(self):
        actual = self.tokenize("}")
        self.assert_lexing(actual, [["QUALIFIER_BLOCK_END", "}", 1, 0]], pop_states=1)

    def test_should_recognise_qualifier_id_value_separator(self):
        actual = self.tokenize("=")
        self.assert_lexing(actual, [["QUALIFIER_ID_VALUE_SEPARATOR", "=", 1, 0]])

    def test_should_recognise_qualifier_list_separator(self):
        actual = self.tokenize(",")
        self.assert_lexing(actual, [["QUALIFIER_LIST_SEPARATOR", ",", 1, 0]])

    def test_should_not_recognise_curly_brackets_as_part_of_qualifier_id(self):
        actual = self.tokenize("""AvalidId}""")
        self.assert_lexing(actual, [["QUALIFIER_ID", "AvalidId", 1, 0], ["QUALIFIER_BLOCK_END", "}", 1, 8]],
                           pop_states=1)

    def test_should_recognise_qualifier_values(self):
        actual = self.tokenize("\"=some value,,{\"")
        self.assert_lexing(actual, [["QUALIFIER_VALUE", "=some value,,{", 1, 0]])

    def test_should_tokenize_qualifier_value_list(self):
        actual = self.tokenize("id=\"value\", other_id=\"other value\"}")
        self.assert_lexing(actual, [["QUALIFIER_ID", "id", 1, 0],
                                    ["QUALIFIER_ID_VALUE_SEPARATOR", "=", 1, 2],
                                    ["QUALIFIER_VALUE", "value", 1, 3],
                                    ["QUALIFIER_LIST_SEPARATOR", ",", 1, 10],
                                    ["QUALIFIER_ID", "other_id", 1, 12],
                                    ["QUALIFIER_ID_VALUE_SEPARATOR", "=", 1, 20],
                                    ["QUALIFIER_VALUE", "other value", 1, 21],
                                    ["QUALIFIER_BLOCK_END", "}", 1, 34],
                                    ], pop_states=1)
