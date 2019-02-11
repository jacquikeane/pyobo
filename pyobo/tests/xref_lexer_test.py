import unittest

from pyobo.obo_lexer import OboLexerBuilder, XRefLexer
from pyobo.tests.base_test_for_lexer import BaseTestForLexer


class XRefLexerTest(BaseTestForLexer, unittest.TestCase):

    def setUp(self):
        BaseTestForLexer.setUp(self)
        self.under_test.in_header = False

    def lexing_module(self):
        return XRefLexer()

    def begin_state(self):
        return OboLexerBuilder.XREF

    # TODO double quote is also a special char that should be supported
    def test_should_recognise_xref_description(self):
        actual = self.tokenize("\"=some value,,{\"")
        self.assert_lexing(actual, [["XREF_DESCRIPTION", "=some value,,{", 1, 0]])

    def test_should_recognise_xref_description_with_escape_chars(self):
        actual = self.tokenize("""\"=some value,,{ \\a\\n\\W\\t\\:\\,\\\\\\(\\)\\{\\}\\[\\]@\"""")
        self.assert_lexing(actual, [["XREF_DESCRIPTION", """=some value,,{ \\a
 \t:,\\(){}[]@""", 1, 0]])

    def test_should_recognise_xref(self):
        actual = self.tokenize("somexref")
        self.assert_lexing(actual, [["XREF", "somexref", 1, 0]])

    def test_should_recognise_xref_with_escape_chars(self):
        actual = self.tokenize("""somexref\\a\\n\\W\\t\\:\\,\\"\\\\\\(\\)\\{\\}\\[\\]@""")
        self.assert_lexing(actual, [["XREF", """somexref\\a
 \t:,\"\\(){}[]@""", 1, 0]])
