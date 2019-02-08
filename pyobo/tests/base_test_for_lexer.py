import abc
import re
from itertools import repeat
from unittest.mock import Mock, call

import ply.lex as lex
from ply.lex import LexToken


class BaseTestForLexer:

    def setUp(self):
        self.under_test = self.lexing_module()
        # TOO hack t_error to avoid warning
        lexer = lex.lex(module=self.under_test, reflags=re.UNICODE)
        self.push_state = Mock()
        self.pop_state = Mock()
        lexer.push_state = self.push_state
        lexer.pop_state = self.pop_state
        self.lexer = lexer

    @abc.abstractmethod
    def lexing_module(self):
        return

    @abc.abstractmethod
    def begin_state(self):
        return

    def tokenize(self, string):
        self.lexer.begin(self.begin_state())
        self.lexer.input(string)
        result = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            result.append(tok)
        return result

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

    def assert_lexing(self, actual, expected_tokens, push_states=[], pop_states=0):
        self._assertEqualsByContent(actual, self.to_tokens(expected_tokens))
        self.assertEquals(self.push_state.mock_calls, [call(state) for state in push_states])
        self.assertEquals(self.pop_state.mock_calls, list(repeat(call(), pop_states)))

    def _assertEqualsByContent(self, actual, expected):
        def extract_dictionary(list):
            return [x.__dict__ for x in list]

        actual_dict = extract_dictionary(actual)
        expected_dict = extract_dictionary(expected)
        self.assertEquals(actual_dict, expected_dict)
