import unittest
from unittest.mock import Mock, call

from pyobo.obo_lexer import OboLexerBuilder
from pyobo.obo_parser import OboParser


# todo ideally mock the lexer.
class TestParser(unittest.TestCase):

    def test_should_parse_tag_value_pair(self):
        mock_callback = Mock()
        OboParser(OboLexerBuilder().new_lexer(), mock_callback).parse_line("format-version: 1.2")
        self.assertEquals(mock_callback.mock_calls, [call.tag_value_pair('format-version', '1.2')])

    def test_should_parse_typedef(self):
        mock_callback = Mock()
        OboParser(OboLexerBuilder().new_lexer(), mock_callback).parse_line("[Typedef]")
        self.assertEquals(mock_callback.mock_calls, [call.typedef()])

    def test_should_parse_term(self):
        mock_callback = Mock()
        OboParser(OboLexerBuilder().new_lexer(), mock_callback).parse_line("[Term]")
        self.assertEquals(mock_callback.mock_calls, [call.term()])
