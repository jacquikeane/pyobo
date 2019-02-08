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


def remove_first_and_last_char(original):
    token = LexToken()
    token.type = original.type
    token.value = original.value[1:-1]
    token.lineno = original.lineno
    token.lexpos = original.lexpos
    token.lexer = original.lexer
    return token


# TODO unit tests each regex, try and factor them out
class OboLexerBuilder:
    HEADER_VALUE = 'hvalue'
    STANZA_VALUE = 'svalue'
    DEF_VALUE = 'defvalue'
    QUALIFIER = 'qualifier'
    XREF = 'xref'

    states = (
        ('hvalue', 'exclusive'),
        ('svalue', 'exclusive'),
        ('defvalue', 'exclusive'),
        ('qualifier', 'exclusive'),
        ('xref', 'exclusive'),
    )

    tokens = ['TAG', 'DEF_TAG', 'XREF_TAG', 'TAG_VALUE', 'TERM', 'TYPEDEF', 'QUALIFIER_ID', 'QUALIFIER_VALUE',
              'BOOLEAN',
              'TAG_VALUE_SEPARATOR', 'QUALIFIER_BLOCK_START', 'QUALIFIER_BLOCK_END', 'QUALIFIER_ID_VALUE_SEPARATOR',
              'QUALIFIER_LIST_SEPARATOR', 'XREF_LIST_START', 'XREF_LIST_END', 'XREF_LIST_SEPARATOR', 'XREF_DESCRIPTION',
              'XREF']

    t_ignore = " \t\u0020\u0009"

    t_defvalue_ignore = " \t\u0020\u0009"
    t_svalue_ignore = " \t\u0020\u0009"
    t_xref_ignore = " \t\u0020\u0009"

    t_hvalue_ignore = " \t\u0020\u0009"
    t_qualifier_ignore = " \t\u0020\u0009"

    def __init__(self):
        self.current_char_count = 0
        self.in_header = True
        self.tag_escape_replacement = re.compile(
            r"""(?P<discard>\\)(?:(?P<keep>[\\\(\)\[\]\{\}:,"])|(?P<blank>W)|(?P<tab>t)|(?P<newline>n))""")
        self.current_tag = None

    def t_newline(self, token):
        r"""\n+"""
        token.lexer.begin('INITIAL')
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

    def t_xref_newline(self, token):
        r"""\n+"""
        self.t_newline(token)

    def t_qualifier_newline(self, token):
        r"""\n+"""
        self.t_newline(token)

    def t_TAG(self, token):
        r"""(?:[-a-zA-Z0-9_@]|\\[Wtn\\\(\)\[\]\{\}:,"])+"""
        result = self._replace_escaped_characters(token)
        self.current_tag = result.value
        if result.value == 'def':
            result.type = 'DEF_TAG'
        if result.value == 'xref':
            result.type = 'XREF_TAG'
        return result

    def _replace_escaped_characters(self, original):
        def replace_escape(matchobj):
            if matchobj.group("newline"):
                return '\n'
            if matchobj.group("blank"):
                return ' '
            if matchobj.group("keep"):
                return matchobj.group("keep")
            if matchobj.group("tab"):
                return '\t'

            return None

        token = LexToken()
        token.type = original.type
        token.value = self.tag_escape_replacement.sub(replace_escape, original.value)
        token.lineno = original.lineno
        token.lexpos = original.lexpos
        token.lexer = original.lexer
        return token

    def t_TAG_VALUE_SEPARATOR(self, token):
        r""":"""
        if self.in_header:
            lexer_type = OboLexerBuilder.HEADER_VALUE
        else:
            if self.current_tag == "def":
                lexer_type = OboLexerBuilder.DEF_VALUE
            else:
                if self.current_tag == "xref":
                    lexer_type = OboLexerBuilder.XREF
                else:
                    lexer_type = OboLexerBuilder.STANZA_VALUE
        token.lexer.begin(lexer_type)
        self.current_tag = None
        return token

    def t_TYPEDEF(self, token):
        r"""\[Typedef\]"""
        self.in_header = False
        return remove_first_and_last_char(token)

    def t_TERM(self, token):
        r"""\[Term\]"""
        self.in_header = False
        return remove_first_and_last_char(token)

    def t_hvalue_BOOLEAN(self, token):
        r"""true|false"""
        return token

    def t_svalue_BOOLEAN(self, token):
        r"""true|false"""
        return token

    def t_hvalue_TAG_VALUE(self, token):
        r"""(?:(?:[^\\\r\n\u000A\u000C\u000D])|(?:\\[a-zA-Z])|(?:\\[Wtn\\\(\)\[\]\{\}:,"]))+"""
        return self._replace_escaped_characters(token)

    def t_svalue_TAG_VALUE(self, token):
        r"""(?:(?:[^\\\r\n\u000A\u000C\u000D!\{])|(?:\\[a-zA-Z])|(?:\\[Wtn\\\(\)\[\]\{\}:,"]))*(?:(?:[^ """ \
        r"""\t\u0020\u0009\\\r\n\u000A\u000C\u000D!\{])|(?:\\[a-zA-Z])|(?:\\[Wtn\\\(\)\[\]\{\}:,"]))+"""
        return self._replace_escaped_characters(token)

    def t_defvalue_TAG_VALUE(self, token):
        r"""\"(?:(?:[^\\\r\n\u000A\u000C\u000D"])|(?:\\[a-zA-Z])|(?:\\[Wtn\\\(\)\[\]\{\}:,"]))+\""""
        return remove_first_and_last_char(self._replace_escaped_characters(token))

    def t_svalue_comment(self, token):
        r"""[ \t\u0020\u0009]*!.*"""
        pass

    def t_defvalue_XREF_LIST_START(self, token):
        r"""\["""
        token.lexer.begin(OboLexerBuilder.XREF)
        return token

    def t_xref_XREF_LIST_SEPARATOR(self, token):
        r""","""
        return token

    def t_xref_XREF_LIST_END(self, token):
        r"""\]"""
        token.lexer.begin(OboLexerBuilder.STANZA_VALUE)
        return token

    def t_xref_XREF_DESCRIPTION(self, token):
        r"""\".*?\""""
        return self._replace_escaped_characters(remove_first_and_last_char(token))

    def t_xref_XREF(self, token):
        r"""(?:(?:[^ \t\u0020\u0009\\\r\n\u000A\u000C\u000D!\{\]\}\,"])|""" \
        r"""(?:\\[a-zA-Z])|(?:\\[Wtn\\\(\)\[\]\{\}:,"]))+"""
        return self._replace_escaped_characters(token)

    def t_xref_QUALIFIER_BLOCK_START(self, token):
        r"""{"""
        token.lexer.begin(OboLexerBuilder.QUALIFIER)
        return token

    def t_svalue_QUALIFIER_BLOCK_START(self, token):
        r"""{"""
        token.lexer.begin(OboLexerBuilder.QUALIFIER)
        return token

    def t_qualifier_QUALIFIER_BLOCK_END(self, token):
        r"""}"""
        token.lexer.begin(OboLexerBuilder.STANZA_VALUE)
        return token

    def t_qualifier_QUALIFIER_VALUE(self, token):
        r"""\".*?\""""
        return remove_first_and_last_char(token)

    def t_qualifier_QUALIFIER_ID_VALUE_SEPARATOR(self, token):
        r"""="""
        return token

    def t_qualifier_QUALIFIER_LIST_SEPARATOR(self, token):
        r""","""
        return token

    def t_qualifier_QUALIFIER_ID(self, token):
        r"""(?:(?:[^ \t\u0020\u0009\\\r\n\u000A\u000C\u000D=,{}])|(?:\\[a-zA-Z]))+"""
        return token

    # \n  newline
    # \W single space
    # \t tab
    # \: colon
    # \, comma
    # \" double quote
    # \\ backslash
    # \( open parenthesis
    # \) close parenthesis
    # \[ open bracket
    # \] close bracket
    # \{ open brace
    # \} close brace
    # @ at (language tag)
    # \<newline>

    def t_error(self, token):
        raise OboParsingError.lexer_error(token, self.token_position(token))

    def t_svalue_error(self, token):
        self.t_error(token)

    def t_defvalue_error(self, token):
        self.t_error(token)

    def t_hvalue_error(self, token):
        self.t_error(token)

    def t_qualifier_error(self, token):
        self.t_error(token)

    def t_xref_error(self, token):
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
