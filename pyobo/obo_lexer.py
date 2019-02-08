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


class BaseLexer:
    def __init__(self):
        self.current_char_count = 0
        self.tag_escape_replacement = re.compile(
            r"""(?P<discard>\\)(?:(?P<keep>[\\\(\)\[\]\{\}:,"])|(?P<blank>W)|(?P<tab>t)|(?P<newline>n))""")

    def t_newline(self, token):
        r"""\n+"""
        token.lexer.lineno += len(token.value)
        self.current_char_count = token.lexpos
        if token.lexer.lineno % 10000 == 0:
            print("Parsed %s lines so far" % token.lexer.lineno)
        if len(token.lexer.lexstatestack) > 0:
            raise OboParsingError.lexer_state_error(token)

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

    def token_position(self, token):
        return token.lexpos - self.current_char_count


class HeaderLexing(BaseLexer):

    def t_hvalue_BOOLEAN(self, token):
        r"""true|false"""
        token.lexer.pop_state()
        return token

    def t_hvalue_TAG_VALUE(self, token):
        r"""(?:(?:[^\\\r\n\u000A\u000C\u000D])|(?:\\[a-zA-Z])|(?:\\[Wtn\\\(\)\[\]\{\}:,"]))+"""
        result = self._replace_escaped_characters(token)
        token.lexer.pop_state()
        return result


class XRefLexing(BaseLexer):

    def t_xref_XREF_DESCRIPTION(self, token):
        r"""\".*?\""""
        return self._replace_escaped_characters(remove_first_and_last_char(token))

    def t_xref_XREF(self, token):
        r"""(?:(?:[^ \t\u0020\u0009\\\r\n\u000A\u000C\u000D!\{\]\}\,"])|""" \
        r"""(?:\\[a-zA-Z])|(?:\\[Wtn\\\(\)\[\]\{\}:,"]))+"""
        result = self._replace_escaped_characters(token)
        return result


class XRefListLexing(BaseLexer):
    def t_xreflist_XREF_LIST_START(self, token):
        r"""\["""
        return token

    def t_xreflist_XREF_LIST_SEPARATOR(self, token):
        r""","""
        return token

    def t_xreflist_XREF_LIST_END(self, token):
        r"""\]"""
        token.lexer.pop_state()
        return token

    def t_xreflist_XREF_DESCRIPTION(self, token):
        r"""\".*?\""""
        return self._replace_escaped_characters(remove_first_and_last_char(token))

    def t_xreflist_XREF(self, token):
        r"""(?:(?:[^ \t\u0020\u0009\\\r\n\u000A\u000C\u000D!\{\]\}\,"])|""" \
        r"""(?:\\[a-zA-Z])|(?:\\[Wtn\\\(\)\[\]\{\}:,"]))+"""
        return self._replace_escaped_characters(token)


class DefTagLexxing(BaseLexer):
    def t_defvalue_TAG_VALUE(self, token):
        r"""\"(?:(?:[^\\\r\n\u000A\u000C\u000D"])|(?:\\[a-zA-Z])|(?:\\[Wtn\\\(\)\[\]\{\}:,"]))+\""""
        result = remove_first_and_last_char(self._replace_escaped_characters(token))
        token.lexer.pop_state()
        return result


class QualifierLexing(BaseLexer):
    def t_qualifier_QUALIFIER_BLOCK_END(self, token):
        r"""}"""
        token.lexer.pop_state()
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


class StanzaValueLexing(BaseLexer):
    def t_svalue_BOOLEAN(self, token):
        r"""true|false"""
        token.lexer.pop_state()
        return token

    def t_svalue_TAG_VALUE(self, token):
        r"""(?:(?:[^\\\r\n\u000A\u000C\u000D!\{])|(?:\\[a-zA-Z])|(?:\\[Wtn\\\(\)\[\]\{\}:,"]))*(?:(?:[^ """ \
        r"""\t\u0020\u0009\\\r\n\u000A\u000C\u000D!\{])|(?:\\[a-zA-Z])|(?:\\[Wtn\\\(\)\[\]\{\}:,"]))+"""
        result = self._replace_escaped_characters(token)
        token.lexer.pop_state()
        return result


