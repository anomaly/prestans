import unittest

from prestans import exception
from prestans.types import Boolean


class BooleanUnitTest(unittest.TestCase):

    def test_required(self):
        required_default = Boolean()
        self.assertEqual(required_default.required, True)

        required_true = Boolean(required=True)
        self.assertEqual(required_true.required, True)

        required_false = Boolean(required=False)
        self.assertEqual(required_false.required, False)

    def test_default(self):
        default_none = Boolean()
        self.assertEqual(default_none.default, None)

        default_true = Boolean(default=True)
        self.assertEqual(default_true.default, True)

        default_false = Boolean(default=False)
        self.assertEqual(default_false.default, False)

        self.assertRaises(TypeError, Boolean, default="string")
        self.assertRaises(TypeError, Boolean, default=23)

    def test_description(self):
        boolean = Boolean(description="description")
        self.assertEqual(boolean.description, "description")

    def test_blueprint(self):
        boolean = Boolean()
        blueprint = boolean.blueprint()
        self.assertEqual(blueprint["type"], "boolean")
        self.assertEqual(blueprint["constraints"]["default"], None)
        self.assertEqual(blueprint["constraints"]["required"], True)
        self.assertEqual(blueprint["constraints"]["description"], None)

        boolean = Boolean(required=False, default=True, description="description")
        blueprint = boolean.blueprint()
        self.assertEqual(blueprint["type"], "boolean")
        self.assertEqual(blueprint["constraints"]["default"], True)
        self.assertEqual(blueprint["constraints"]["required"], False)
        self.assertEqual(blueprint["constraints"]["description"], "description")

    def test_validate(self):

        # not required and no default
        boolean = Boolean(required=False)
        self.assertEqual(boolean.validate(None), None)

        # required and no default
        boolean = Boolean(required=True)
        self.assertRaises(exception.RequiredAttributeError, boolean.validate, None)

        # required with default
        boolean = Boolean(required=True, default=True)
        self.assertEqual(boolean.validate(None), True)

        # not required with default
        boolean = Boolean(required=False, default=False)
        self.assertEqual(boolean.validate(None), False)

        # check invalid type parse fails
        boolean = Boolean()
        self.assertRaises(exception.ParseFailedError, boolean.validate, "string")
        self.assertRaises(exception.ParseFailedError, boolean.validate, 23)
        self.assertRaises(exception.ParseFailedError, boolean.validate, 34.67)
