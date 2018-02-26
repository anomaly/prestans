import unittest

from prestans import exception
from prestans.types import Integer


class IntegerUnitTest(unittest.TestCase):

    def test_default(self):
        integer = Integer()
        self.assertIsNone(integer.default)

        integer = Integer(default=6)
        self.assertEquals(integer.default, 6)

    def test_required(self):
        required_default = Integer()
        self.assertTrue(required_default.required)

        required_true = Integer(required=True)
        self.assertTrue(required_true.required)

        required_false = Integer(required=False)
        self.assertFalse(required_false.required)

    def test_minimum(self):
        minimum_default = Integer()
        self.assertIsNone(minimum_default.minimum)

        minimum_value = Integer(minimum=1)
        self.assertEquals(minimum_value.minimum, 1)

    def test_maximum(self):
        maximum_default = Integer()
        self.assertIsNone(maximum_default.maximum)

        maximum_value = Integer(maximum=5)
        self.assertEquals(maximum_value.maximum, 5)

        self.assertRaises(ValueError, Integer, minimum=5, maximum=1)

    def test_choices(self):
        choices_default = Integer()
        self.assertIsNone(choices_default.choices)

        choices_value = Integer(choices=[1, 5])
        self.assertEquals(choices_value.choices, [1, 5])

    def test_description(self):
        desc_default = Integer()
        self.assertIsNone(desc_default.description)

        desc_value = Integer(description="description")
        self.assertEquals(desc_value.description, "description")

    def test_blueprint(self):
        integer = Integer()
        blueprint = integer.blueprint()
        self.assertEquals(blueprint["type"], "integer")
        self.assertEquals(blueprint["constraints"]["default"], None)
        self.assertEquals(blueprint["constraints"]["minimum"], None)
        self.assertEquals(blueprint["constraints"]["maximum"], None)
        self.assertEquals(blueprint["constraints"]["required"], True)
        self.assertEquals(blueprint["constraints"]["choices"], None)
        self.assertEquals(blueprint["constraints"]["description"], None)

        integer = Integer(
            default=3,
            minimum=1,
            maximum=5,
            required=False,
            choices=[1, 3, 5],
            description="description"
        )
        blueprint = integer.blueprint()
        self.assertEquals(blueprint["type"], "integer")
        self.assertEquals(blueprint["constraints"]["default"], 3)
        self.assertEquals(blueprint["constraints"]["minimum"], 1)
        self.assertEquals(blueprint["constraints"]["maximum"], 5)
        self.assertEquals(blueprint["constraints"]["required"], False)
        self.assertEquals(blueprint["constraints"]["choices"], [1, 3, 5])
        self.assertEquals(blueprint["constraints"]["description"], "description")

    def test_validate(self):

        integer = Integer(required=False)
        self.assertEquals(integer.validate(None), None)

        # check required raises exception for None
        self.assertRaises(exception.RequiredAttributeError, Integer().validate, None)

        # check default values being applied
        self.assertEquals(Integer(required=True, default=5).validate(None), 5)
        self.assertEquals(Integer(required=False, default=6).validate(None), 6)

        # check less than minimum
        self.assertRaises(exception.LessThanMinimumError, Integer(minimum=3).validate, 2)

        # check more than maximum
        self.assertRaises(exception.MoreThanMaximumError, Integer(maximum=3).validate, 4)

        # check not in choices
        self.assertRaises(exception.InvalidChoiceError, Integer(choices=[1, 3, 5]).validate, 2)
        self.assertEquals(Integer(choices=[2, 4]).validate(4), 4)

        # check non-integer raise parse error
        self.assertRaises(exception.ParseFailedError, Integer().validate, "string")
