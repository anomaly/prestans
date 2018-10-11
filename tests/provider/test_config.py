import unittest

from prestans.provider import Config


class ProviderConfigUnitTest(unittest.TestCase):

    def test_blueprint(self):
        blueprint = Config().blueprint()
        self.assertEqual(blueprint, {})

    def test_authentication(self):
        config = Config()
        self.assertEqual(config.authentication, None)

        from prestans.provider.auth import Base
        auth = Base()
        config.authentication = auth
        self.assertEqual(config.authentication, auth)

    def test_throttle(self):
        config = Config()
        self.assertEqual(config.throttle, None)

        from prestans.provider.throttle import Base
        throttle = Base()
        config.throttle = throttle
        self.assertEqual(config.throttle, throttle)

    def test_cache(self):
        config = Config()
        self.assertEqual(config.cache, None)

        from prestans.provider.cache import Base
        cache = Base()
        config.cache = cache
        self.assertEqual(config.cache, cache)
