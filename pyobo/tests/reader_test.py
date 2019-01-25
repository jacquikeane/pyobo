from pyobo.obo_document import OboDocument
from pyobo.obo_reader import read
from pyobo.tests.document_assert import DocumentAsserter


class TestReader(DocumentAsserter):

    def test_should_read_lines(self):
        actual = read((line for line in ["format-version: 1.2", "another-format-version: 1.3"]))
        expected = OboDocument()
        expected.header.format_version = "1.2"
        expected.header.another_format_version = "1.3"
        self.assertDocumentEquals(actual, expected)
