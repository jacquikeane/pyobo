from pyobo.document_builder import OboDocumentBuilder, OboDocumentBuildingError
from pyobo.obo_document import OboDocument, OboTerm, OboTypedef
from pyobo.tests.document_assert import DocumentAsserter


class TestDocBuilding(DocumentAsserter):

    def test_should_update_single_value_tag_header(self):
        under_test = OboDocumentBuilder()
        under_test.tag_value_pair("data-version", "world")
        expected = OboDocument()
        expected.header.data_version = "world"
        self.assertDocumentEquals(under_test.document, expected)

    def test_should_update_unknown_tag_header(self):
        under_test = OboDocumentBuilder()
        under_test.tag_value_pair("hello", "world")
        expected = OboDocument()
        expected.header.hello = ["world"]
        self.assertDocumentEquals(under_test.document, expected)

    def test_should_update_multi_value_tag_header(self):
        under_test = OboDocumentBuilder()
        under_test.tag_value_pair("remark", "remark")
        under_test.tag_value_pair("remark", "remark")
        expected = OboDocument()
        expected.header.remark = ["remark", "remark"]
        self.assertDocumentEquals(under_test.document, expected)

    def test_should_fail_if_single_value_tag_is_present_more_than_once(self):
        under_test = OboDocumentBuilder()
        under_test.tag_value_pair("data-version", "world")
        with self.assertRaises(OboDocumentBuildingError):
            under_test.tag_value_pair("data-version", "anotherWorld")

    def test_should_not_fail_if_single_value_tag_is_present_more_than_once_with_same_value(self):
        under_test = OboDocumentBuilder()
        under_test.tag_value_pair("data-version", "world")
        under_test.tag_value_pair("data-version", "world")
        expected = OboDocument()
        expected.header.data_version = "world"
        self.assertDocumentEquals(under_test.document, expected)

    def test_should_support_version_as_data_version(self):
        under_test = OboDocumentBuilder()
        under_test.tag_value_pair("version", "1.2")
        expected = OboDocument()
        expected.header.data_version = "1.2"
        self.assertDocumentEquals(under_test.document, expected)

    def test_should_support_term_addition(self):
        under_test = OboDocumentBuilder()
        under_test.term()
        expected = OboDocument()
        expected.terms = [OboTerm()]
        self.assertDocumentEquals(under_test.document, expected)

    def test_should_support_typedef_addition(self):
        under_test = OboDocumentBuilder()
        under_test.typedef()
        expected = OboDocument()
        expected.typedefs = [OboTypedef()]
        self.assertDocumentEquals(under_test.document, expected)
