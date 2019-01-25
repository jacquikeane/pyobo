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


header_tvp = ['format_version', 'data_version', 'saved_by', 'auto_generated_by', 'remark', 'ontology', 'owl_axioms']
class OboHeader(Base):

    def __init__(self):
        for tvp in header_tvp:
            self.__dict__[tvp] = None
        pass
# Possible header tags and status of implementation
# format_version -> supported
# data-version -> supported
# date-Tag  DD:MM:YYYY sp hh:mm -> not supported
# saved-by -> supported
# auto-generated-by  -> supported
# import-Tag  IRI | filepath  -> not supported
# subsetdef-Tag  ID sp QuotedString  -> not supported
# synonymtypedef-Tag  ID sp QuotedString  -> not supported
#    [  SynonymScope ]  -> not supported
# default-namespace-Tag  OBONamespace  -> not supported
# idspace-Tag IDPrefix sp IRI  -> not supported
#   [ sp QuotedString ]  -> not supported
# treat-xrefs-as-equivalent-Tag IDPrefix  -> not supported
# treat-xrefs-as-genus-differentia-Tag IDPrefix ws Rel-ID ws Class-ID  -> not supported
# treat-xrefs-as-reverse-genus-differentia-Tag IDPrefix ws Rel-ID ws Class-ID  -> not supported
# treat-xrefs-as-relationship-Tag IDPrefix Rel-ID  -> not supported
# treat-xrefs-as-is_a-Tag IDPrefix  -> not supported
# treat-xrefs-as-has-subclass-Tag IDPrefix  -> not supported
# property_value-Tag Relation-ID ( QuotedString XSD-Type | ID ) {WhiteSpaceChar} [ QualifierBlock ] {WhiteSpaceChar} [ HiddenComment ] -> not supported
# remark -> supported
# ontology -> supported
# owl-axioms -> supported
# UnreservedToken -> supported
