class OboParsingError(Exception):

    @staticmethod
    def lexer_error(token, position):
        result = OboParsingError()
        result.message = "Illegal character '%s' at line %s position %s" % (token.value[0], token.lineno, position)
        return result

    @staticmethod
    def lexer_state_error(token):
        result = OboParsingError()
        result.message = "Illegal lexer state at line %s, stack should be empty. Current state is %s, stack is %s" % (
        token.lineno, token.lexer.lexstate, token.lexer.lexstatestack)
        return result

    def __init__(self):
        pass

    def __str__(self):
        fields = ["%s=%s" % (key, self.__dict__[key]) for key in sorted(self.__dict__.keys())]
        return "%s%s" % (self.__class__.__name__, fields)
