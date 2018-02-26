from mock import patch
import unittest

from prestans.devel.gen import Preplate


class PreplateTest(unittest.TestCase):

    def test_init(self):
        preplate = Preplate(
            template_type="closure.model",
            model_file="project/models.py",
            namespace="project.namespace.models",
            filter_namespace="project.namespace.filters",
            output_directory="project/namespace/models"
        )
        self.assertEquals(preplate.template_type, "closure.model")
        self.assertEquals(preplate.model_file, "project/models.py")
        self.assertEquals(preplate.namespace, "project.namespace.models")
        self.assertEquals(preplate.filter_namespace, "project.namespace.filters")
        self.assertEquals(preplate.output_directory, "project/namespace/models")

        from jinja2 import Environment
        self.assertTrue(isinstance(preplate.template_engine, Environment))


    def test_run_unknown_template(self):
        preplate = Preplate(
            template_type="closure.unknown",
            model_file="models.py",
            namespace="namespace.models",
            filter_namespace="project.namespace.filters",
            output_directory="namespace/models"
        )
        self.assertEquals(preplate.run(), 1)

    @patch("prestans.devel.gen.closure.Model.run", return_value=0)
    @patch("prestans.devel.gen.closure.Model.__init__", return_value=None)
    def test_run_closure_model(self, model_init, model_run):
        preplate = Preplate(
            template_type="closure.model",
            model_file="models.py",
            namespace="namespace.models",
            filter_namespace="namespace.filters",
            output_directory="namespace/models"
        )
        self.assertEquals(preplate.run(), 0)
        model_init.assert_called_with(
            template_engine=preplate.template_engine,
            model_file=preplate.model_file,
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
            model_file="models.py",
            namespace="namespace.filter",
            filter_namespace="namespace.filters",
            output_directory="namespace/filter"
        )
        self.assertEquals(preplate.run(), 0)
        filter_init.assert_called_with(
            template_engine=preplate.template_engine,
            model_file=preplate.model_file,
            namespace=preplate.namespace,
            output_directory=preplate.output_directory
        )
        filter_run.assert_called()