class LineLexing(BaseLexer):
    def __init__(self):
        BaseLexer.__init__(self)
        self.in_header = True

    def t_line_TAG(self, token):
        r"""(?:[-a-zA-Z0-9_@]|\\[Wtn\\\(\)\[\]\{\}:,"])+"""
        result = self._replace_escaped_characters(token)
        if self.in_header:
            token.lexer.push_state(OboLexerBuilder.HEADER_VALUE)
        else:
            if result.value == 'xref':
                result.type = 'XREF_TAG'
                token.lexer.push_state(OboLexerBuilder.XREF)  # Special case due to optional description
            else:
                token.lexer.push_state(OboLexerBuilder.END_OF_LINE)  # To capture comment and qualifiers
                if result.value == 'def':
                    result.type = 'DEF_TAG'
                    token.lexer.push_state(OboLexerBuilder.XREF_LIST)
                    token.lexer.push_state(OboLexerBuilder.DEF_VALUE)
                else:
                    token.lexer.push_state(OboLexerBuilder.STANZA_VALUE)

        token.lexer.push_state(OboLexerBuilder.LINE)  # To capture the tag value separator:
        return result

    def t_line_TYPEDEF(self, token):
        r"""\[Typedef\]"""
        self.in_header = False
        return remove_first_and_last_char(token)

    def t_line_TERM(self, token):
        r"""\[Term\]"""
        self.in_header = False
        return remove_first_and_last_char(token)


class ContextIndependentLexing(BaseLexer):
    t_ignore = " \t\u0020\u0009"

    def t_error(self, token):
        raise OboParsingError.lexer_error(token, self.token_position(token))

    def t_TAG_VALUE_SEPARATOR(self, token):
        r""":"""
        token.lexer.pop_state()
        return token


class StanzaValueEndOfLineLexing(BaseLexer):

    def __init__(self):
        BaseLexer.__init__(self)
        self.in_header = True

    def t_eol_xref_comment(self, token):
        r"""[ \t\u0020\u0009]*!.*"""
        pass

    def t_eol_xref_QUALIFIER_BLOCK_START(self, token):
        r"""{"""
        token.lexer.push_state(OboLexerBuilder.QUALIFIER)
        return token

    def t_eol_xref_newline(self, token):
        r"""\n+"""
        token.lexer.pop_state()
        self.t_newline(token)


# TODO unit tests each regex, try and factor them out
class OboLexerBuilder(ContextIndependentLexing, StanzaValueEndOfLineLexing, XRefListLexing, XRefLexing, HeaderLexing,
                      DefTagLexxing, QualifierLexing,
                      StanzaValueLexing, LineLexing):
    HEADER_VALUE = 'hvalue'
    STANZA_VALUE = 'svalue'
    DEF_VALUE = 'defvalue'
    QUALIFIER = 'qualifier'
    XREF = 'xref'
    XREF_LIST = 'xreflist'
    LINE = 'line'
    END_OF_LINE = 'eol'

    states = (
        ('hvalue', 'inclusive'),
        ('svalue', 'inclusive'),
        ('defvalue', 'inclusive'),
        ('qualifier', 'inclusive'),
        ('xref', 'inclusive'),
        ('xreflist', 'inclusive'),
        ('line', 'inclusive'),
        ('eol', 'inclusive'),
    )

    tokens = ['TAG', 'DEF_TAG', 'XREF_TAG', 'TAG_VALUE', 'TERM', 'TYPEDEF', 'QUALIFIER_ID', 'QUALIFIER_VALUE',
              'BOOLEAN',
              'TAG_VALUE_SEPARATOR', 'QUALIFIER_BLOCK_START', 'QUALIFIER_BLOCK_END', 'QUALIFIER_ID_VALUE_SEPARATOR',
              'QUALIFIER_LIST_SEPARATOR', 'XREF_LIST_START', 'XREF_LIST_END', 'XREF_LIST_SEPARATOR', 'XREF_DESCRIPTION',
              'XREF']

    def __init__(self):
        LineLexing.__init__(self)

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

    def new_lexer(self, **kwargs):
        lexer = lex.lex(module=self, reflags=re.UNICODE, **kwargs)
        lexer.begin(OboLexerBuilder.LINE)
        return lexer

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
