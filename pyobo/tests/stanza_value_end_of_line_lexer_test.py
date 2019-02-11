import unittest

from pyobo.obo_lexer import OboLexerBuilder, StanzaValueEndOfLineLexer
from pyobo.tests.base_test_for_lexer import BaseTestForLexer


class StanzaValueEndOfLineLexerTest(BaseTestForLexer, unittest.TestCase):

    def setUp(self):
        BaseTestForLexer.setUp(self)
        self.under_test.in_header = False

    def lexing_module(self):
        return StanzaValueEndOfLineLexer()

    def begin_state(self):
        return OboLexerBuilder.END_OF_LINE

    def test_should_recognize_qualifier_block_start(self):
        actual = self.tokenize("{")
        self.assert_lexing(actual, [["QUALIFIER_BLOCK_START", "{", 1, 0]], push_states=[OboLexerBuilder.QUALIFIER])

    def test_should_ignore_comments(self):
        actual = self.tokenize(" \t\u0020\u0009! Some comment")
        self.assert_lexing(actual, [])

    def test_should_pop_state_on_new_lines(self):
        actual = self.tokenize("\n")
        self.assert_lexing(actual, [], pop_states=1)


class StanzaValueEndOfLineLexerForXrefTest(StanzaValueEndOfLineLexerTest, unittest.TestCase):

    def setUp(self):
        StanzaValueEndOfLineLexerTest.setUp(self)

    def begin_state(self):
        return OboLexerBuilder.XREF
