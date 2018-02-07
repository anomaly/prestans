import unittest

from prestans.ext.data.adapters import ModelAdapter
from prestans import types


class ModelAdapterTest(unittest.TestCase):

    def test_rest_model_class(self):

        class PythonObject(object):
            pass

        class RESTModel(types.Model):
            name = types.String()

        model_adapter = ModelAdapter(rest_model_class=RESTModel, persistent_model_class=PythonObject)
        self.assertEquals(model_adapter.rest_model_class, RESTModel)
        self.assertEquals(model_adapter.persistent_model_class, PythonObject)

        self.assertRaises(TypeError, ModelAdapter, rest_model_class=PythonObject, persistent_model_class=None)

    def test_persistent_model_class(self):
        class PythonObject(object):
            pass

        class RESTModel(types.Model):
            name = types.String()

        model_adapter = ModelAdapter(rest_model_class=RESTModel, persistent_model_class=PythonObject)
        self.assertEquals(model_adapter.rest_model_class, RESTModel)
        self.assertEquals(model_adapter.persistent_model_class, PythonObject)

    def test_adapt_persistent_to_rest(self):
        class MyModel(types.Model):
            name = types.String()

        model_adapter = ModelAdapter(MyModel, None)
        self.assertRaises(NotImplementedError, model_adapter.adapt_persistent_to_rest, None)
