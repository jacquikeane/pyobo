from pyobo.document_builder import OboDocumentBuilder
from pyobo.obo_lexer import OboLexerBuilder
from pyobo.obo_parser import OboParser


def read(line_generator):
    builder = OboDocumentBuilder()
    parser = OboParser(OboLexerBuilder().new_lexer(), builder)
    parser.parse(line_generator)
    return builder.document


if __name__ == "__main__":
    print(read((line for line in ["format-version: 1.2"])))
