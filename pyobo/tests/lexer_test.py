import unittest
from functools import partial

from ply.lex import LexToken

from pyobo.obo_lexer import OboLexerBuilder
from pyobo.parsing_exception import OboParsingError


class TestLexer(unittest.TestCase):

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

    def test_should_recognise_qualifier_ids(self):
        self.under_test.in_header = False
        self.lexer.begin(OboLexerBuilder.QUALIFIER)
        actual = self.tokenize("""AvalidId""")
        expected = self.to_tokens([["QUALIFIER_ID", "AvalidId", 1, 0]])
        self.assertEqualsByContent(actual, expected)

    def test_should_not_recognise_curly_brackets_as_part_of_qualifier_id(self):
        self.under_test.in_header = False
        self.lexer.begin(OboLexerBuilder.QUALIFIER)
        actual = self.tokenize("""AvalidId}""")
        expected = self.to_tokens([["QUALIFIER_ID", "AvalidId", 1, 0],
                                   ["QUALIFIER_BLOCK_END", "}", 1, 8]])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_qualifier_values(self):
        self.under_test.in_header = False
        self.lexer.begin(OboLexerBuilder.QUALIFIER)
        actual = self.tokenize("""\"=some value,,{\"""")
        expected = self.to_tokens([["QUALIFIER_VALUE", "=some value,,{", 1, 0]])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_tags(self):
        actual = self.tokenize("""a_valid_tag-AZ_8""")
        expected = self.to_tokens([["TAG", "a_valid_tag-AZ_8", 1, 0]])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_typedefs(self):
        actual = self.tokenize("""[Typedef]""")
        expected = self.to_tokens([["TYPEDEF", "Typedef", 1, 0]])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_terms(self):
        actual = self.tokenize("""[Term]""")
        expected = self.to_tokens([["TERM", "Term", 1, 0]])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_header_tag_values(self):
        self.lexer.begin(OboLexerBuilder.HEADER_VALUE)
        actual = self.tokenize("""It can contain any characters but new lines \u0145 \\a""")
        expected = self.to_tokens([["TAG_VALUE", "It can contain any characters but new lines \u0145 \\a", 1, 0]])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_stanza_tag_values(self):
        self.lexer.begin(OboLexerBuilder.STANZA_VALUE)
        actual = self.tokenize("""It can contain any characters but new lines \u0145 \\a""")
        expected = self.to_tokens([["TAG_VALUE", "It can contain any characters but new lines \u0145 \\a", 1, 0]])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_true_tag_values_in_stanza(self):
        self.lexer.begin(OboLexerBuilder.STANZA_VALUE)
        actual = self.tokenize("""true""")
        expected = self.to_tokens([["BOOLEAN", "true", 1, 0]])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_false_tag_values_in_stanza(self):
        self.lexer.begin(OboLexerBuilder.STANZA_VALUE)
        actual = self.tokenize("""false""")
        expected = self.to_tokens([["BOOLEAN", "false", 1, 0]])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_true_tag_values_in_header(self):
        self.lexer.begin(OboLexerBuilder.HEADER_VALUE)
        actual = self.tokenize("""true""")
        expected = self.to_tokens([["BOOLEAN", "true", 1, 0]])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_false_tag_values_in_header(self):
        self.lexer.begin(OboLexerBuilder.HEADER_VALUE)
        actual = self.tokenize("""false""")
        expected = self.to_tokens([["BOOLEAN", "false", 1, 0]])
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_an_ending_comment(self):
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
        actual = self.tokenize("""  a_valid_tag-AZ_8: \tIt can contain any characters \t but new lines \u0145 \\a""")
        expected = self.to_tokens([
            ["TAG", "a_valid_tag-AZ_8", 1, 2],
            ["TAG_VALUE_SEPARATOR", ":", 1, 18],
            ["TAG_VALUE", "It can contain any characters \t but new lines \u0145 \\a", 1, 21]
        ])
        self.assertEqualsByContent(actual, expected)

    def test_should_fail_on_invalid_character(self):
        with self.assertRaises(OboParsingError):
            self.tokenize("""==:""")

    def assertEqualsByContent(self, actual, expected):
        def extract_dictionary(list):
            return [x.__dict__ for x in list]

        actual_dict = extract_dictionary(actual)
        expected_dict = extract_dictionary(expected)
        self.assertEquals(actual_dict, expected_dict)
