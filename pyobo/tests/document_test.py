from pyobo.obo_document import OboHeader, OboTypedef, OboDocument, OboTerm
from pyobo.tests.document_assert import DocumentAsserter


class TestDocument(DocumentAsserter):
    A_TERM_ID = "1234"
    A_TYPEDEF_ID = "5678"

    def test_header_initialization(self):
        header = OboHeader()
        self.assertIsNone(header.ontology)
        self.assertIsNone(header.format_version)
        self.assertIsNone(header.date)
        self.assertIsNone(header.default_namespace)
        self.assertIsNone(header.saved_by)
        self.assertIsNone(header.auto_generated_by)
        self.assertIsNone(header.data_version)
        self.assertIsNone(header.default_relationship_id_prefix)

        self.assertEquals(header.remark, [])
        self.assertEquals(header.import_, [])
        self.assertEquals(header.subsetdef, [])
        self.assertEquals(header.synonymtypedef, [])
        self.assertEquals(header.idspace, [])
        self.assertEquals(header.treat_xrefs_as_equivalent, [])
        self.assertEquals(header.treat_xrefs_as_genus_differentia, [])
        self.assertEquals(header.treat_xrefs_as_reverse_genus_differentia, [])
        self.assertEquals(header.treat_xrefs_as_relationship, [])
        self.assertEquals(header.treat_xrefs_as_is_a, [])
        self.assertEquals(header.treat_xrefs_as_has_subclass, [])
        self.assertEquals(header.property_value, [])
        self.assertEquals(header.owl_axioms, [])
        self.assertEquals(header.id_mapping, [])
        self.assertEquals(header.relax_unique_identifier_assumption_for_namespace, [])
        self.assertEquals(header.relax_unique_label_assumption_for_namespace, [])

    def test_add_term(self):
        actual = OboDocument()
        term = actual.add_term()
        term.id = TestDocument.A_TERM_ID

        expected = OboDocument()
        expected_term = OboTerm()
        expected_term.id = TestDocument.A_TERM_ID
        expected.terms = [expected_term]

        self.assertDocumentEquals(actual, expected)

    def test_add_typedef(self):
        actual = OboDocument()
        typedef = actual.add_typedef()
        typedef.id = TestDocument.A_TYPEDEF_ID

        expected = OboDocument()
        expected_typedef = OboTypedef()
        expected_typedef.id = TestDocument.A_TYPEDEF_ID
        expected.typedefs = [expected_typedef]

        self.assertDocumentEquals(actual, expected)
