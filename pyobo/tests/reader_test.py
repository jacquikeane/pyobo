from pyobo.obo_document import OboDocument, OboTerm, OboTypedef, OboDef, OboXref
from pyobo.obo_reader import read
from pyobo.tests.document_assert import DocumentAsserter


class TestReader(DocumentAsserter):

    def test_should_read_lines(self):
        actual = read((line for line in [
            "format-version: 1.2\n",
            "another-format-version: 1.3\n",
            "[Term]\n",
            "id: GO:0015137\n",
            "name: citrate transmembrane transporter activity\n",
            "namespace: molecular_function\n",
            '''def: "Enables the transfer of citrate from one side of a membrane to the other." [GOC:ai]\n''',
            """synonym: "tricarboxylate transport protein" RELATED [] {comment="WIkipedia:Mitochondrial_carrier"}\n""",
            'xref: reactome:R-HSA-433104 "NACT co-transports trivalent citrate and a sodium ion"\n',
            "is_a: GO:0015142 ! tricarboxylic acid transmembrane transporter activity\n",
            "is_a: GO:0042895 ! antibiotic transmembrane transporter activity\n",
            "relationship: part_of GO:0015746 ! citrate transport\n",
            "is_obsolete: true ! this is just to test a boolean\n",

            "[Typedef]\n",
            "id: ends_during\n",
            "name: ends_during\n",
            "namespace: external\n",
            "xref: RO:0002093\n",

        ]))
        expected = OboDocument()
        expected.header.format_version = "1.2"
        expected.header.another_format_version = ["1.3"]
        term = OboTerm()
        term.id = "GO:0015137"
        term.name = "citrate transmembrane transporter activity"
        term.namespace = "molecular_function"
        term.def_ = OboDef('''Enables the transfer of citrate from one side of a membrane to the other.''',
                           [OboXref("GOC:ai", None)])
        term.synonym = ['"tricarboxylate transport protein" RELATED []']
        term.xref = OboXref('reactome:R-HSA-433104', "NACT co-transports trivalent citrate and a sodium ion")
        term.is_a = ["GO:0015142", "GO:0042895"]
        term.relationship = ["part_of GO:0015746"]
        term.is_obsolete = True
        term._qualifiers["synonym"] = {"comment": "WIkipedia:Mitochondrial_carrier"}

        typedef = OboTypedef()
        typedef.id = "ends_during"
        typedef.name = "ends_during"
        typedef.namespace = "external"
        typedef.xref = OboXref("RO:0002093", None)
        expected.terms = [term]
        expected.typedefs = [typedef]
        self.assertDocumentEquals(actual, expected)
