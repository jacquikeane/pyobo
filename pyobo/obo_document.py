class Base:

    def __repr__(self):
        fields = ["%s=%s" % (key, self.__dict__[key]) for key in sorted(self.__dict__.keys())]
        return "%s%s" % (self.__class__.__name__, fields)


class OboDocument(Base):

    def __init__(self):
        self.header = OboHeader()
        self.terms = []
        self.typedefs = []
        pass


# todo version is deprecated, so not supported
header_tvp = ['format_version', 'data_version', 'saved_by', 'auto_generated_by', 'remark', 'ontology', 'owl_axioms']


class OboHeader(Base):

    def __init__(self):
        for tvp in header_tvp:
            self.__dict__[tvp] = None
        pass

    def valid(self):
        return self.format_version is not None

# Possible header tags and status of implementation
# format_version (mandatory only one)-> supported
# data-version (zero/one)-> supported
# version (zero/one)-> supported
# date-Tag  DD:MM:YYYY sp hh:mm (zero/one)-> not supported
# saved-by (zero/one)-> supported
# auto-generated-by (zero/one) -> supported
# import-Tag  IRI | filepath  (Any) -> not supported
# subsetdef-Tag  ID sp QuotedString  (any) -> not supported  (The value for this tag should contain a subset name, a space, and a quote enclosed subset description ie subsetdef: GO_SLIM "GO Slim")
# synonymtypedef-Tag  ID sp QuotedString [  SynonymScope ] (any) -> not supported (ie synonymtypedef: UK_SPELLING "British spelling" EXACT)
# default-namespace-Tag  OBONamespace  -> not supported
# idspace-Tag IDPrefix sp IRI [ sp QuotedString ] (any)-> not supported (idspace: GO urn:lsid:bioontology.org:GO: "gene ontology terms")
# treat-xrefs-as-equivalent-Tag IDPrefix  (Any)-> not supported
# treat-xrefs-as-genus-differentia-Tag IDPrefix ws Rel-ID ws Class-ID  (Any)-> not supported
# treat-xrefs-as-reverse-genus-differentia-Tag IDPrefix ws Rel-ID ws Class-ID  -> not supported
# treat-xrefs-as-relationship-Tag IDPrefix Rel-ID  (Any)-> not supported
# treat-xrefs-as-is_a-Tag IDPrefix  (Any)-> not supported
# treat-xrefs-as-has-subclass-Tag IDPrefix  -> not supported
# property_value-Tag Relation-ID ( QuotedString XSD-Type | ID ) {WhiteSpaceChar} [ QualifierBlock ] {WhiteSpaceChar} [ HiddenComment ] -> not supported
# remark (any)-> supported
# ontology -> supported (prefix of term of ontology in lowercase ie go, if extention, should be xx/yy ie go/gosubset_prok)
# owl-axioms -> supported
# UnreservedToken -> supported
# default-relationship-id-prefix: OBO_REL (zero or one)
# id-mapping (any) ie (id-mapping: part_of OBO_REL:part_of)
# relax-unique-identifier-assumption-for-namespace (Any)
# relax-unique-label-assumption-for-namespace (Any)
