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

    def p_obo_file(self, p):
        """obo_file : header_clause"""
        self.callback.obo_file()

    def p_header_clause(self, p):
        """header_clause : tag_list"""
        self.callback.header_clause()

    def p_tag_list_single(self, p):
        """tag_list : tag_definition"""
        self.callback.tag_list_single()

    def p_tag_list_multiple(self, p):
        """tag_list : tag_list tag_definition"""
        self.callback.tag_list_multiple()

    def p_tag_definition(self, p):
        """tag_definition : tag_value_pair"""
        self.callback.tag_definition()

    def p_tag_value_pair(self, p):
        """tag_value_pair : TAG OBO_UNQUOTED_STRING"""
        self.callback.tag_value_pair(p[1], p[2])

    def parse_line(self, input):
        self.parser.parse(lexer=self.lexer, input=input)

    def parse(self, generator):
        for input in generator:
            self.parse_line(input)


if __name__ == "__main__":
    class ShowParsing:

        def __init__(self):
            pass

        def obo_file(self):
            print("obo_file")

        def header_clause(self):
            print("header_clause")

        def tag_list_single(self):
            print("p_tag_list_single")

        def tag_list_multiple(self):
            print("tag_list_multiple")

        def tag_definition(self):
            print("tag_definition")

        def tag_value_pair(self, tag_token, value_token):
            print("single_value_tag %s %s" % (tag_token, value_token))


    OboParser(OboLexerBuilder().new_lexer(), ShowParsing()).parse_line("""
    format-version: 1.2
    """)
