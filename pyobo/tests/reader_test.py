from pyobo.obo_document import OboDocument, OboTerm, OboTypedef
from pyobo.obo_reader import read
from pyobo.tests.document_assert import DocumentAsserter


class TestReader(DocumentAsserter):

    def test_should_read_lines(self):
        actual = read((line for line in [
            "format-version: 1.2",
            "another-format-version: 1.3",
            "[Term]",
            "id: GO:0015137",
            "name: citrate transmembrane transporter activity",
            "namespace: molecular_function",
            '''def: "Enables the transfer of citrate, 2-hydroxy-1,2,3-propanetricarboyxlate, '''
            '''from one side of a membrane to the other." [GOC:ai]''',
            """synonym: "tricarboxylate transport protein" RELATED [] {comment="WIkipedia:Mitochondrial_carrier"}""",
            'xref: reactome:R-HSA-433104 "NACT co-transports trivalent citrate and a sodium ion"',
            "is_a: GO:0015142 ! tricarboxylic acid transmembrane transporter activity",
            "is_a: GO:0042895 ! antibiotic transmembrane transporter activity",
            "relationship: part_of GO:0015746 ! citrate transport",

            "[Typedef]",
            "id: ends_during",
            "name: ends_during",
            "namespace: external",
            "xref: RO:0002093",

        ]))
        expected = OboDocument()
        expected.header.format_version = "1.2"
        expected.header.another_format_version = ["1.3"]
        term = OboTerm()
        term.id = "GO:0015137"
        term.name = "citrate transmembrane transporter activity"
        term.namespace = "molecular_function"
        term.def_ = '''"Enables the transfer of citrate, 2-hydroxy-1,2,3-propanetricarboyxlate, ''' \
                    + '''from one side of a membrane to the other." [GOC:ai]'''
        term.synonym = ['"tricarboxylate transport protein" RELATED []']
        term.xref = ['reactome:R-HSA-433104 "NACT co-transports trivalent citrate and a sodium ion"']
        term.is_a = ["GO:0015142", "GO:0042895"]
        term.relationship = ["part_of GO:0015746"]
        term._qualifiers["synonym"] = {"comment": "WIkipedia:Mitochondrial_carrier"}

        typedef = OboTypedef()
        typedef.id = "ends_during"
        typedef.name = "ends_during"
        typedef.namespace = "external"
        typedef.xref = ["RO:0002093"]
        expected.terms = [term]
        expected.typedefs = [typedef]
        self.assertDocumentEquals(actual, expected)
