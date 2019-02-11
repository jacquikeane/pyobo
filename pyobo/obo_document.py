class Base:

    def __init__(self, single_value_tags=[], multi_value_tags=[]):
        for tag in single_value_tags:
            self.__dict__[tag] = None
        for tag in multi_value_tags:
            self.__dict__[tag] = []

    def __repr__(self):
        fields = ["%s=%s" % (key, self.__dict__[key]) for key in sorted(self.__dict__.keys())]
        return "%s%s" % (self.__class__.__name__, fields)


class OboDocument(Base):

    def __init__(self):
        self.header = OboHeader()
        self.terms = []
        self.typedefs = []
        pass

    def add_term(self):
        term = OboTerm()
        self.terms.append(term)
        return term

    def add_typedef(self):
        typedef = OboTypedef()
        self.typedefs.append(typedef)
        return typedef


HEADER_SINGLE_VALUE_TAGS = ['ontology',
                            'format_version',
                            'date',
                            'default_namespace',
                            'saved_by',
                            'auto_generated_by',
                            'data_version',
                            'default_relationship_id_prefix']

HEADER_MULTI_VALUE_TAGS = ['remark',
                           'import_',
                           'subsetdef',
                           'synonymtypedef',
                           'idspace',
                           'treat_xrefs_as_equivalent',
                           'treat_xrefs_as_genus_differentia',
                           'treat_xrefs_as_reverse_genus_differentia',
                           'treat_xrefs_as_relationship',
                           'treat_xrefs_as_is_a',
                           'treat_xrefs_as_has_subclass',
                           'property_value',
                           'owl_axioms',
                           'id_mapping',
                           'relax_unique_identifier_assumption_for_namespace',
                           'relax_unique_label_assumption_for_namespace']

TERM_SINGLE_VALUE_TAGS = ['id',
                          'is_anonymous',
                          'name',
                          'namespace',
                          'def_',
                          'comment',
                          'builtin',
                          'is_obsolete',
                          'created_by',
                          'creation_date']
TERM_MULTI_VALUE_TAGS = ['alt_id',
                         'subset',
                         'synonym',
                         'xref',
                         'property_value',
                         'is_a',
                         'intersection_of',
                         'union_of',
                         'equivalent_to',
                         'disjoint_from',
                         'relationship',
                         'replaced_by',
                         'consider']

TYPEDEF_SINGLE_VALUE_TAGS = ['id',
                             'is_anonymous',
                             'name',
                             'namespace',
                             'def_',
                             'comment',
                             'domain',
                             'range',
                             'builtin',
                             'is_anti_symmetric',
                             'is_cyclic',
                             'is_reflexive',
                             'is_symmetric',
                             'is_transitive',
                             'is_functional',
                             'is_inverse_functional',
                             'is_obsolete',
                             'created_by',
                             'creation_date',
                             'is_metadata_tag',
                             'is_class_level_tag']
TYPEDEF_MULTI_VALUE_TAGS = ['alt_id',
                            'subset',
                            'synonym',
                            'xref',
                            'property_value',
                            'holds_over_chain',
                            'is_a',
                            'intersection_of',
                            'union_of',
                            'equivalent_to',
                            'disjoint_from',
                            'inverse_of',
                            'transitive_over',
                            'equivalent_to_chain',
                            'disjoint_over',
                            'relationship',
                            'replaced_by',
                            'consider',
                            'expand_assertion_to',
                            'expand_expression_to']


class OboXref(Base):
    def __init__(self, xref, description):
        self.xref = xref
        self.description = description

    def __eq__(self, other):
        return self.description == other.description and self.xref == other.xref


class OboDef(Base):

    def __init__(self, value, xrefs):
        self.value = value
        self.xrefs = xrefs

    def __eq__(self, other):
        return self.value == other.value and self.xrefs == other.xrefs

class OboHeader(Base):

    def __init__(self):
        super(OboHeader, self).__init__(HEADER_SINGLE_VALUE_TAGS, HEADER_MULTI_VALUE_TAGS)

    def valid(self):
        return self.format_version is not None


class OboStanza(Base):

    def __init__(self, single_value_tags, multi_value_tags):
        super(OboStanza, self).__init__(single_value_tags, multi_value_tags)
        self._qualifiers = {}

    def add_qualifiers(self, attribute, qualifiers):
        self._qualifiers[attribute] = qualifiers

    def valid(self):
        return True


class OboTerm(OboStanza):

    def __init__(self):
        super(OboTerm, self).__init__(TERM_SINGLE_VALUE_TAGS, TERM_MULTI_VALUE_TAGS)
        pass


class OboTypedef(OboStanza):

    def __init__(self):
        super(OboTypedef, self).__init__(TYPEDEF_SINGLE_VALUE_TAGS, TYPEDEF_MULTI_VALUE_TAGS)
        pass
