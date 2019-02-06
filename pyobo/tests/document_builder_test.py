from functools import partial

from pyobo.document_builder import OboDocumentBuilder, OboDocumentBuildingError
from pyobo.obo_document import OboDocument, OboTerm, OboTypedef
from pyobo.tests.document_assert import DocumentAsserter


class TestDocBuilding(DocumentAsserter):

    def setUp(self):
        self.under_test = OboDocumentBuilder()
        self.tag_value_pair = self.under_test.tag_value_pair
        self.boolean_tag_value_pair = self.under_test.boolean_tag_value_pair
        self.assertDocuments = partial(self.assertDocumentEquals, self.under_test.document)

    def expected(self, header=lambda header: None, terms=lambda: [], typedefs=lambda: []):
        result = OboDocument()
        header(result.header)
        result.terms = terms()
        result.typedefs = typedefs()
        return result

    def test_should_update_single_value_tag_header2(self):
        self.tag_value_pair("data-version", "world")

        def expected_header(header):
            header.data_version = "world"

        expected = self.expected(header=expected_header)
        self.assertDocuments(expected)

    def test_should_update_boolean_value_tag(self):
        self.under_test.term()
        self.boolean_tag_value_pair("is_obsolete", True)

        def expected_terms():
            term = OboTerm()
            term.is_obsolete = True
            return [term]

        expected = self.expected(terms=expected_terms)
        self.assertDocuments(expected)

    def test_should_reject_booleans_on_multi_value_tags(self):
        self.under_test.term()
        with self.assertRaises(OboDocumentBuildingError):
            self.boolean_tag_value_pair("subset", True)

    def test_should_update_unknown_tag_header(self):
        self.tag_value_pair("hello", "world")

        def expected_header(header):
            header.hello = ["world"]

        expected = self.expected(header=expected_header)
        self.assertDocuments(expected)

    def test_should_update_multi_value_tag_header(self):
        self.tag_value_pair("remark", "remark")
        self.tag_value_pair("remark", "remark")

        def expected_header(header):
            header.remark = ["remark", "remark"]

        expected = self.expected(header=expected_header)
        self.assertDocuments(expected)

    def test_should_fail_if_single_value_tag_is_present_more_than_once(self):
        self.tag_value_pair("data-version", "world")
        with self.assertRaises(OboDocumentBuildingError):
            self.tag_value_pair("data-version", "anotherWorld")

    def test_should_not_fail_if_single_value_tag_is_present_more_than_once_with_same_value(self):
        self.tag_value_pair("data-version", "world")
        self.tag_value_pair("data-version", "world")

        def expected_header(header):
            header.data_version = "world"

        expected = self.expected(header=expected_header)
        self.assertDocuments(expected)

    def test_should_support_version_as_data_version(self):
        self.tag_value_pair("version", "1.2")

        def expected_header(header):
            header.data_version = "1.2"

        expected = self.expected(header=expected_header)
        self.assertDocuments(expected)

    def test_should_support_term_addition(self):
        self.under_test.term()

        def expected_terms():
            return [OboTerm()]

        expected = self.expected(terms=expected_terms)
        self.assertDocuments(expected)

    def test_should_support_typedef_addition(self):
        self.under_test.typedef()

        def expected_typedefs():
            return [OboTypedef()]

        expected = self.expected(typedefs=expected_typedefs)
        self.assertDocuments(expected)

    def test_should_support_qualifiers(self):
        self.under_test.term()
        self.under_test.qualifier("q1", "v1")
        self.under_test.tag_value_pair("data-version", "world")

        def expected_terms():
            term = OboTerm()
            term.data_version = ["world"]
            term._qualifiers["data_version"] = {"q1": "v1"}
            return [term]

        expected = self.expected(terms=expected_terms)
        self.assertDocuments(expected)

    def test_should_support_mix_qualifiers_and_no_qualifier(self):
        self.under_test.term()
        self.under_test.qualifier("q1", "v1")
        self.under_test.tag_value_pair("data-version", "world")
        self.under_test.tag_value_pair("data-version2", "world2")

        def expected_terms():
            term = OboTerm()
            term.data_version = ["world"]
            term.data_version2 = ["world2"]
            term._qualifiers["data_version"] = {"q1": "v1"}
            return [term]

        expected = self.expected(terms=expected_terms)
        self.assertDocuments(expected)
