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
        attribute = OboDocumentBuilder._extract_attribute(tag)
        self._ensure_attribute_is_defined(attribute)
        self._set_attribute_value(tag, attribute, value)

    def _set_attribute_value(self, tag, attribute, value):
        current_value = self.scope.__dict__.get(attribute)
        if current_value is None:
            self.scope.__dict__[attribute] = value
            return
        if type(current_value) == list:
            current_value.append(value)
            return
        if current_value != value:
            raise OboDocumentBuildingError.invalidTagPairMerge(tag, current_value, value)

    def _ensure_attribute_is_defined(self, attribute):
        if attribute not in self.scope.__dict__:
            self.scope.__dict__[attribute] = []

    @staticmethod
    def _extract_attribute(tag):
        attribute = tag.replace("-", "_")
        if attribute == "version":
            attribute = "data_version"
        return attribute


class OboDocumentBuildingError(Exception):

    @staticmethod
    def invalidTagPairMerge(tag, current, new):
        result = OboDocumentBuildingError()
        result.message = "Tag %s defined more than once with different values (%s and %s)" % (tag, current, new)
        return result

    def __init__(self):
        pass
