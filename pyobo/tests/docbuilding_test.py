from pyobo.document_builder import OboDocumentBuilder
from pyobo.obo_document import OboDocument
from pyobo.tests.document_assert import DocumentAsserter


class TestDocBuilding(DocumentAsserter):

    def test_should_update_header(self):
        under_test = OboDocumentBuilder()
        under_test.tag_value_pair("hello", "world")
        expected = OboDocument()
        expected.header.hello = "world"
        self.assertDocumentEquals(under_test.document, expected)
