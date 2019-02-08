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

    def test_should_parse_def_tag_with_xref(self):
        mock_callback = Mock()
        builder = OboLexerBuilder()
        builder.in_header = False
        OboParser(builder.new_lexer(), mock_callback).parse_line(
            '''def: "Enables the transfer of citrate, 2-hydroxy-1,2,3-propanetricarboyxlate, '''
            '''from one side of a membrane to the other." [GOC:ai,HELLO "WORLD"]''')
        self.assertEquals(mock_callback.mock_calls, [
            call.add_xref('GOC:ai', None),
            call.add_xref('HELLO', 'WORLD'),
            call.def_tag_value('Enables the transfer of citrate, 2-hydroxy-1,2,3-propanetricarboyxlate, '
                               'from one side of a membrane to the other.'),

        ])

    def test_should_parse_def_tag_with_xref_and_brackets(self):
        mock_callback = Mock()
        builder = OboLexerBuilder()
        builder.in_header = False
        OboParser(builder.new_lexer(), mock_callback).parse_line("""def: "Catalysis of the reaction!: {}2'-phospho-[ligated tRNA] + NAD+ = mature tRNA + ADP ribose 1'',2''-phosphate + nicotinamide + H2O. This reaction is the transfer of the splice junction 2-phosphate from ligated tRNA to NAD+ to produce ADP-ribose 1'-2' cyclic phosphate." [EC:2.7.1.160, PMID:9148937]
""")
        self.assertEquals(mock_callback.mock_calls, [
            call.add_xref('EC:2.7.1.160', None),
            call.add_xref('PMID:9148937', None),
            call.def_tag_value(
                "Catalysis of the reaction!: {}2'-phospho-[ligated tRNA] + NAD+ = mature tRNA + ADP ribose 1'',2''-phosphate + nicotinamide + H2O. This reaction is the transfer of the splice junction 2-phosphate from ligated tRNA to NAD+ to produce ADP-ribose 1'-2' cyclic phosphate."),

        ])

    def test_should_parse_xref_tag(self):
        mock_callback = Mock()
        builder = OboLexerBuilder()
        builder.in_header = False
        OboParser(builder.new_lexer(), mock_callback).parse_line(
            '''xref: reactome:R-HSA-71593 "((1,6)-alpha-glucosyl)poly((1,4)-alpha-glucosyl)glycogenin => poly{(1,4)-alpha-glucosyl} glycogenin + alpha-D-glucose"''')
        self.assertEquals(mock_callback.mock_calls, [
            call.add_xref('reactome:R-HSA-71593',
                          "((1,6)-alpha-glucosyl)poly((1,4)-alpha-glucosyl)glycogenin => poly{(1,4)-alpha-glucosyl} glycogenin + alpha-D-glucose"),
            call.xref_tag(),
        ])

    def test_should_parse_xref_tag_with_qualifiers(self):
        mock_callback = Mock()
        builder = OboLexerBuilder()
        builder.in_header = False
        OboParser(builder.new_lexer(), mock_callback).parse_line(
            '''xref: reactome:R-HSA-71593 "((1,6)-alpha-glucosyl)poly((1,4)-alpha-glucosyl)glycogenin => poly{(1,4)-alpha-glucosyl} glycogenin + alpha-D-glucose" {XXX="YYY"} ! comment''')
        self.assertEquals(mock_callback.mock_calls, [
            call.add_xref('reactome:R-HSA-71593',
                          "((1,6)-alpha-glucosyl)poly((1,4)-alpha-glucosyl)glycogenin => poly{(1,4)-alpha-glucosyl} glycogenin + alpha-D-glucose"),
            call.qualifier("XXX", "YYY"),
            call.xref_tag(),
        ])

    def test_should_parse_def_tag_with_xref_and_brackets2(self):
        mock_callback = Mock()
        builder = OboLexerBuilder()
        builder.in_header = False
        OboParser(builder.new_lexer(), mock_callback).parse_line(
            """def: "Any process that reduces the frequency, rate or extent of branch elongation involved in ureteric bud branching, the growth of a branch of the ureteric bud along its axis." [GOC:mtg_kidney_jan10]""")
        self.assertEquals(mock_callback.mock_calls, [
            call.add_xref('GOC:mtg_kidney_jan10', None),
            call.def_tag_value(
                "Any process that reduces the frequency, rate or extent of branch elongation involved in ureteric bud branching, the growth of a branch of the ureteric bud along its axis."),

        ])

    def test_should_parse_def_tag_value_pair_with_qualifiers(self):
        mock_callback = Mock()
        builder = OboLexerBuilder()
        builder.in_header = False
        OboParser(builder.new_lexer(), mock_callback).parse_line(
            '''def: "Enables the transfer of citrate, 2-hydroxy-1,2,3-propanetricarboyxlate, '''
            '''from one side of a membrane to the other." [GOC:ai,HELLO "WORLD"] {XXX="YYY"} ! some comment''')
        self.assertEquals(mock_callback.mock_calls, [
            call.add_xref('GOC:ai', None),
            call.add_xref('HELLO', 'WORLD'),
            call.qualifier("XXX", "YYY"),
            call.def_tag_value('Enables the transfer of citrate, 2-hydroxy-1,2,3-propanetricarboyxlate, '
                               'from one side of a membrane to the other.'),

        ])

    def test_should_parse_def_tag_value_pair_with_empty_xrefs(self):
        mock_callback = Mock()
        builder = OboLexerBuilder()
        builder.in_header = False
        OboParser(builder.new_lexer(), mock_callback).parse_line(
            '''def: "OK" [] {XXX="YYY"} ! some comment''')
        self.assertEquals(mock_callback.mock_calls, [
            call.qualifier("XXX", "YYY"),
            call.def_tag_value('OK'),

        ])

    def test_should_parse_typedef(self):
        mock_callback = Mock()
        OboParser(OboLexerBuilder().new_lexer(), mock_callback).parse_line("[Typedef]")
        self.assertEquals(mock_callback.mock_calls, [call.typedef()])

    def test_should_parse_term(self):
        mock_callback = Mock()
        OboParser(OboLexerBuilder().new_lexer(), mock_callback).parse_line("[Term]")
        self.assertEquals(mock_callback.mock_calls, [call.term()])
