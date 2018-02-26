import unittest

from prestans.devel.gen.closure import udl_to_cc


class ClosureTest(unittest.TestCase):

    def test_udl_to_cc(self):
        self.assertEquals(udl_to_cc("name"), "Name")
        self.assertEquals(udl_to_cc("first_name"), "FirstName")
        self.assertEquals(udl_to_cc("last_name"), "LastName")
        self.assertEquals(udl_to_cc("last_name_field"), "LastNameField")
