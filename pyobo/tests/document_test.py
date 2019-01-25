import unittest

from pyobo.obo_document import OboHeader


def extract_dictionary(list):
    return [x.__dict__ for x in list]


class TestDocument(unittest.TestCase):

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
