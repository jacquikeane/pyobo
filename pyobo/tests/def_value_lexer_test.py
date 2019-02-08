import unittest

from pyobo.obo_lexer import DefTagValueLexer, OboLexerBuilder
from pyobo.tests.base_test_for_lexer import BaseTestForLexer


class DefTagValueLexerTest(BaseTestForLexer, unittest.TestCase):

    def setUp(self):
        BaseTestForLexer.setUp(self)
        self.under_test.in_header = False

    def lexing_module(self):
        return DefTagValueLexer()

    def begin_state(self):
        return OboLexerBuilder.DEF_VALUE

    def test_should_recognise_def_tag_values(self):
        actual = self.tokenize("""\"Hello\"""")
        self.assert_lexing(actual, [["TAG_VALUE", "Hello", 1, 0]], pop_states=1)

    def test_should_recognise_def_tag_values_with_escape_chars(self):
        actual = self.tokenize("""\"Escape chars: \u0145 \\a\\n\\W\\t\\:\\,\\"\\\\\\(\\)\\{\\}\\[\\]@\"""")
        self.assert_lexing(actual, [["TAG_VALUE", """Escape chars: \u0145 \\a
 \t:,\"\\(){}[]@""", 1, 0]], pop_states=1)
