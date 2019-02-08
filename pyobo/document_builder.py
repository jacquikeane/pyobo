from pyobo.obo_document import OboDocument, OboXref, OboDef


# todo remove print statements and simplify callbacks.
class OboDocumentBuilder:

    def __init__(self):
        self.document = OboDocument()
        self.scope = self.document.header
        self.qualifiers = {}
        self.xrefs = []

    def term(self):
        self.scope = self.document.add_term()

    def add_xref(self, xref, description):
        self.xrefs.append(OboXref(xref, description))

    def def_tag_value(self, value):
        definition = OboDef(value, self.xrefs)
        self.xrefs = []
        self.scope.def_ = definition
        self._process_qualifiers("def_")

    def typedef(self):
        self.scope = self.document.add_typedef()

    def xref_tag(self):
        if len(self.xrefs) != 1:
            raise OboDocumentBuildingError.expected_only_one_xref(self.xrefs)
        self.scope.xref = self.xrefs.pop()
        self._process_qualifiers("xref")

    def tag_value_pair(self, tag, value):
        attribute = OboDocumentBuilder._extract_attribute(tag)
        self._ensure_attribute_is_defined(attribute)
        self._set_attribute_value(tag, attribute, value)
        self._process_qualifiers(attribute)

    def _process_qualifiers(self, attribute):
        if len(self.qualifiers) > 0:
            self.scope.add_qualifiers(attribute, self.qualifiers)
            self.qualifiers = {}

    def boolean_tag_value_pair(self, tag, boolean_value):
        attribute = OboDocumentBuilder._extract_attribute(tag)
        self._set_boolean_attribute_value(tag, attribute, boolean_value)
        self._process_qualifiers(attribute)

    def qualifier(self, id, value):
        self.qualifiers[id] = value

    def _set_attribute_value(self, tag, attribute, value):
        current_value = self.scope.__dict__.get(attribute)
        if current_value is None:
            self.scope.__dict__[attribute] = value
            return
        if type(current_value) == list:
            current_value.append(value)
            return
        if current_value != value:
            raise OboDocumentBuildingError.invalid_tag_pair_merge(tag, current_value, value)

    def _set_boolean_attribute_value(self, tag, attribute, value):
        current_value = self.scope.__dict__.get(attribute)
        if current_value is None:
            self.scope.__dict__[attribute] = value
            return
        if type(current_value) == list:
            raise OboDocumentBuildingError.unexpected_boolean_value(tag, current_value, value)
        if current_value != value:
            raise OboDocumentBuildingError.invalid_tag_pair_merge(tag, current_value, value)

    def _ensure_attribute_is_defined(self, attribute):
        if attribute not in self.scope.__dict__:
            self.scope.__dict__[attribute] = []

    @staticmethod
    def _extract_attribute(tag):
        attribute = tag.replace("-", "_")
        if attribute == "version":
            return "data_version"
        if attribute == "import":
            return "import_"
        if attribute == "def":
            return "def_"
        return attribute


class OboDocumentBuildingError(Exception):

    @staticmethod
    def invalid_tag_pair_merge(tag, current, new):
        result = OboDocumentBuildingError()
        result.message = "Tag %s defined more than once with different values (%s and %s)" % (tag, current, new)
        return result

    @staticmethod
    def expected_only_one_xref(xrefs):
        result = OboDocumentBuildingError()
        result.message = "Tag xref expects an single xref defined, found %s" % xrefs
        return result

    @staticmethod
    def unexpected_boolean_value(tag, current, new):
        result = OboDocumentBuildingError()
        result.message = "Tag %s is either undefined or defined with a cardinality of many and therefore cannot " \
                         "be a boolean (%s and %s)" % (tag, current, new)
        return result

    def __init__(self):
        pass
