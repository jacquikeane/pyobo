class OboParsingError(Exception):

    @staticmethod
    def lexer_error(token, position):
        result = OboParsingError()
        result.message = "Illegal character '%s' at line %s position %s" % (token.value[0], token.lineno, position)
        return result

    def __init__(self):
        pass

    def __str__(self):
        fields = ["%s=%s" % (key, self.__dict__[key]) for key in sorted(self.__dict__.keys())]
        return "%s%s" % (self.__class__.__name__, fields)
