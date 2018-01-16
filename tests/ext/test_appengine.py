from mock import MagicMock, patch
import unittest

from prestans.ext.appengine import AppEngineAuthContextProvider
from prestans.ext.appengine import AppEngineMemcacheProvider


class AppEngineAuthContextProviderTest(unittest.TestCase):

    def setUp(self):
        self.gae_mock = MagicMock()
        self.gae_mock.google.appengine.api.users.get_current_user.return_value = 72
        self.gae_mock.google.appengine.api.oauth.get_current_user.return_value = 66
        self.gae_mock.google.appengine.api.oauth.get_current_user.side_effect = Exception
        self.gae_mock.google.appengine.api.oauth.OAuthRequestError = Exception

        gae_modules = {
            "google": self.gae_mock.google,
            "google.appengine": self.gae_mock.google.appengine,
            "google.appengine.api": self.gae_mock.google.appengine.api
        }

        self.module_patcher = patch.dict('sys.modules', gae_modules)
        self.module_patcher.start()

    def tearDown(self):
        self.module_patcher.stop()

    def test_is_authenticated_user(self):

        # check if user found
        auth = AppEngineAuthContextProvider()
        self.assertTrue(auth.is_authenticated_user())
        self.gae_mock.google.appengine.api.users.get_current_user.assert_called_with()

        self.gae_mock.google.appengine.api.users.get_current_user.return_value = None

        # check if user not found
        self.assertFalse(auth.is_authenticated_user())
        self.gae_mock.google.appengine.api.users.get_current_user.assert_called_with()

    def test_get_current_user_production(self):

        import prestans.ext.appengine
        prestans.ext.appengine._IS_DEVELOPMENT_SERVER = False

        # production: oauth missing
        auth = AppEngineAuthContextProvider()
        self.assertEquals(auth.get_current_user(), 72)
        self.gae_mock.google.appengine.api.oauth.get_current_user.assert_called_with()
        self.gae_mock.google.appengine.api.users.get_current_user.assert_called_with()

        # production oauth found
        self.gae_mock.google.appengine.api.oauth.get_current_user.side_effect = None
        self.assertEquals(auth.get_current_user(), 66)
        self.gae_mock.google.appengine.api.oauth.get_current_user.assert_called_with()
        self.gae_mock.google.appengine.api.users.get_current_user.assert_called_with()

    def test_get_current_user_development(self):
        # development oauth not called
        import prestans.ext.appengine
        prestans.ext.appengine._IS_DEVELOPMENT_SERVER = True

        auth = AppEngineAuthContextProvider()
        self.assertEquals(auth.get_current_user(), 72)
        self.gae_mock.google.appengine.api.oauth.get_current_user.assert_not_called()
        self.gae_mock.google.appengine.api.users.get_current_user.assert_called_with()




class AppEngineMemcacheProviderTest(unittest.TestCase):

    def setUp(self):
        self.gae_mock = MagicMock()
        self.gae_mock.google.appengine.api.memcache.get.return_value = "value"
        self.gae_mock.google.appengine.api.memcache.set.return_value = True
        self.gae_mock.google.appengine.api.memcache.add.return_value = True
        self.gae_mock.google.appengine.api.memcache.delete.return_value = True
        self.gae_mock.google.appengine.api.memcache.flush_all.return_value = True

        gae_modules = {
            "google": self.gae_mock.google,
            "google.appengine": self.gae_mock.google.appengine,
            "google.appengine.api": self.gae_mock.google.appengine.api
        }

        self.module_patcher = patch.dict('sys.modules', gae_modules)
        self.module_patcher.start()

    def tearDown(self):
        self.module_patcher.stop()

    def test_get(self):
        memcache = AppEngineMemcacheProvider()
        self.assertEquals(memcache.get("key"), "value")
        self.gae_mock.google.appengine.api.memcache.get.assert_called_with("key", None, False)

        self.assertEquals(memcache.get("key", "namespace", True), "value")
        self.gae_mock.google.appengine.api.memcache.get.assert_called_with("key", "namespace", True)

    def test_set(self):
        memcache = AppEngineMemcacheProvider()
        self.assertTrue(memcache.set("key", "value"))
        self.gae_mock.google.appengine.api.memcache.set.assert_called_with("key", "value", 0, 0, None)

        self.assertTrue(memcache.set("key", "value", 10, 20, "namespace"))
        self.gae_mock.google.appengine.api.memcache.set.assert_called_with("key", "value", 10, 20, "namespace")

    def test_add(self):
        memcache = AppEngineMemcacheProvider()
        self.assertTrue(memcache.add("key", "value"))
        self.gae_mock.google.appengine.api.memcache.add.assert_called_with("key", "value", 0, 0, None)

        self.assertTrue(memcache.add("key", "value", 100, 200, "namespace"))
        self.gae_mock.google.appengine.api.memcache.add.assert_called_with("key", "value", 100, 200, "namespace")

    def test_delete(self):
        memcache = AppEngineMemcacheProvider()
        self.assertTrue(memcache.delete("key"))
        self.gae_mock.google.appengine.api.memcache.delete.assert_called_with("key", 0, None)

        self.assertTrue(memcache.delete("key", 30, "namespace"))
        self.gae_mock.google.appengine.api.memcache.delete.assert_called_with("key", 30, "namespace")

    def test_flush_all(self):
        memcache = AppEngineMemcacheProvider()
        self.assertTrue(memcache.flush_all())
        self.gae_mock.google.appengine.api.memcache.flush_all.assert_called()
