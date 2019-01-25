import unittest

from pyobo.obo_document import OboHeader


def extract_dictionary(list):
    return [x.__dict__ for x in list]


class TestDocument(unittest.TestCase):

    def test_header_simple_tag_value_initialized_to_none(self):
        header = OboHeader()
        self.assertIsNone(header.format_version)
        self.assertIsNone(header.data_version)
        self.assertIsNone(header.saved_by)
        self.assertIsNone(header.auto_generated_by)
        self.assertIsNone(header.remark)
        self.assertIsNone(header.ontology)
        self.assertIsNone(header.owl_axioms)
