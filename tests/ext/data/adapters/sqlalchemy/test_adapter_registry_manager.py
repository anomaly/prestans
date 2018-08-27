import unittest

from prestans.ext.data import adapters
from prestans import types


class PersistentModelA(object):
    pass

class PersistentModelB(object):
    pass

class RESTModelA(types.Model):
    pass


class RESTModelB(types.Model):
    pass


class AdapterRegistryManagerTest(unittest.TestCase):

    def test_registry_singleton(self):
        self.assertTrue(isinstance(adapters.registry, adapters.AdapterRegistryManager))

    def test_generate_signature(self):
        rest_a_class_sig = adapters.AdapterRegistryManager.generate_signature(RESTModelA)
        rest_a_instance_sig = adapters.AdapterRegistryManager.generate_signature(RESTModelA())
        rest_b_class_sig = adapters.AdapterRegistryManager.generate_signature(RESTModelB)
        rest_b_instance_sig = adapters.AdapterRegistryManager.generate_signature(RESTModelB())
        persistent_class_sig = adapters.AdapterRegistryManager.generate_signature(PersistentModelA)
        persistent_instance_sig = adapters.AdapterRegistryManager.generate_signature(PersistentModelA())

        self.assertEquals(rest_a_class_sig, rest_a_instance_sig)
        self.assertEquals(rest_b_class_sig, rest_b_instance_sig)
        self.assertEquals(persistent_class_sig, persistent_instance_sig)

        self.assertNotEquals(rest_a_class_sig, rest_b_class_sig)
        self.assertNotEquals(rest_a_instance_sig, rest_b_instance_sig)
        self.assertNotEquals(rest_a_class_sig, persistent_class_sig)

    def test_init(self):
        registry_manager = adapters.AdapterRegistryManager()
        self.assertEquals(registry_manager._rest_map, {})
        self.assertEquals(registry_manager._persistent_map, {})

    def test_register_adapter_of_incorrect_type(self):
        registry_manager = adapters.AdapterRegistryManager()
        self.assertRaises(TypeError, registry_manager.register_adapter, None)
        self.assertRaises(TypeError, registry_manager.register_adapter, "string")

        self.assertEquals(registry_manager._rest_map, {})
        self.assertEquals(registry_manager._persistent_map, {})

    def test_register_adapter_of_correct_type(self):

        registry_manager = adapters.AdapterRegistryManager()
        registry_manager.register_adapter(adapters.ModelAdapter(
            rest_model_class=RESTModelA,
            persistent_model_class=PersistentModelA
        ))

        # fetch via the REST model
        found_adapter = registry_manager.get_adapter_for_rest_model(RESTModelA())
        self.assertEquals(found_adapter.rest_model_class, RESTModelA)
        self.assertEquals(found_adapter.persistent_model_class, PersistentModelA)

        # fetch via the persistent model
        found_adapter = registry_manager.get_adapter_for_persistent_model(PersistentModelA())
        self.assertEquals(found_adapter.rest_model_class, RESTModelA)
        self.assertEquals(found_adapter.persistent_model_class, PersistentModelA)

    def test_unknown_adapter_raises_exception(self):

        registry_manager = adapters.AdapterRegistryManager()
        registry_manager.register_adapter(adapters.ModelAdapter(
            rest_model_class=RESTModelA,
            persistent_model_class=PersistentModelA
        ))

        # fetch via the REST model
        found_adapter = registry_manager.get_adapter_for_rest_model(RESTModelA())
        self.assertEquals(found_adapter.rest_model_class, RESTModelA)
        self.assertEquals(found_adapter.persistent_model_class, PersistentModelA)

        # fetch via the persistent model
        found_adapter = registry_manager.get_adapter_for_persistent_model(PersistentModelA())
        self.assertEquals(found_adapter.rest_model_class, RESTModelA)
        self.assertEquals(found_adapter.persistent_model_class, PersistentModelA)

        self.assertRaises(TypeError, registry_manager.get_adapter_for_rest_model, RESTModelB)
        self.assertRaises(TypeError, registry_manager.get_adapter_for_persistent_model, PersistentModelB)

    def test_register_persistent_rest_pair(self):
        registry_manager = adapters.AdapterRegistryManager()
        registry_manager.register_persistent_rest_pair(
            persistent_model_class=PersistentModelA,
            rest_model_class=RESTModelA
        )

        # fetch via the REST model
        found_adapter = registry_manager.get_adapter_for_rest_model(RESTModelA())
        self.assertEquals(found_adapter.rest_model_class, RESTModelA)
        self.assertEquals(found_adapter.persistent_model_class, PersistentModelA)

        # fetch via the persistent model
        found_adapter = registry_manager.get_adapter_for_persistent_model(PersistentModelA())
        self.assertEquals(found_adapter.rest_model_class, RESTModelA)
        self.assertEquals(found_adapter.persistent_model_class, PersistentModelA)

    def test_clear_registered_adapters(self):
        registry_manager = adapters.AdapterRegistryManager()
        registry_manager.register_adapter(adapters.ModelAdapter(
            rest_model_class=RESTModelA,
            persistent_model_class=PersistentModelA
        ))

        # fetch via the REST model
        found_adapter = registry_manager.get_adapter_for_rest_model(RESTModelA())
        self.assertEquals(found_adapter.rest_model_class, RESTModelA)
        self.assertEquals(found_adapter.persistent_model_class, PersistentModelA)

        # fetch via the persistent model
        found_adapter = registry_manager.get_adapter_for_persistent_model(PersistentModelA())
        self.assertEquals(found_adapter.rest_model_class, RESTModelA)
        self.assertEquals(found_adapter.persistent_model_class, PersistentModelA)

        # clear the registry
        registry_manager.clear_registered_adapters()

        # check they have been cleared
        self.assertRaises(TypeError, registry_manager.get_adapter_for_rest_model, RESTModelA())
        self.assertRaises(TypeError, registry_manager.get_adapter_for_persistent_model, PersistentModelA())
