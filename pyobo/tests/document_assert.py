import unittest


def extract_dictionary(list):
    return [x.__dict__ for x in list]


class DocumentAsserter(unittest.TestCase):

    def assertDocumentEquals(self, expected, actual):
        self.assertEquals(expected.header.__dict__, actual.header.__dict__)
        self.assertEqualsByContent(expected.terms, actual.terms)
        self.assertEqualsByContent(expected.typedefs, actual.typedefs)

    def assertEqualsByContent(self, actual, expected):
        actual_dict = extract_dictionary(actual)
        expected_dict = extract_dictionary(expected)
        self.assertEqual(actual_dict, expected_dict)
