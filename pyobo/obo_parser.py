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

    def create_yacc_parser(self):
        return yacc.yacc(module=self, debug=False, write_tables=False)

    def p_obo_file_line_tag_value_pair(self, p):
        """obo_file_line : TAG OBO_UNQUOTED_STRING"""
        self.callback.tag_value_pair(p[1], p[2])

    def p_obo_file_line_term(self, p):
        """obo_file_line : TERM"""
        self.callback.term()

    def p_obo_file_line_typedef(self, p):
        """obo_file_line : TYPEDEF"""
        self.callback.typedef()

    def parse_line(self, input):
        self.parser.parse(lexer=self.lexer, input=input)

    def parse(self, generator):
        for input in generator:
            self.parse_line(input)


if __name__ == "__main__":
    class ShowParsing:

        def __init__(self):
            pass

        def tag_value_pair(self, tag_token, value_token):
            print("single_value_tag %s %s" % (tag_token, value_token))

        def typedef(self):
            print("typedef")

        def term(self):
            print("term")


    OboParser(OboLexerBuilder().new_lexer(), ShowParsing()).parse(line for line in [
        "[TERM]",
        "tag: value",
        "[Typedef]"
    ])
