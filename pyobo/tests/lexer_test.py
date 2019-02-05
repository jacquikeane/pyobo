import unittest

from ply.lex import LexToken

from pyobo.obo_lexer import OboLexerBuilder


def to_token(lexer, type, value, line, position):
    token = LexToken()
    token.type = type
    token.value = value
    token.lineno = line
    token.lexpos = position
    token.lexer = lexer
    return token


def extract_dictionary(list):
    return [x.__dict__ for x in list]


class TestLexer(unittest.TestCase):

    def test_should_recognise_qualifier_ids(self):
        builder = OboLexerBuilder()
        builder.in_header = False
        lexer = builder.new_lexer()
        lexer.begin(OboLexerBuilder.QUALIFIER)
        actual = builder.tokenize(lexer, """AvalidId=""")
        expected = [to_token(lexer, "QUALIFIER_ID", "AvalidId", 1, 0)]
        self.assertEqualsByContent(actual, expected)

    def test_should_not_recognise_curly_brackets_as_part_of_qualifier_id(self):
        builder = OboLexerBuilder()
        builder.in_header = False
        lexer = builder.new_lexer()
        lexer.begin(OboLexerBuilder.QUALIFIER)
        actual = builder.tokenize(lexer, """AvalidId}""")
        expected = [to_token(lexer, "QUALIFIER_ID", "AvalidId", 1, 0)]
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_qualifier_values(self):
        builder = OboLexerBuilder()
        builder.in_header = False
        lexer = builder.new_lexer()
        lexer.begin(OboLexerBuilder.QUALIFIER)
        actual = builder.tokenize(lexer, """\"=some value,,{\"""")
        expected = [to_token(lexer, "QUALIFIER_VALUE", "=some value,,{", 1, 0)]
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_tags(self):
        lexer = OboLexerBuilder().new_lexer()
        actual = OboLexerBuilder().tokenize(lexer, """a_valid_tag-AZ_8:""")
        expected = [to_token(lexer, "TAG", "a_valid_tag-AZ_8", 1, 0)]
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_typedefs(self):
        lexer = OboLexerBuilder().new_lexer()
        actual = OboLexerBuilder().tokenize(lexer, """[Typedef]""")
        expected = [to_token(lexer, "TYPEDEF", "Typedef", 1, 0)]
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_terms(self):
        lexer = OboLexerBuilder().new_lexer()
        actual = OboLexerBuilder().tokenize(lexer, """[Term]""")
        expected = [to_token(lexer, "TERM", "Term", 1, 0)]
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_obo_strings(self):
        lexer = OboLexerBuilder().new_lexer()
        lexer.begin(OboLexerBuilder.HEADER_VALUE)
        actual = OboLexerBuilder().tokenize(lexer, """It can contain any characters but new lines \u0145 \\a""")
        expected = [to_token(lexer, "OBO_UNQUOTED_STRING",
                             "It can contain any characters but new lines \u0145 \\a", 1, 0)]
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_an_ending_comment(self):
        builder = OboLexerBuilder()
        lexer = builder.new_lexer()
        builder.in_header = False
        actual = builder.tokenize(lexer, """is_a: RO:0002323 ! mereotopologically related to""")
        expected = [to_token(lexer, "TAG",
                             "is_a", 1, 0),
                    to_token(lexer, "OBO_UNQUOTED_STRING",
                             "RO:0002323", 1, 6)
                    ]
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_qualifiers_without_comments(self):
        builder = OboLexerBuilder()
        lexer = builder.new_lexer()
        builder.in_header = False
        actual = builder.tokenize(lexer,
                                  """range: BFO:0000004 {http://purl.obolibrary.org/obo/IAO_0000116="This is """
                                  + """redundant with the more specific 'independent and not spatial region' """
                                  + """constraint. We leave in the redundant axiom for use with reasoners that do """
                                  + """not use negation.",  XXX="YYY"}""")
        expected = [to_token(lexer, "TAG", "range", 1, 0),
                    to_token(lexer, "OBO_UNQUOTED_STRING", "BFO:0000004", 1, 7),
                    to_token(lexer, "QUALIFIER_ID", "http://purl.obolibrary.org/obo/IAO_0000116", 1, 20),
                    to_token(lexer, "QUALIFIER_VALUE",
                             "This is redundant with the more specific 'independent and not spatial region' "
                             + "constraint. We leave in the redundant axiom for use with reasoners that do not "
                             + "use negation.", 1, 63),
                    to_token(lexer, "QUALIFIER_ID",
                             "XXX", 1, 238),
                    to_token(lexer, "QUALIFIER_VALUE",
                             "YYY", 1, 242)
                    ]
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_single_qualifier_without_comments(self):
        builder = OboLexerBuilder()
        lexer = builder.new_lexer()
        builder.in_header = False
        actual = builder.tokenize(lexer,
                                  """range: BFO:0000004 {http://purl.obolibrary.org/obo/IAO_0000116="This is """
                                  + """redundant with the more specific 'independent and not spatial region' """
                                  + """constraint. We leave in the redundant axiom for use with reasoners that do """
                                  + """not use negation."}""")
        expected = [to_token(lexer, "TAG", "range", 1, 0),
                    to_token(lexer, "OBO_UNQUOTED_STRING", "BFO:0000004", 1, 7),
                    to_token(lexer, "QUALIFIER_ID", "http://purl.obolibrary.org/obo/IAO_0000116", 1, 20),
                    to_token(lexer, "QUALIFIER_VALUE",
                             "This is redundant with the more specific 'independent and not spatial region' "
                             + "constraint. We leave in the redundant axiom for use with reasoners that do not "
                             + "use negation.", 1, 63)
                    ]
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_qualifiers_with_comments(self):
        builder = OboLexerBuilder()
        lexer = builder.new_lexer()
        builder.in_header = False
        actual = OboLexerBuilder().tokenize(lexer,
                                            """range: BFO:0000004 {http://purl.obolibrary.org/obo/IAO_0000116="This """
                                            + """is redundant with the more specific 'independent and not spatial """
                                            + """region' constraint. We leave in the redundant axiom for use with """
                                            + """reasoners that do not use negation."} ! independent continuant""")
        expected = [to_token(lexer, "TAG", "range", 1, 0),
                    to_token(lexer, "OBO_UNQUOTED_STRING", "BFO:0000004", 1, 7),
                    to_token(lexer, "QUALIFIER_ID", "http://purl.obolibrary.org/obo/IAO_0000116", 1, 20),
                    to_token(lexer, "QUALIFIER_VALUE",
                             "This is redundant with the more specific 'independent and not spatial region' constraint."
                             + " We leave in the redundant axiom for use with reasoners that do not use negation.", 1,
                             63)
                    ]
        self.assertEqualsByContent(actual, expected)

    def test_should_recognise_new_lines(self):
        lexer = OboLexerBuilder().new_lexer()
        actual = OboLexerBuilder().tokenize(lexer, """
        a_valid_tag-AZ_8:""")
        expected = [to_token(lexer, "TAG", "a_valid_tag-AZ_8", 2, 9)]
        self.assertEqualsByContent(actual, expected)

    def test_should_ignore_spaces_and_tab(self):
        lexer = OboLexerBuilder().new_lexer()
        actual = OboLexerBuilder().tokenize(lexer, """  a_valid_tag-AZ_8: \t"""
                                            + """It can contain any characters \t but new lines \u0145 \\a""")
        expected = [
            to_token(lexer, "TAG", "a_valid_tag-AZ_8", 1, 2),
            to_token(lexer, "OBO_UNQUOTED_STRING", "It can contain any characters \t but new lines \u0145 \\a", 1, 21)]
        self.assertEqualsByContent(actual, expected)

    def test_should_skip_an_invalid_character(self):
        lexer = OboLexerBuilder().new_lexer()
        actual = OboLexerBuilder().tokenize(lexer, """==:""")
        # TODO Register lexer errors so they can be reported
        self.assertEqualsByContent(actual, [])

    def assertEqualsByContent(self, actual, expected):
        actual_dict = extract_dictionary(actual)
        expected_dict = extract_dictionary(expected)
        self.assertEquals(actual_dict, expected_dict)
