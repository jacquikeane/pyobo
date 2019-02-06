import re

import ply.yacc as yacc

from pyobo.obo_lexer import OboLexerBuilder


# todo implement p_error, to simply fail on error
class OboParser:
    tokens = OboLexerBuilder.tokens

    def __init__(self, lexer, callback):
        self.lexer = lexer
        self.parser = self.create_yacc_parser()
        self.vars = {}
        self.callback = callback
        self.pattern = re.compile("^\s*$")

    def create_yacc_parser(self):
        return yacc.yacc(module=self, debug=False, write_tables=False)

    def p_obo_file_line_tag_value_pair(self, p):
        """obo_file_line : TAG TAG_VALUE"""
        self.callback.tag_value_pair(p[1], p[2])

    def p_obo_file_line_boolean_tag_value_pair(self, p):
        """obo_file_line : TAG BOOLEAN"""
        self.callback.boolean_tag_value_pair(p[1], p[2] == 'true')

    def p_obo_file_line_tag_value_pair_with_qualifiers(self, p):
        """obo_file_line : TAG TAG_VALUE qualifier_block"""
        self.callback.tag_value_pair(p[1], p[2])

    def p_qualifier_block_single(self, p):
        """qualifier_block : QUALIFIER_ID QUALIFIER_VALUE"""
        self.callback.qualifier(p[1], p[2])

    def p_qualifier_block_multiple(self, p):
        """qualifier_block : qualifier_block QUALIFIER_ID QUALIFIER_VALUE"""
        self.callback.qualifier(p[2], p[3])

    def p_obo_file_line_term(self, p):
        """obo_file_line : TERM"""
        self.callback.term()

    def p_obo_file_line_typedef(self, p):
        """obo_file_line : TYPEDEF"""
        self.callback.typedef()

    def p_error(self, p):
        if self.pattern.match(self.input):
            return

        print("Syntax error line: %s error: %s" % (self.input, p))
        pass

    def parse_line(self, input):
        self.input = input
        self.parser.parse(lexer=self.lexer, input=input)

    def parse(self, generator):
        for input in generator:
            try:
                self.parse_line(input)
            except Exception as inst:
                # TODO register issues as part of the results
                print("Unexpected error: %s" % inst)


if __name__ == "__main__":
    class ShowParsing:

        def __init__(self):
            pass

        def boolean_tag_value_pair(self, tag_token, value_token):
            print("boolean_value_tag %s %s" % (tag_token, value_token))

        def tag_value_pair(self, tag_token, value_token):
            print("single_value_tag %s %s" % (tag_token, value_token))

        def qualifier(self, id, value):
            print("qualifier %s %s" % (id, value))

        def typedef(self):
            print("typedef")

        def term(self):
            print("term")


    OboParser(OboLexerBuilder().new_lexer(), ShowParsing()).parse(line for line in [
        "[Term]",
        "tag: value",
        "[Typedef]",
        """tag2: value2 {q1="v1"}""",
        """tag3: value3 {q2="v2", q3="v3"}""",
        """tag4: true {q1="v1"}""",
    ])
