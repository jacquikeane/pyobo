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

    def test_should_parse_boolean_tag_value_pair(self):
        mock_callback = Mock()
        OboParser(OboLexerBuilder().new_lexer(), mock_callback).parse_line("is_anonymous: true")
        self.assertEquals(mock_callback.mock_calls, [call.boolean_tag_value_pair('is_anonymous', True)])

    def test_should_parse_tag_value_pair_with_qualifiers(self):
        mock_callback = Mock()
        builder = OboLexerBuilder()
        builder.in_header = False
        OboParser(builder.new_lexer(), mock_callback).parse_line(
            """range: BFO:0000004 {http://purl.obolibrary.org/obo/IAO_0000116="This is redundant with the more """
            """specific 'independent and not spatial region' constraint. We leave in the redundant axiom for use """
            """with reasoners that do not use negation.",  XXX="YYY"} ! some comment""")
        self.assertEquals(mock_callback.mock_calls, [
            call.qualifier('http://purl.obolibrary.org/obo/IAO_0000116',
                           "This is redundant with the more specific 'independent and not spatial region' constraint. "
                           "We leave in the redundant axiom for use with reasoners that do not use negation."),
            call.qualifier("XXX", "YYY"),
            call.tag_value_pair('range', 'BFO:0000004'),
        ])

    def test_should_parse_typedef(self):
        mock_callback = Mock()
        OboParser(OboLexerBuilder().new_lexer(), mock_callback).parse_line("[Typedef]")
        self.assertEquals(mock_callback.mock_calls, [call.typedef()])

    def test_should_parse_term(self):
        mock_callback = Mock()
        OboParser(OboLexerBuilder().new_lexer(), mock_callback).parse_line("[Term]")
        self.assertEquals(mock_callback.mock_calls, [call.term()])
