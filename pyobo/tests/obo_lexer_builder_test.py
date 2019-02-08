import unittest
from functools import partial

from ply.lex import LexToken

from pyobo.obo_lexer import OboLexerBuilder


class OboLexerBuilderTest(unittest.TestCase):

    def setUp(self):
        self.under_test = OboLexerBuilder()
        self.lexer = self.under_test.new_lexer()
        self.tokenize = partial(self.under_test.tokenize, self.lexer)

    def to_tokens(self, token_list):
        result = []
        for values in token_list:
            token = LexToken()
            token.type = values[0]
            token.value = values[1]
            token.lineno = values[2]
            token.lexpos = values[3]
            token.lexer = self.lexer
            result.append(token)
        return result

    def test_should_recognise_a_tag_and_ignore_an_ending_comment(self):
        self.under_test.in_header = False
        actual = self.tokenize("""is_a: RO:0002323 ! mereotopologically related to""")
        expected = self.to_tokens([["TAG", "is_a", 1, 0],
                                   ["TAG_VALUE_SEPARATOR", ":", 1, 4],
                                   ["TAG_VALUE", "RO:0002323", 1, 6]
                                   ])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_qualifiers_without_comments(self):
        self.under_test.in_header = False
        actual = self.tokenize("""range: BFO:0000004 {http://purl.obolibrary.org/obo/IAO_0000116="This is """
                               """redundant with the more specific 'independent and not spatial region' """
                               """constraint. We leave in the redundant axiom for use with reasoners that do """
                               """not use negation.",  XXX="YYY"}""")
        expected = self.to_tokens([["TAG", "range", 1, 0],
                                   ["TAG_VALUE_SEPARATOR", ":", 1, 5],
                                   ["TAG_VALUE", "BFO:0000004", 1, 7],
                                   ["QUALIFIER_BLOCK_START", "{", 1, 19],
                                   ["QUALIFIER_ID", "http://purl.obolibrary.org/obo/IAO_0000116", 1, 20],
                                   ["QUALIFIER_ID_VALUE_SEPARATOR", "=", 1, 62],
                                   ["QUALIFIER_VALUE",
                                    "This is redundant with the more specific 'independent and not spatial region' "
                                    "constraint. We leave in the redundant axiom for use with reasoners that do not "
                                    "use negation.", 1, 63],
                                   ["QUALIFIER_LIST_SEPARATOR", ",", 1, 235],
                                   ["QUALIFIER_ID", "XXX", 1, 238],
                                   ["QUALIFIER_ID_VALUE_SEPARATOR", "=", 1, 241],
                                   ["QUALIFIER_VALUE", "YYY", 1, 242],
                                   ["QUALIFIER_BLOCK_END", "}", 1, 247],
                                   ])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_def_tag(self):
        self.under_test.in_header = False
        actual = self.tokenize('''def: "some \\"value" [SOMEID "description", ANOTHERID] {qualifier="quality"}''')
        expected = self.to_tokens([["DEF_TAG", "def", 1, 0],
                                   ["TAG_VALUE_SEPARATOR", ":", 1, 3],
                                   ["TAG_VALUE", "some \"value", 1, 5],
                                   ["XREF_LIST_START", "[", 1, 20],
                                   ["XREF", "SOMEID", 1, 21],
                                   ["XREF_DESCRIPTION", "description", 1, 28],
                                   ["XREF_LIST_SEPARATOR", ",", 1, 41],
                                   ["XREF", "ANOTHERID", 1, 43],
                                   ["XREF_LIST_END", "]", 1, 52],
                                   ["QUALIFIER_BLOCK_START", "{", 1, 54],
                                   ["QUALIFIER_ID", "qualifier", 1, 55],
                                   ["QUALIFIER_ID_VALUE_SEPARATOR", "=", 1, 64],
                                   ["QUALIFIER_VALUE", "quality", 1, 65],
                                   ["QUALIFIER_BLOCK_END", "}", 1, 74],
                                   ])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_xref_tag(self):
        self.under_test.in_header = False
        actual = self.tokenize(
            '''xref: reactome:R-HSA-71593 "((1,6)-alpha-glucosyl)poly((1,4)-alpha-glucosyl)glycogenin => poly{(1,4)-alpha-glucosyl} glycogenin + alpha-D-glucose"''')
        expected = self.to_tokens([["XREF_TAG", "xref", 1, 0],
                                   ["TAG_VALUE_SEPARATOR", ":", 1, 4],
                                   ["XREF", "reactome:R-HSA-71593", 1, 6],
                                   ["XREF_DESCRIPTION",
                                    "((1,6)-alpha-glucosyl)poly((1,4)-alpha-glucosyl)glycogenin => poly{(1,4)-alpha-glucosyl} glycogenin + alpha-D-glucose",
                                    1, 27],
                                   ])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_single_qualifier_without_comments(self):
        self.under_test.in_header = False
        actual = self.tokenize("""range: BFO:0000004 {http://purl.obolibrary.org/obo/IAO_0000116="This is """
                               """redundant with the more specific 'independent and not spatial region' """
                               """constraint. We leave in the redundant axiom for use with reasoners that do """
                               """not use negation."}""")
        expected = self.to_tokens([["TAG", "range", 1, 0],
                                   ["TAG_VALUE_SEPARATOR", ":", 1, 5],
                                   ["TAG_VALUE", "BFO:0000004", 1, 7],
                                   ["QUALIFIER_BLOCK_START", "{", 1, 19],
                                   ["QUALIFIER_ID", "http://purl.obolibrary.org/obo/IAO_0000116", 1, 20],
                                   ["QUALIFIER_ID_VALUE_SEPARATOR", "=", 1, 62],
                                   ["QUALIFIER_VALUE",
                                    "This is redundant with the more specific 'independent and not spatial region' "
                                    "constraint. We leave in the redundant axiom for use with reasoners that do not "
                                    "use negation.", 1, 63],
                                   ["QUALIFIER_BLOCK_END", "}", 1, 235],
                                   ])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_qualifiers_with_comments(self):
        self.under_test.in_header = False
        actual = self.tokenize("""range: BFO:0000004 {http://purl.obolibrary.org/obo/IAO_0000116="This """
                               """is redundant with the more specific 'independent and not spatial """
                               """region' constraint. We leave in the redundant axiom for use with """
                               """reasoners that do not use negation."} ! independent continuant""")
        expected = self.to_tokens([
            ["TAG", "range", 1, 0],
            ["TAG_VALUE_SEPARATOR", ":", 1, 5],
            ["TAG_VALUE", "BFO:0000004", 1, 7],
            ["QUALIFIER_BLOCK_START", "{", 1, 19],
            ["QUALIFIER_ID", "http://purl.obolibrary.org/obo/IAO_0000116", 1, 20],
            ["QUALIFIER_ID_VALUE_SEPARATOR", "=", 1, 62],
            ["QUALIFIER_VALUE",
             "This is redundant with the more specific 'independent and not spatial region' constraint."
             " We leave in the redundant axiom for use with reasoners that do not use negation.", 1, 63],
            ["QUALIFIER_BLOCK_END", "}", 1, 235],
        ])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_new_lines(self):
        actual = self.tokenize("""
        a_valid_tag-AZ_8""")
        expected = self.to_tokens([["TAG", "a_valid_tag-AZ_8", 2, 9]])
        self.assertEqualsByContent(actual, expected)

    def test_should_ignore_spaces_and_tab(self):
        actual = self.tokenize(""" \t a_valid_tag-AZ_8: \tIt can contain any characters \t but new lines \u0145 \\a""")
        expected = self.to_tokens([
            ["TAG", "a_valid_tag-AZ_8", 1, 3],
            ["TAG_VALUE_SEPARATOR", ":", 1, 19],
            ["TAG_VALUE", "It can contain any characters \t but new lines \u0145 \\a", 1, 22]
        ])
        self.assertEqualsByContent(actual, expected)

    def assertEqualsByContent(self, actual, expected):
        def extract_dictionary(list):
            return [x.__dict__ for x in list]

        actual_dict = extract_dictionary(actual)
        expected_dict = extract_dictionary(expected)
        self.assertEquals(actual_dict, expected_dict)
