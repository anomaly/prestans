import unittest

from prestans.devel.gen.closure import AttributeMetaData
from prestans import types


class AttributeMetaDataTest(unittest.TestCase):

    def test_string_default(self):
        string_type = types.String()

        blueprint = string_type.blueprint()
        blueprint["map_name"] = "a_b"
        string_meta = AttributeMetaData("first_name", blueprint)
        self.assertEqual(string_meta.name, "first_name")
        self.assertEqual(string_meta.map_name, "a_b")
        self.assertEqual(string_meta.cc, "FirstName")
        self.assertEqual(string_meta.ccif, "firstName")
        self.assertEqual(string_meta.blueprint_type, "string")
        self.assertEqual(string_meta.client_class_name, "String")
        self.assertEqual(string_meta.required, "true")
        self.assertEqual(string_meta.trim, "true")
        self.assertEqual(string_meta.default, "null")
        self.assertEqual(string_meta.format, "null")
        self.assertEqual(string_meta.choices, "null")
        self.assertEqual(string_meta.min_length, "null")
        self.assertEqual(string_meta.max_length, "null")

    def test_string_given_values(self):
        string_type = types.String(
            required=False,
            trim=False,
            default="default",
            format="[a-z]{2,8}",
            choices=["a", "b", "c"],
            min_length=2,
            max_length=8
        )

        blueprint = string_type.blueprint()
        blueprint["map_name"] = "a_b"
        string_meta = AttributeMetaData("first_name", blueprint)
        self.assertEqual(string_meta.name, "first_name")
        self.assertEqual(string_meta.map_name, "a_b")
        self.assertEqual(string_meta.cc, "FirstName")
        self.assertEqual(string_meta.ccif, "firstName")
        self.assertEqual(string_meta.blueprint_type, "string")
        self.assertEqual(string_meta.client_class_name, "String")
        self.assertEqual(string_meta.required, "false")
        self.assertEqual(string_meta.trim, "false")
        self.assertEqual(string_meta.default, "\"default\"")
        self.assertEqual(string_meta.format, "\"[a-z]{2,8}\"")
        self.assertEqual(string_meta.choices, ["a", "b", "c"])
        self.assertEqual(string_meta.min_length, 2)
        self.assertEqual(string_meta.max_length, 8)

    def test_integer_default(self):
        integer_type = types.Integer()

        blueprint = integer_type.blueprint()
        blueprint["map_name"] = "a_b"
        integer_meta = AttributeMetaData("max_size", blueprint)
        self.assertEqual(integer_meta.name, "max_size")
        self.assertEqual(integer_meta.map_name, "a_b")
        self.assertEqual(integer_meta.cc, "MaxSize")
        self.assertEqual(integer_meta.ccif, "maxSize")
        self.assertEqual(integer_meta.blueprint_type, "integer")
        self.assertEqual(integer_meta.client_class_name, "Integer")
        self.assertEqual(integer_meta.required, "true")
        self.assertEqual(integer_meta.default, "null")
        self.assertEqual(integer_meta.choices, "null")
        self.assertEqual(integer_meta.minimum, "null")
        self.assertEqual(integer_meta.maximum, "null")

    def test_given_values(self):
        integer_type = types.Integer(
            required=False,
            default=3,
            choices=[1, 3, 5],
            minimum=1,
            maximum=5
        )

        blueprint = integer_type.blueprint()
        blueprint["map_name"] = "a_b"
        integer_meta = AttributeMetaData("max_size", blueprint)
        self.assertEqual(integer_meta.name, "max_size")
        self.assertEqual(integer_meta.map_name, "a_b")
        self.assertEqual(integer_meta.cc, "MaxSize")
        self.assertEqual(integer_meta.ccif, "maxSize")
        self.assertEqual(integer_meta.blueprint_type, "integer")
        self.assertEqual(integer_meta.client_class_name, "Integer")
        self.assertEqual(integer_meta.required, "false")
        self.assertEqual(integer_meta.default, 3)
        self.assertEqual(integer_meta.choices, [1, 3, 5])
        self.assertEqual(integer_meta.minimum, 1)
        self.assertEqual(integer_meta.maximum, 5)

    def test_float_default(self):
        float_type = types.Float()

        blueprint = float_type.blueprint()
        blueprint["map_name"] = "a_b"
        float_meta = AttributeMetaData("max_size", blueprint)
        self.assertEqual(float_meta.name, "max_size")
        self.assertEqual(float_meta.map_name, "a_b")
        self.assertEqual(float_meta.cc, "MaxSize")
        self.assertEqual(float_meta.ccif, "maxSize")
        self.assertEqual(float_meta.blueprint_type, "float")
        self.assertEqual(float_meta.client_class_name, "Float")
        self.assertEqual(float_meta.required, "true")
        self.assertEqual(float_meta.default, "null")
        self.assertEqual(float_meta.choices, "null")
        self.assertEqual(float_meta.minimum, "null")
        self.assertEqual(float_meta.maximum, "null")

    def test_float_given_values(self):
        float_type = types.Float(
            required=False,
            default=3.3,
            choices=[1.1, 3.3, 5.5],
            minimum=1.1,
            maximum=5.5
        )

        blueprint = float_type.blueprint()
        blueprint["map_name"] = "a_b"
        float_meta = AttributeMetaData("max_size", blueprint)
        self.assertEqual(float_meta.name, "max_size")
        self.assertEqual(float_meta.map_name, "a_b")
        self.assertEqual(float_meta.cc, "MaxSize")
        self.assertEqual(float_meta.ccif, "maxSize")
        self.assertEqual(float_meta.blueprint_type, "float")
        self.assertEqual(float_meta.client_class_name, "Float")
        self.assertEqual(float_meta.required, "false")
        self.assertEqual(float_meta.default, 3.3)
        self.assertEqual(float_meta.choices, [1.1, 3.3, 5.5])
        self.assertEqual(float_meta.minimum, 1.1)
        self.assertEqual(float_meta.maximum, 5.5)

    def test_boolean_default(self):
        boolean_type = types.Boolean()

        blueprint = boolean_type.blueprint()
        blueprint["map_name"] = "a_b"
        boolean_meta = AttributeMetaData("is_admin", blueprint)
        self.assertEqual(boolean_meta.name, "is_admin")
        self.assertEqual(boolean_meta.map_name, "a_b")
        self.assertEqual(boolean_meta.cc, "IsAdmin")
        self.assertEqual(boolean_meta.ccif, "isAdmin")
        self.assertEqual(boolean_meta.blueprint_type, "boolean")
        self.assertEqual(boolean_meta.client_class_name, "Boolean")
        self.assertEqual(boolean_meta.required, "true")
        self.assertEqual(boolean_meta.default, "null")

    def test_boolean_given_values(self):
        boolean_type = types.Boolean(
            required=False,
            default=True
        )

        blueprint = boolean_type.blueprint()
        blueprint["map_name"] = "a_b"
        boolean_meta = AttributeMetaData("is_admin", blueprint)
        self.assertEqual(boolean_meta.name, "is_admin")
        self.assertEqual(boolean_meta.map_name, "a_b")
        self.assertEqual(boolean_meta.cc, "IsAdmin")
        self.assertEqual(boolean_meta.ccif, "isAdmin")
        self.assertEqual(boolean_meta.blueprint_type, "boolean")
        self.assertEqual(boolean_meta.client_class_name, "Boolean")
        self.assertEqual(boolean_meta.required, "false")
        self.assertEqual(boolean_meta.default, "true")

        boolean_type = types.Boolean(
            required=False,
            default=False
        )

        blueprint = boolean_type.blueprint()
        blueprint["map_name"] = "a_b"
        boolean_meta = AttributeMetaData("is_admin", blueprint)
        self.assertEqual(boolean_meta.name, "is_admin")
        self.assertEqual(boolean_meta.map_name, "a_b")
        self.assertEqual(boolean_meta.cc, "IsAdmin")
        self.assertEqual(boolean_meta.ccif, "isAdmin")
        self.assertEqual(boolean_meta.blueprint_type, "boolean")
        self.assertEqual(boolean_meta.client_class_name, "Boolean")
        self.assertEqual(boolean_meta.required, "false")
        self.assertEqual(boolean_meta.default, "false")

    def test_datetime_default(self):
        datetime_type = types.DateTime()

        blueprint = datetime_type.blueprint()
        blueprint["map_name"] = "a_b"
        datetime_meta = AttributeMetaData("created_date", blueprint)
        self.assertEqual(datetime_meta.name, "created_date")
        self.assertEqual(datetime_meta.map_name, "a_b")
        self.assertEqual(datetime_meta.cc, "CreatedDate")
        self.assertEqual(datetime_meta.ccif, "createdDate")
        self.assertEqual(datetime_meta.blueprint_type, "datetime")
        self.assertEqual(datetime_meta.client_class_name, "DateTime")
        self.assertEqual(datetime_meta.required, "true")
        self.assertEqual(datetime_meta.default, "null")
        self.assertEqual(datetime_meta.timezone, "false")
        self.assertEqual(datetime_meta.utc, "false")

    def test_datetime_given_values(self):
        datetime_type = types.DateTime(
            required=False,
            default=types.DateTime.NOW,
            timezone=True,
            utc=True
        )

        blueprint = datetime_type.blueprint()
        blueprint["map_name"] = "a_b"
        datetime_meta = AttributeMetaData("created_date", blueprint)
        self.assertEqual(datetime_meta.name, "created_date")
        self.assertEqual(datetime_meta.map_name, "a_b")
        self.assertEqual(datetime_meta.cc, "CreatedDate")
        self.assertEqual(datetime_meta.ccif, "createdDate")
        self.assertEqual(datetime_meta.blueprint_type, "datetime")
        self.assertEqual(datetime_meta.client_class_name, "DateTime")
        self.assertEqual(datetime_meta.required, "false")
        self.assertEqual(datetime_meta.default, "prestans.types.DateTime.NOW")
        self.assertEqual(datetime_meta.timezone, "true")
        self.assertEqual(datetime_meta.utc, "true")

    def test_date_default(self):
        datetime_type = types.Date()

        blueprint = datetime_type.blueprint()
        blueprint["map_name"] = "a_b"
        datetime_meta = AttributeMetaData("created_date", blueprint)
        self.assertEqual(datetime_meta.name, "created_date")
        self.assertEqual(datetime_meta.map_name, "a_b")
        self.assertEqual(datetime_meta.cc, "CreatedDate")
        self.assertEqual(datetime_meta.ccif, "createdDate")
        self.assertEqual(datetime_meta.blueprint_type, "date")
        self.assertEqual(datetime_meta.client_class_name, "Date")
        self.assertEqual(datetime_meta.required, "true")
        self.assertEqual(datetime_meta.default, "null")

    def test_date_given_values(self):
        datetime_type = types.Date(
            required=False,
            default=types.Date.TODAY
        )

        blueprint = datetime_type.blueprint()
        blueprint["map_name"] = "a_b"
        datetime_meta = AttributeMetaData("created_date", blueprint)
        self.assertEqual(datetime_meta.name, "created_date")
        self.assertEqual(datetime_meta.map_name, "a_b")
        self.assertEqual(datetime_meta.cc, "CreatedDate")
        self.assertEqual(datetime_meta.ccif, "createdDate")
        self.assertEqual(datetime_meta.blueprint_type, "date")
        self.assertEqual(datetime_meta.client_class_name, "Date")
        self.assertEqual(datetime_meta.required, "false")
        self.assertEqual(datetime_meta.default, "prestans.types.Date.TODAY")

    def test_time_default(self):
        datetime_type = types.Time()

        blueprint = datetime_type.blueprint()
        blueprint["map_name"] = "a_b"
        datetime_meta = AttributeMetaData("opening_time", blueprint)
        self.assertEqual(datetime_meta.name, "opening_time")
        self.assertEqual(datetime_meta.map_name, "a_b")
        self.assertEqual(datetime_meta.cc, "OpeningTime")
        self.assertEqual(datetime_meta.ccif, "openingTime")
        self.assertEqual(datetime_meta.blueprint_type, "time")
        self.assertEqual(datetime_meta.client_class_name, "Time")
        self.assertEqual(datetime_meta.required, "true")
        self.assertEqual(datetime_meta.default, "null")

    def test_time_given_values(self):
        datetime_type = types.Time(
            required=False,
            default=types.Time.NOW
        )

        blueprint = datetime_type.blueprint()
        blueprint["map_name"] = "a_b"
        datetime_meta = AttributeMetaData("opening_time", blueprint)
        self.assertEqual(datetime_meta.name, "opening_time")
        self.assertEqual(datetime_meta.map_name, "a_b")
        self.assertEqual(datetime_meta.cc, "OpeningTime")
        self.assertEqual(datetime_meta.ccif, "openingTime")
        self.assertEqual(datetime_meta.blueprint_type, "time")
        self.assertEqual(datetime_meta.client_class_name, "Time")
        self.assertEqual(datetime_meta.required, "false")
        self.assertEqual(datetime_meta.default, "prestans.types.Time.NOW")

    def test_data_url_file_default(self):
        data_url_file_type = types.DataURLFile()

        blueprint = data_url_file_type.blueprint()
        blueprint["map_name"] = "b_a"
        data_url_file_meta = AttributeMetaData("file_download", blueprint)
        self.assertEqual(data_url_file_meta.name, "file_download")
        self.assertEqual(data_url_file_meta.map_name, "b_a")
        self.assertEqual(data_url_file_meta.cc, "FileDownload")
        self.assertEqual(data_url_file_meta.ccif, "fileDownload")
        self.assertEqual(data_url_file_meta.blueprint_type, "data_url_file")
        self.assertEqual(data_url_file_meta.client_class_name, "DataURLFile")
        self.assertEqual(data_url_file_meta.required, "true")
        self.assertEqual(data_url_file_meta.allowed_mime_types, [])

    def test_data_url_file_given_values(self):
        data_url_file_type = types.DataURLFile(
            required=False,
            allowed_mime_types=["text/plain"]
        )

        blueprint = data_url_file_type.blueprint()
        blueprint["map_name"] = "b_a"
        data_url_file_meta = AttributeMetaData("file_download", blueprint)
        self.assertEqual(data_url_file_meta.name, "file_download")
        self.assertEqual(data_url_file_meta.map_name, "b_a")
        self.assertEqual(data_url_file_meta.cc, "FileDownload")
        self.assertEqual(data_url_file_meta.ccif, "fileDownload")
        self.assertEqual(data_url_file_meta.blueprint_type, "data_url_file")
        self.assertEqual(data_url_file_meta.client_class_name, "DataURLFile")
        self.assertEqual(data_url_file_meta.required, "false")
        self.assertEqual(data_url_file_meta.allowed_mime_types, ["text/plain"])

    def test_model(self):
        class User(types.Model):
            first_name = types.String()

        blueprint = User().blueprint()
        blueprint["map_name"] = "b_a"
        data_url_file_meta = AttributeMetaData("my_model", blueprint)
        self.assertEqual(data_url_file_meta.name, "my_model")
        self.assertEqual(data_url_file_meta.map_name, "b_a")
        self.assertEqual(data_url_file_meta.cc, "MyModel")
        self.assertEqual(data_url_file_meta.ccif, "myModel")
        self.assertEqual(data_url_file_meta.blueprint_type, "model")
        self.assertEqual(data_url_file_meta.client_class_name, "Model")
        self.assertEqual(data_url_file_meta.required, "true")
        self.assertEqual(data_url_file_meta.model_template, "User")

    def test_array_basic_type(self):
        array = types.Array(element_template=types.String(default="default"))

        blueprint = array.blueprint()
        blueprint["map_name"] = "b_a"
        array_meta = AttributeMetaData("user_tags", blueprint)
        self.assertEqual(array_meta.name, "user_tags")
        self.assertEqual(array_meta.map_name, "b_a")
        self.assertEqual(array_meta.cc, "UserTags")
        self.assertEqual(array_meta.ccif, "userTags")
        self.assertEqual(array_meta.blueprint_type, "array")
        self.assertEqual(array_meta.client_class_name, "Array")
        self.assertEqual(array_meta.required, "true")
        self.assertEqual(array_meta.min_length, "null")
        self.assertEqual(array_meta.max_length, "null")
        self.assertFalse(array_meta.element_template_is_model)
        self.assertEqual(array_meta.element_template.blueprint_type, "string")
        self.assertEqual(array_meta.element_template.default, "\"default\"")

    def test_array_model(self):
        class User(types.Model):
            first_name = types.String(required=False)

        array = types.Array(
            min_length=1,
            max_length=10,
            element_template=User()
        )

        blueprint = array.blueprint()
        blueprint["map_name"] = "b_a"
        array_meta = AttributeMetaData("user_records", blueprint)
        self.assertEqual(array_meta.name, "user_records")
        self.assertEqual(array_meta.map_name, "b_a")
        self.assertEqual(array_meta.cc, "UserRecords")
        self.assertEqual(array_meta.ccif, "userRecords")
        self.assertEqual(array_meta.blueprint_type, "array")
        self.assertEqual(array_meta.client_class_name, "Array")
        self.assertEqual(array_meta.required, "true")
        self.assertEqual(array_meta.min_length, 1)
        self.assertEqual(array_meta.max_length, 10)
        self.assertTrue(array_meta.element_template_is_model)
        self.assertEqual(array_meta.element_template, "User")

