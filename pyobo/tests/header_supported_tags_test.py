from pyobo.obo_document import OboDocument
from pyobo.obo_reader import read
from pyobo.tests.document_assert import DocumentAsserter


class TestFullySupportedHeaderTags(DocumentAsserter):

    def test_supports_format_version(self):
        actual = read((line for line in ["format-version: 1.2"]))
        expected = OboDocument()
        expected.header.format_version = "1.2"
        self.assertDocumentEquals(actual, expected)

    def test_supports_ontology(self):
        actual = read((line for line in ["ontology: hello"]))
        expected = OboDocument()
        expected.header.ontology = "hello"
        self.assertDocumentEquals(actual, expected)

    def test_supports_default_namespace(self):
        actual = read((line for line in ["default-namespace: hello"]))
        expected = OboDocument()
        expected.header.default_namespace = "hello"
        self.assertDocumentEquals(actual, expected)

    def test_supports_data_version(self):
        actual = read((line for line in ["data-version: 1.2"]))
        expected = OboDocument()
        expected.header.data_version = "1.2"
        self.assertDocumentEquals(actual, expected)

    def test_supports_version(self):
        actual = read((line for line in ["version: 1.2"]))
        expected = OboDocument()
        expected.header.data_version = "1.2"
        self.assertDocumentEquals(actual, expected)

    def test_supports_saved_by(self):
        actual = read((line for line in ["saved-by: myself"]))
        expected = OboDocument()
        expected.header.saved_by = "myself"
        self.assertDocumentEquals(actual, expected)

    def test_supports_auto_generated_by(self):
        actual = read((line for line in ["auto-generated-by: myself"]))
        expected = OboDocument()
        expected.header.auto_generated_by = "myself"
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_remark(self):
        actual = read((line for line in ["remark: some comment"]))
        expected = OboDocument()
        expected.header.remark = ["some comment"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_remarks(self):
        actual = read((line for line in ["remark: some comment\n", "remark: some other comment\n"]))
        expected = OboDocument()
        expected.header.remark = ["some comment", "some other comment"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_owl_axiom(self):
        actual = read((line for line in ["owl-axioms: an axiom"]))
        expected = OboDocument()
        expected.header.owl_axioms = ["an axiom"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_owl_axioms(self):
        actual = read((line for line in ["owl-axioms: an axiom\n", "owl-axioms: another axiom\n"]))
        expected = OboDocument()
        expected.header.owl_axioms = ["an axiom", "another axiom"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_default_relationship_id_prefix(self):
        actual = read((line for line in ["default-relationship-id-prefix: prefix"]))
        expected = OboDocument()
        expected.header.default_relationship_id_prefix = "prefix"
        self.assertDocumentEquals(actual, expected)
