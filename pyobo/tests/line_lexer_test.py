import unittest

from pyobo.obo_lexer import OboLexerBuilder, LineLexer
from pyobo.tests.base_test_for_lexer import BaseTestForLexer


class LineLexerTest(BaseTestForLexer, unittest.TestCase):

    def setUp(self):
        BaseTestForLexer.setUp(self)

    def lexing_module(self):
        return LineLexer()

    def begin_state(self):
        return OboLexerBuilder.LINE

    def test_should_recognise_tags_in_header(self):
        actual = self.tokenize("""a_valid_tag-AZ_8""")
        self.assert_lexing(actual, [["TAG", "a_valid_tag-AZ_8", 1, 0]],
                           push_states=[OboLexerBuilder.HEADER_VALUE, OboLexerBuilder.TAG_VALUE_SEPARATOR])

    def test_should_recognise_tags_in_stanza(self):
        self.under_test.in_header = False
        actual = self.tokenize("""a_valid_tag-AZ_8""")
        self.assert_lexing(actual, [["TAG", "a_valid_tag-AZ_8", 1, 0]],
                           push_states=[OboLexerBuilder.END_OF_LINE, OboLexerBuilder.STANZA_VALUE,
                                        OboLexerBuilder.TAG_VALUE_SEPARATOR])

    def test_should_recognise_def_tag(self):
        self.under_test.in_header = False
        actual = self.tokenize("""def""")
        self.assert_lexing(actual, [["DEF_TAG", "def", 1, 0]],
                           push_states=[OboLexerBuilder.END_OF_LINE, OboLexerBuilder.XREF_LIST,
                                        OboLexerBuilder.DEF_VALUE, OboLexerBuilder.TAG_VALUE_SEPARATOR])

    def test_should_recognise_xref_tag(self):
        self.under_test.in_header = False
        actual = self.tokenize("""xref""")
        self.assert_lexing(actual, [["XREF_TAG", "xref", 1, 0]],
                           push_states=[OboLexerBuilder.XREF, OboLexerBuilder.TAG_VALUE_SEPARATOR])

    def test_should_recognise_typedefs(self):
        actual = self.tokenize("[Typedef]")
        self.assert_lexing(actual, [["TYPEDEF", "Typedef", 1, 0]])

    def test_should_recognise_terms(self):
        actual = self.tokenize("[Term]")
        self.assert_lexing(actual, [["TERM", "Term", 1, 0]])
