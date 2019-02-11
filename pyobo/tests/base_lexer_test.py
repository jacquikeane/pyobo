import unittest

from pyobo.obo_lexer import BaseLexer
from pyobo.parsing_exception import OboParsingError
from pyobo.tests.base_test_for_lexer import BaseTestForLexer


class BaseLexerTest(BaseTestForLexer, unittest.TestCase):

    def setUp(self):
        BaseTestForLexer.setUp(self)
        self.under_test.in_header = False

    def lexing_module(self):
        return BaseLexer()

    def begin_state(self):
        return "INITIAL"

    def test_should_recognise_ignore_new_lines(self):
        actual = self.tokenize("\n")
        self.assert_lexing(actual, [])

    def test_should_recognise_ignore_spaces(self):
        actual = self.tokenize(" \t\u0020\u0009\n")
        self.assert_lexing(actual, [])

    def test_should_throw_exception_on_lexing_error(self):
        with self.assertRaises(OboParsingError):
            self.tokenize("A")
