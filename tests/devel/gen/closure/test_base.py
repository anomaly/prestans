import unittest

from prestans.devel.gen.closure import Base
from prestans.devel.gen.closure import AttributeMetaData
from prestans import types


class BaseTest(unittest.TestCase):

    def test_init(self):

        base = Base(
            template_engine=None,
            model_file="models.py",
            namespace="namespace.models",
            output_directory="namespace/models"
        )
        self.assertIsNone(base._template_engine)
        self.assertEquals(base._model_file, "models.py")
        self.assertEquals(base._namespace, "namespace.models")
        self.assertEquals(base._output_directory, "namespace/models")
        self.assertEquals(base._dependencies, [])
        self.assertEquals(base.attribute_string, "")

    def test_add_filter_dependency(self):
        base = Base(
            template_engine=None,
            model_file="models.py",
            namespace="namespace.filters",
            output_directory="namespace/filters"
        )
        self.assertEquals(base._dependencies, [])

        class User(types.Model):
            first_name = types.String()

        user_blueprint = User().blueprint()
        user_blueprint["map_name"] = "a"

        base.add_filter_dependency(AttributeMetaData("user", user_blueprint))
        self.assertEquals(base._dependencies, ["namespace.filters.User"])

        users_blueprint = types.Array(element_template=User()).blueprint()
        users_blueprint["map_name"] = "b"

        base.add_filter_dependency(AttributeMetaData("users", users_blueprint))
        self.assertEquals(base._dependencies, ["namespace.filters.User"])

        class Log(types.Model):
            message = types.String()

        logs_blueprint = types.Array(element_template=Log()).blueprint()
        logs_blueprint["map_name"] = "c"

        base.add_filter_dependency(AttributeMetaData("logs", logs_blueprint))
        self.assertEquals(base._dependencies, ["namespace.filters.User", "namespace.filters.Log"])

    def test_add_model_dependency(self):
        base = Base(
            template_engine=None,
            model_file="models.py",
            namespace="namespace.models",
            output_directory="namespace/models"
        )
        self.assertEquals(base._dependencies, [])

        class User(types.Model):
            first_name = types.String()

        model_blueprint = User().blueprint()
        model_blueprint["map_name"] = "a"

        base.add_model_dependency(AttributeMetaData("user", model_blueprint))
        self.assertEquals(base._dependencies, ["namespace.models.User"])

        string_blueprint = types.String().blueprint()
        string_blueprint["map_name"] = "a_b"

        base.add_model_dependency(AttributeMetaData("first_name", string_blueprint))
        self.assertEquals(base._dependencies, ["namespace.models.User", "prestans.types.String"])

        array_basic = types.Array(element_template=types.String()).blueprint()
        array_basic["map_name"] = "c"

        base.add_model_dependency(AttributeMetaData("tags", array_basic))
        self.assertEquals(base._dependencies, ["namespace.models.User", "prestans.types.String"])

        array_model = types.Array(element_template=User()).blueprint()
        array_model["map_name"] = "d"

        base.add_model_dependency(AttributeMetaData("users", array_model))
        self.assertEquals(base._dependencies, ["namespace.models.User", "prestans.types.String"])

        integer_blueprint = types.Integer().blueprint()
        integer_blueprint["map_name"] = "e"

        base.add_model_dependency(AttributeMetaData("numbers", integer_blueprint))
        self.assertEquals(
            base._dependencies,
            ["namespace.models.User", "prestans.types.String", "prestans.types.Integer"]
        )

    def test_add_attribute_string(self):
        base = Base(
            template_engine=None,
            model_file="models.py",
            namespace="namespace.models",
            output_directory="namespace/models"
        )
        self.assertEquals(base.attribute_string, "")

        string_blueprint = types.String().blueprint()
        string_blueprint["map_name"] = "a"

        base.add_attribute_string(AttributeMetaData("string", string_blueprint))
        self.assertEquals(base.attribute_string, "this.string_")

        class MyModel(types.Model):
            field = types.String()

        model_blueprint = MyModel().blueprint()
        model_blueprint["map_name"] = "b"

        base.add_attribute_string(AttributeMetaData("model", model_blueprint))
        self.assertEquals(base.attribute_string, "this.string_ || this.model_.anyFieldsEnabled()")

        array_blueprint = types.Array(element_template=MyModel()).blueprint()
        array_blueprint["map_name"] = "c"

        base.add_attribute_string(AttributeMetaData("array", array_blueprint))
        self.assertEquals(
            base.attribute_string,
            "this.string_ || this.model_.anyFieldsEnabled() || this.array_.anyFieldsEnabled()"
        )
