from pyobo.obo_document import OboDocument
from pyobo.obo_reader import read
from pyobo.tests.document_assert import DocumentAsserter


class TestHeaderReader(DocumentAsserter):

    def test_supports_invalid_date(self):
        """This test should not pass, the date should be validated"""
        actual = read((line for line in ["date: some invalid date"]))
        expected = OboDocument()
        expected.header.date = "some invalid date"
        self.assertDocumentEquals(actual, expected)

    def test_supports_date(self):
        actual = read((line for line in ["date: 22:05:1987 10:54"]))
        expected = OboDocument()
        expected.header.date = "22:05:1987 10:54"
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_import_but_does_not_validate_url(self):
        actual = read((line for line in ["import: an invalid import"]))
        expected = OboDocument()
        expected.header.import_ = ["an invalid import"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_imports_but_does_not_validate_url(self):
        actual = read((line for line in ["import: an invalid import\n", "import: http://someurl/\n"]))
        expected = OboDocument()
        expected.header.import_ = ["an invalid import", "http://someurl/"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_subsetdef_but_does_not_validate_content(self):
        actual = read((line for line in ["subsetdef: an invalid subsetdef"]))
        expected = OboDocument()
        expected.header.subsetdef = ["an invalid subsetdef"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_subsetdef_but_does_not_validate_content(self):
        actual = read((line for line in ["subsetdef: an invalid subsetdef\n", "subsetdef: ID \"value\"\n"]))
        expected = OboDocument()
        expected.header.subsetdef = ["an invalid subsetdef", 'ID "value"']
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_synonymtypedef_but_does_not_validate_content(self):
        actual = read((line for line in ["synonymtypedef: an invalid synonymtypedef"]))
        expected = OboDocument()
        expected.header.synonymtypedef = ["an invalid synonymtypedef"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_synonymtypedef_but_does_not_validate_content(self):
        actual = read(
            (line for line in ["synonymtypedef: an invalid synonymtypedef\n", "synonymtypedef: ID \"value\"\n"]))
        expected = OboDocument()
        expected.header.synonymtypedef = ["an invalid synonymtypedef", 'ID "value"']
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_treat_xrefs_as_equivalent_but_does_not_validate_content(self):
        actual = read((line for line in ["treat-xrefs-as-equivalent: an invalid treat-xrefs-as-equivalent"]))
        expected = OboDocument()
        expected.header.treat_xrefs_as_equivalent = ["an invalid treat-xrefs-as-equivalent"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_treat_xrefs_as_equivalent_but_does_not_validate_content(self):
        actual = read((line for line in ["treat-xrefs-as-equivalent: an invalid treat-xrefs-as-equivalent\n",
                                         "treat-xrefs-as-equivalent: ID\n"]))
        expected = OboDocument()
        expected.header.treat_xrefs_as_equivalent = ["an invalid treat-xrefs-as-equivalent", 'ID']
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_idspace_but_does_not_validate_content(self):
        actual = read((line for line in ["idspace: an invalid idspace"]))
        expected = OboDocument()
        expected.header.idspace = ["an invalid idspace"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_idspace_but_does_not_validate_content(self):
        actual = read((line for line in ["idspace: an invalid idspace\n", "idspace: ID \"value\"\n"]))
        expected = OboDocument()
        expected.header.idspace = ["an invalid idspace", 'ID "value"']
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_relax_unique_label_assumption_for_namespace_but_does_not_validate_content(self):
        actual = read((line for line in [
            "relax-unique-label-assumption-for-namespace: an invalid relax-unique-label-assumption-for-namespace"]))
        expected = OboDocument()
        expected.header.relax_unique_label_assumption_for_namespace = [
            "an invalid relax-unique-label-assumption-for-namespace"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_relax_unique_label_assumption_for_namespace_but_does_not_validate_content(self):
        actual = read((line for line in [
            "relax-unique-label-assumption-for-namespace: an invalid relax-unique-label-assumption-for-namespace\n",
            "relax-unique-label-assumption-for-namespace: ID \"value\"\n"]))
        expected = OboDocument()
        expected.header.relax_unique_label_assumption_for_namespace = [
            "an invalid relax-unique-label-assumption-for-namespace", 'ID "value"']
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_relax_unique_identifier_assumption_for_namespace_but_does_not_validate_content(self):
        actual = read((line for line in [
            "relax-unique-identifier-assumption-for-namespace: an invalid relax-unique-identifier-assumption-for-namespace"]))
        expected = OboDocument()
        expected.header.relax_unique_identifier_assumption_for_namespace = [
            "an invalid relax-unique-identifier-assumption-for-namespace"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_relax_unique_identifier_assumption_for_namespace_but_does_not_validate_content(self):
        actual = read((line for line in [
            "relax-unique-identifier-assumption-for-namespace: an invalid relax-unique-identifier-assumption-for-namespace\n",
            "relax-unique-identifier-assumption-for-namespace: ID \"value\"\n"]))
        expected = OboDocument()
        expected.header.relax_unique_identifier_assumption_for_namespace = [
            "an invalid relax-unique-identifier-assumption-for-namespace", 'ID "value"']
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_property_value_but_does_not_validate_content(self):
        actual = read((line for line in ["property_value: an invalid property_value"]))
        expected = OboDocument()
        expected.header.property_value = ["an invalid property_value"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_property_value_but_does_not_validate_content(self):
        actual = read(
            (line for line in ["property_value: an invalid property_value\n", "property_value: ID \"value\"\n"]))
        expected = OboDocument()
        expected.header.property_value = ["an invalid property_value", 'ID "value"']
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_id_mapping_but_does_not_validate_content(self):
        actual = read((line for line in ["id-mapping: an invalid id-mapping"]))
        expected = OboDocument()
        expected.header.id_mapping = ["an invalid id-mapping"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_id_mapping_but_does_not_validate_content(self):
        actual = read((line for line in ["id-mapping: an invalid id-mapping\n", "id-mapping: ID \"value\"\n"]))
        expected = OboDocument()
        expected.header.id_mapping = ["an invalid id-mapping", 'ID "value"']
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_treat_xrefs_as_has_subclass_but_does_not_validate_content(self):
        actual = read((line for line in ["treat-xrefs-as-has-subclass: an invalid treat-xrefs-as-has-subclass"]))
        expected = OboDocument()
        expected.header.treat_xrefs_as_has_subclass = ["an invalid treat-xrefs-as-has-subclass"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_treat_xrefs_as_has_subclass_but_does_not_validate_content(self):
        actual = read((line for line in ["treat-xrefs-as-has-subclass: an invalid treat-xrefs-as-has-subclass\n",
                                         "treat-xrefs-as-has-subclass: ID \"value\"\n"]))
        expected = OboDocument()
        expected.header.treat_xrefs_as_has_subclass = ["an invalid treat-xrefs-as-has-subclass", 'ID "value"']
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_treat_xrefs_as_is_a_but_does_not_validate_content(self):
        actual = read((line for line in ["treat-xrefs-as-is_a: an invalid treat-xrefs-as-is_a"]))
        expected = OboDocument()
        expected.header.treat_xrefs_as_is_a = ["an invalid treat-xrefs-as-is_a"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_treat_xrefs_as_is_a_but_does_not_validate_content(self):
        actual = read((line for line in
                       ["treat-xrefs-as-is_a: an invalid treat-xrefs-as-is_a\n",
                        "treat-xrefs-as-is_a: ID \"value\"\n"]))
        expected = OboDocument()
        expected.header.treat_xrefs_as_is_a = ["an invalid treat-xrefs-as-is_a", 'ID "value"']
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_treat_xrefs_as_relationship_but_does_not_validate_content(self):
        actual = read((line for line in ["treat-xrefs-as-relationship: an invalid treat-xrefs-as-relationship"]))
        expected = OboDocument()
        expected.header.treat_xrefs_as_relationship = ["an invalid treat-xrefs-as-relationship"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_treat_xrefs_as_relationship_but_does_not_validate_content(self):
        actual = read((line for line in ["treat-xrefs-as-relationship: an invalid treat-xrefs-as-relationship\n",
                                         "treat-xrefs-as-relationship: ID \"value\"\n"]))
        expected = OboDocument()
        expected.header.treat_xrefs_as_relationship = ["an invalid treat-xrefs-as-relationship", 'ID "value"']
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_treat_xrefs_as_genus_differentia_but_does_not_validate_content(self):
        actual = read(
            (line for line in ["treat-xrefs-as-genus-differentia: an invalid treat-xrefs-as-genus-differentia"]))
        expected = OboDocument()
        expected.header.treat_xrefs_as_genus_differentia = ["an invalid treat-xrefs-as-genus-differentia"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_treat_xrefs_as_genus_differentia_but_does_not_validate_content(self):
        actual = read((line for line in
                       ["treat-xrefs-as-genus-differentia: an invalid treat-xrefs-as-genus-differentia\n",
                        "treat-xrefs-as-genus-differentia: ID \"value\"\n"]))
        expected = OboDocument()
        expected.header.treat_xrefs_as_genus_differentia = ["an invalid treat-xrefs-as-genus-differentia", 'ID "value"']
        self.assertDocumentEquals(actual, expected)

    def test_supports_single_treat_xrefs_as_reverse_genus_differentia_but_does_not_validate_content(self):
        actual = read(
            (line for line in
             ["treat-xrefs-as-reverse-genus-differentia: an invalid treat-xrefs-as-reverse-genus-differentia"]))
        expected = OboDocument()
        expected.header.treat_xrefs_as_reverse_genus_differentia = [
            "an invalid treat-xrefs-as-reverse-genus-differentia"]
        self.assertDocumentEquals(actual, expected)

    def test_supports_multiple_treat_xrefs_as_reverse_genus_differentia_but_does_not_validate_content(self):
        actual = read((line for line in
                       [
                           "treat-xrefs-as-reverse-genus-differentia: an invalid treat-xrefs-as-reverse-genus-differentia\n"
                           , "treat-xrefs-as-reverse-genus-differentia: ID \"value\"\n"]))
        expected = OboDocument()
        expected.header.treat_xrefs_as_reverse_genus_differentia = [
            "an invalid treat-xrefs-as-reverse-genus-differentia", 'ID "value"']
        self.assertDocumentEquals(actual, expected)
