import unittest

from pyobo.obo_lexer import OboLexerBuilder, StanzaValueLexer
from pyobo.tests.base_test_for_lexer import BaseTestForLexer


class StanzaValueLexerTest(BaseTestForLexer, unittest.TestCase):

    def setUp(self):
        BaseTestForLexer.setUp(self)
        self.under_test.in_header = False

    def lexing_module(self):
        return StanzaValueLexer()

    def begin_state(self):
        return OboLexerBuilder.STANZA_VALUE

    def test_should_recognise_stanza_tag_values(self):
        actual = self.tokenize("""Any characters but new lines \u0145 \\a""")
        self.assert_lexing(actual, [["TAG_VALUE", "Any characters but new lines \u0145 \\a", 1, 0]], pop_states=1)

    def test_should_recognise_escape_characters_in_stanza_tag_values(self):
        actual = self.tokenize("""Escape chars: \u0145 \\a\\n\\W\\t\\:\\,\\"\\\\\\(\\)\\{\\}\\[\\]@""")
        self.assert_lexing(actual, [["TAG_VALUE", """Escape chars: \u0145 \\a
 \t:,\"\\(){}[]@""", 1, 0]], pop_states=1)

    def test_should_recognise_true_tag_values_in_stanza(self):
        actual = self.tokenize("true")
        self.assert_lexing(actual, [["BOOLEAN", "true", 1, 0]], pop_states=1)

    def test_should_recognise_false_tag_values_in_stanza(self):
        actual = self.tokenize("false")
        self.assert_lexing(actual, [["BOOLEAN", "false", 1, 0]], pop_states=1)
