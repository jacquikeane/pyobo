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


header_tvp = ['ontology', 'format_version', 'date', 'default_namespace', 'saved_by', 'auto_generated_by',
              'data_version', 'default_relationship_id_prefix']
header_mtvp = ['remark', 'import_', 'subsetdef', 'synonymtypedef', 'idspace', 'treat_xrefs_as_equivalent',
               'treat_xrefs_as_genus_differentia', 'treat_xrefs_as_reverse_genus_differentia',
               'treat_xrefs_as_relationship',
               'treat_xrefs_as_is_a', 'treat_xrefs_as_has_subclass', 'property_value', 'owl_axioms', 'id_mapping',
               'relax_unique_identifier_assumption_for_namespace',
               'relax_unique_label_assumption_for_namespace'
               ]


class OboHeader(Base):

    def __init__(self):
        for tvp in header_tvp:
            self.__dict__[tvp] = None
        for tvp in header_mtvp:
            self.__dict__[tvp] = []
        pass

    def valid(self):
        return self.format_version is not None
