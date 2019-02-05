import re

import ply.lex as lex
from ply.lex import LexToken


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
    states = (
        ('value', 'exclusive'),
    )

    tokens = ['TAG', 'OBO_UNQUOTED_STRING', 'TERM', 'TYPEDEF']

    t_ignore = " \t\u0020\u0009"

    t_value_ignore = " \t\u0020\u0009"

    def __init__(self):
        self.current_char_count = 0

    def t_newline(self, token):
        r"""\n+"""
        token.lexer.lineno += len(token.value)
        self.current_char_count = token.lexpos

    def t_value_newline(self, token):
        r"""\n+"""
        self.t_newline(token)

    def t_TAG(self, token):
        r"""[a-zA-Z0-9_-]+:"""
        token.lexer.begin('value')
        return correct_tag_name(token)

    def t_TYPEDEF(self, token):
        r"""\[Typedef\]"""
        return correct_stanza_name(token)

    def t_TERM(self, token):
        r"""\[Term\]"""
        return correct_stanza_name(token)

    def t_value_OBO_UNQUOTED_STRING(self, token):
        r"""(?:(?:[^\\\r\n\u000A\u000C\u000D])|(?:\\[a-zA-Z]))+"""
        token.lexer.begin('INITIAL')
        return token

    def t_error(self, token):
        print("Illegal character '%s' at line %s position %s" % (token.value[0], token.lineno,
                                                                 self.token_position(token)))
        token.lexer.skip(1)

    def t_value_error(self, token):
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
    ID: 1.3
    
    """)
    print("Begin")
    while True:
        tok = lexer.token()
        if not tok:
            print("End")
            break
        print(tok)
