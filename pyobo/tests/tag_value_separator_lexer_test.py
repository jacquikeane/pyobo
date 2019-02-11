import unittest

from pyobo.obo_lexer import OboLexerBuilder, TagValueSeparatorLexer
from pyobo.tests.base_test_for_lexer import BaseTestForLexer


class TagValueSeparatorLexerTest(BaseTestForLexer, unittest.TestCase):

    def setUp(self):
        BaseTestForLexer.setUp(self)
        self.under_test.in_header = False

    def lexing_module(self):
        return TagValueSeparatorLexer()

    def begin_state(self):
        return OboLexerBuilder.TAG_VALUE_SEPARATOR

    def test_should_tag_value_separator(self):
        actual = self.tokenize(":")
        self.assert_lexing(actual, [["TAG_VALUE_SEPARATOR", ":", 1, 0]], pop_states=1)

    def test_should_rignore_spaces(self):
        actual = self.tokenize(" \t\u0020\u0009:")
        self.assert_lexing(actual, [["TAG_VALUE_SEPARATOR", ":", 1, 4]], pop_states=1)
