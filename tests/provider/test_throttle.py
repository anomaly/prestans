import unittest

from prestans.provider.throttle import Base


class ThrottleBaseUnitTest(unittest.TestCase):

    def test_debug(self):
        base = Base()
        self.assertEquals(base.debug, False)

        base.debug = True
        self.assertEqual(base.debug, True)
