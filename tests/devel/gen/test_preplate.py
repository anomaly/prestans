from mock import patch
import unittest

from prestans.devel.gen import Preplate


class PreplateTest(unittest.TestCase):

    def test_init(self):
        preplate = Preplate(
            template_type="closure.model",
            models_definition="project/models.py",
            namespace="project.namespace.models",
            filter_namespace="project.namespace.filters",
            output_directory="project/namespace/models"
        )
        self.assertEqual(preplate.template_type, "closure.model")
        self.assertEqual(preplate.models_definition, "project/models.py")
        self.assertEqual(preplate.namespace, "project.namespace.models")
        self.assertEqual(preplate.filter_namespace, "project.namespace.filters")
        self.assertEqual(preplate.output_directory, "project/namespace/models")

        from jinja2 import Environment
        self.assertTrue(isinstance(preplate.template_engine, Environment))

    def test_run_unknown_template(self):
        preplate = Preplate(
            template_type="closure.unknown",
            models_definition="models.py",
            namespace="namespace.models",
            filter_namespace="project.namespace.filters",
            output_directory="namespace/models"
        )
        self.assertEqual(preplate.run(), 1)

    @patch("prestans.devel.gen.closure.Model.run", return_value=0)
    @patch("prestans.devel.gen.closure.Model.__init__", return_value=None)
    def test_run_closure_model(self, model_init, model_run):
        preplate = Preplate(
            template_type="closure.model",
            models_definition="models.py",
            namespace="namespace.models",
            filter_namespace="namespace.filters",
            output_directory="namespace/models"
        )
        self.assertEqual(preplate.run(), 0)
        model_init.assert_called_with(
            template_engine=preplate.template_engine,
            models_definition=preplate.models_definition,
            namespace=preplate.namespace,
            filter_namespace=preplate.filter_namespace,
            output_directory=preplate.output_directory
        )
        model_run.assert_called()

    @patch("prestans.devel.gen.closure.Filter.run", return_value=0)
    @patch("prestans.devel.gen.closure.Filter.__init__", return_value=None)
    def test_run_closure_filter(self, filter_init, filter_run):
        preplate = Preplate(
            template_type="closure.filter",
            models_definition="models.py",
            namespace="namespace.filter",
            filter_namespace="namespace.filters",
            output_directory="namespace/filter"
        )
        self.assertEqual(preplate.run(), 0)
        filter_init.assert_called_with(
            template_engine=preplate.template_engine,
            models_definition=preplate.models_definition,
            namespace=preplate.namespace,
            output_directory=preplate.output_directory
        )
        filter_run.assert_called()
