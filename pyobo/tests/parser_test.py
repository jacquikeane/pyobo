import unittest
from unittest.mock import Mock, call

from pyobo.obo_lexer import OboLexerBuilder
from pyobo.obo_parser import OboParser


class TestParser(unittest.TestCase):

    def test_should_parse_tag_value_pairs(self):
        mock_callback = Mock()
        # todo ideally mock the lexer.
        OboParser(OboLexerBuilder().new_lexer(), mock_callback).parse_line("""
        format-version: 1.2
        """)
        expected = [call.tag_value_pair('format-version', '1.2'),
                    call.tag_definition(),
                    call.tag_list_single(),
                    call.header_clause(),
                    call.obo_file()]
        self.assertDictEqual(mock_callback.mock_calls, expected)
