from pyobo.obo_document import OboDocument


# todo remove print statements and simplify callbacks.
class OboDocumentBuilder:

    def __init__(self):
        self.document = OboDocument()
        self.scope = self.document.header

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

    def tag_value_pair(self, tag, value):
        self.scope.__dict__[tag.replace("-", "_")] = value
