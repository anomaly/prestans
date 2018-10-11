import unittest

from prestans import exception
from prestans.types import Float


class FloatUnitTest(unittest.TestCase):

    def test_default(self):
        default_default = Float()
        self.assertIsNone(default_default.default)

        default_value = Float(default=6.0)
        self.assertEqual(default_value.default, 6.0)

    def test_minimum(self):
        minimum_default = Float()
        self.assertIsNone(minimum_default.minimum)

        minimum_value = Float(minimum=2.2)
        self.assertEqual(minimum_value.minimum, 2.2)

    def test_maximum(self):
        maximum_default = Float()
        self.assertIsNone(maximum_default.maximum)

        maximum_value = Float(maximum=5.5)
        self.assertEqual(maximum_value.maximum, 5.5)

        self.assertRaises(ValueError, Float, minimum=5.5, maximum=1.1)

    def test_required(self):
        required_default = Float()
        self.assertTrue(required_default.required)

        required_true = Float(required=True)
        self.assertTrue(required_true.required)

        required_false = Float(required=False)
        self.assertFalse(required_false.required)

    def test_choices(self):
        choices_default = Float()
        self.assertIsNone(choices_default.choices)

        choices_value = Float(choices=[1.0, 3.0])
        self.assertEqual(choices_value.choices, [1.0, 3.0])

    def test_description(self):
        description_default = Float()
        self.assertIsNone(description_default.description)

        description_value = Float(description="description")
        self.assertEqual(description_value.description, "description")

    def test_blueprint(self):
        float = Float()
        blueprint = float.blueprint()
        self.assertEqual(blueprint["type"], "float")
        self.assertEqual(blueprint["constraints"]["default"], None)
        self.assertEqual(blueprint["constraints"]["minimum"], None)
        self.assertEqual(blueprint["constraints"]["maximum"], None)
        self.assertEqual(blueprint["constraints"]["required"], True)
        self.assertEqual(blueprint["constraints"]["choices"], None)
        self.assertEqual(blueprint["constraints"]["description"], None)

        float = Float(
            default=3.3,
            minimum=1.1,
            maximum=5.5,
            required=False,
            choices=[1.1, 3.3, 5.5],
            description="description"
        )
        blueprint = float.blueprint()
        self.assertEqual(blueprint["type"], "float")
        self.assertEqual(blueprint["constraints"]["default"], 3.3)
        self.assertEqual(blueprint["constraints"]["minimum"], 1.1)
        self.assertEqual(blueprint["constraints"]["maximum"], 5.5)
        self.assertEqual(blueprint["constraints"]["required"], False)
        self.assertEqual(blueprint["constraints"]["choices"], [1.1, 3.3, 5.5])
        self.assertEqual(blueprint["constraints"]["description"], "description")

    def test_validate(self):

        float = Float(required=False)
        self.assertEqual(float.validate(None), None)

        # check required raises exception for None
        self.assertRaises(exception.RequiredAttributeError, Float().validate, None)

        # check default values being applied
        self.assertEqual(Float(required=True, default=5.5).validate(None), 5.5)
        self.assertEqual(Float(required=False, default=6.6).validate(None), 6.6)

        # check less than minimum
        self.assertRaises(exception.LessThanMinimumError, Float(minimum=3.3).validate, 2.2)

        # check more than maximum
        self.assertRaises(exception.MoreThanMaximumError, Float(maximum=3.3).validate, 4.4)

        # check not in choices
        self.assertRaises(exception.InvalidChoiceError, Float(choices=[1.1, 3.3, 5.5]).validate, 2.2)
        self.assertEqual(Float(choices=[2.2, 4.4]).validate(4.4), 4.4)

        # check non-integer raise parse error
        self.assertRaises(exception.ParseFailedError, Float().validate, "string")
