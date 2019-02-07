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

    def test_term_initialization(self):
        term = OboTerm()

        self.assertIsNone(term.id)
        self.assertIsNone(term.is_anonymous)
        self.assertIsNone(term.name)
        self.assertIsNone(term.namespace)
        self.assertIsNone(term.def_)
        self.assertIsNone(term.comment)
        self.assertIsNone(term.builtin)
        self.assertIsNone(term.is_obsolete)
        self.assertIsNone(term.created_by)
        self.assertIsNone(term.creation_date)

        self.assertEquals(term.alt_id, [])
        self.assertEquals(term.subset, [])
        self.assertEquals(term.synonym, [])
        self.assertEquals(term.xref, [])
        self.assertEquals(term.property_value, [])
        self.assertEquals(term.is_a, [])
        self.assertEquals(term.intersection_of, [])
        self.assertEquals(term.union_of, [])
        self.assertEquals(term.equivalent_to, [])
        self.assertEquals(term.disjoint_from, [])
        self.assertEquals(term.relationship, [])
        self.assertEquals(term.replaced_by, [])
        self.assertEquals(term.consider, [])

    def test_typedef_initialization(self):
        term = OboTypedef()

        self.assertIsNone(term.id)
        self.assertIsNone(term.is_anonymous)
        self.assertIsNone(term.name)
        self.assertIsNone(term.namespace)
        self.assertIsNone(term.def_)
        self.assertIsNone(term.comment)
        self.assertIsNone(term.domain)
        self.assertIsNone(term.range)
        self.assertIsNone(term.builtin)
        self.assertIsNone(term.is_anti_symmetric)
        self.assertIsNone(term.is_cyclic)
        self.assertIsNone(term.is_reflexive)
        self.assertIsNone(term.is_symmetric)
        self.assertIsNone(term.is_transitive)
        self.assertIsNone(term.is_functional)
        self.assertIsNone(term.is_inverse_functional)
        self.assertIsNone(term.is_obsolete)
        self.assertIsNone(term.created_by)
        self.assertIsNone(term.creation_date)
        self.assertIsNone(term.is_metadata_tag)
        self.assertIsNone(term.is_class_level_tag)

        self.assertEquals(term.alt_id, [])
        self.assertEquals(term.subset, [])
        self.assertEquals(term.synonym, [])
        self.assertEquals(term.xref, [])
        self.assertEquals(term.property_value, [])
        self.assertEquals(term.holds_over_chain, [])
        self.assertEquals(term.is_a, [])
        self.assertEquals(term.intersection_of, [])
        self.assertEquals(term.union_of, [])
        self.assertEquals(term.equivalent_to, [])
        self.assertEquals(term.disjoint_from, [])
        self.assertEquals(term.inverse_of, [])
        self.assertEquals(term.transitive_over, [])
        self.assertEquals(term.equivalent_to_chain, [])
        self.assertEquals(term.disjoint_over, [])
        self.assertEquals(term.relationship, [])
        self.assertEquals(term.replaced_by, [])
        self.assertEquals(term.consider, [])
        self.assertEquals(term.expand_assertion_to, [])
        self.assertEquals(term.expand_expression_to, [])

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
