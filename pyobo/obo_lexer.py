import re

import ply.lex as lex
from ply.lex import LexToken

from pyobo.parsing_exception import OboParsingError


def correct_tag_name(original):
    token = LexToken()
    token.type = original.type
    token.value = original.value[:-1]
    token.lineno = original.lineno
    token.lexpos = original.lexpos
    token.lexer = original.lexer
    return token


def correct_stanza_name(original):
    token = LexToken()
    token.type = original.type
    token.value = original.value[1:-1]
    token.lineno = original.lineno
    token.lexpos = original.lexpos
    token.lexer = original.lexer
    return token


class OboLexerBuilder:
    HEADER_VALUE = 'hvalue'
    STANZA_VALUE = 'svalue'
    QUALIFIER = 'qualifier'

    states = (
        ('hvalue', 'exclusive'),
        ('svalue', 'exclusive'),
        ('qualifier', 'exclusive'),
    )

    tokens = ['TAG', 'TAG_VALUE', 'TERM', 'TYPEDEF', 'QUALIFIER_ID', 'QUALIFIER_VALUE', 'BOOLEAN',
              'TAG_VALUE_SEPARATOR', 'QUALIFIER_BLOCK_START', 'QUALIFIER_BLOCK_END', 'QUALIFIER_ID_VALUE_SEPARATOR',
              'QUALIFIER_LIST_SEPARATOR']

    t_ignore = " \t\u0020\u0009"

    t_svalue_ignore = " \t\u0020\u0009"

    t_hvalue_ignore = " \t\u0020\u0009"
    t_qualifier_ignore = " \t\u0020\u0009"


    def __init__(self):
        self.current_char_count = 0
        self.in_header = True

    def t_newline(self, token):
        r"""\n+"""
        token.lexer.lineno += len(token.value)
        self.current_char_count = token.lexpos
        if token.lexer.lineno % 10000 == 0:
            print("Parsed %s lines so far" % token.lexer.lineno)

    def t_hvalue_newline(self, token):
        r"""\n+"""
        self.t_newline(token)

    def t_svalue_newline(self, token):
        r"""\n+"""
        self.t_newline(token)

    def t_qualifier_newline(self, token):
        r"""\n+"""
        self.t_newline(token)

    def t_TAG(self, token):
        r"""[a-zA-Z0-9_-]+"""
        return token

    def t_TAG_VALUE_SEPARATOR(self, token):
        r""":"""
        token.lexer.begin(OboLexerBuilder.HEADER_VALUE if self.in_header else OboLexerBuilder.STANZA_VALUE)
        return token

    def t_TYPEDEF(self, token):
        r"""\[Typedef\]"""
        self.in_header = False
        return correct_stanza_name(token)

    def t_TERM(self, token):
        r"""\[Term\]"""
        self.in_header = False
        return correct_stanza_name(token)

    def t_hvalue_BOOLEAN(self, token):
        r"""true|false"""
        token.lexer.begin('INITIAL')
        return token

    def t_svalue_BOOLEAN(self, token):
        r"""true|false"""
        token.lexer.begin('INITIAL')
        return token

    def t_hvalue_TAG_VALUE(self, token):
        r"""(?:(?:[^\\\r\n\u000A\u000C\u000D])|(?:\\[a-zA-Z]))+"""
        token.lexer.begin('INITIAL')
        return token

    def t_svalue_TAG_VALUE(self, token):
        r"""(?:(?:[^\\\r\n\u000A\u000C\u000D!\{])|(?:\\[a-zA-Z]))*(?:(?:[^ \t\u0020\u0009\\\r\n\u000A\u000C\u000D!\{])|(?:\\[a-zA-Z]))+"""
        token.lexer.begin('INITIAL')
        return token

    def t_comment(self, token):
        r"""[ \t\u0020\u0009]*!.*"""
        pass

    def t_QUALIFIER_BLOCK_START(self, token):
        r"""{"""
        token.lexer.begin(OboLexerBuilder.QUALIFIER)
        return token

    def t_qualifier_QUALIFIER_BLOCK_END(self, token):
        r"""}"""
        token.lexer.begin('INITIAL')
        return token

    def t_qualifier_QUALIFIER_VALUE(selfself, token):
        r"""\".*?\""""
        return correct_stanza_name(token)

    def t_qualifier_QUALIFIER_ID_VALUE_SEPARATOR(selfself, token):
        r"""="""
        return token

    def t_qualifier_QUALIFIER_LIST_SEPARATOR(selfself, token):
        r""","""
        return token

    def t_qualifier_QUALIFIER_ID(selfself, token):
        r"""(?:(?:[^ \t\u0020\u0009\\\r\n\u000A\u000C\u000D=,{}])|(?:\\[a-zA-Z]))+"""
        return token


    def t_error(self, token):
        raise OboParsingError.lexer_error(token, self.token_position(token))

    def t_svalue_error(self, token):
        self.t_error(token)

    def t_hvalue_error(self, token):
        self.t_error(token)

    def t_qualifier_error(self, token):
        self.t_error(token)

    def token_position(self, token):
        return token.lexpos - self.current_char_count

    def new_lexer(self, **kwargs):
        return lex.lex(module=self, reflags=re.UNICODE, **kwargs)

    def tokenize(self, lexer, input):
        return list(self._new_generator(lexer, input))

    def _new_generator(self, lexer, input):
        lexer.input(input)

        def token_generator():
            while True:
                tok = lexer.token()
                if not tok:
                    break
                yield tok

        return token_generator()


if __name__ == "__main__":
    lexer = OboLexerBuilder().new_lexer()
    lexer.input("""
    format-version: 1.2
    [Term]
    ID: 1.1
    [Typedef]
    ID: 1.3 {qualifier="quality"}
    is_obsolete: false {qualifier1="quality1", qualifier2="quality2"}
    [Typedef]
    
    """)
    print("Begin")
    while True:
        tok = lexer.token()
        if not tok:
            print("End")
            break
        print(tok)
