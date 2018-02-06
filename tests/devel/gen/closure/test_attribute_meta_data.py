import unittest

from prestans.devel.gen.closure import AttributeMetaData
from prestans import types


class AttributeMetaDataTest(unittest.TestCase):

    def test_string_default(self):
        string_type = types.String()

        blueprint = string_type.blueprint()
        blueprint["map_name"] = "a_b"
        string_meta = AttributeMetaData("first_name", blueprint)
        self.assertEquals(string_meta.name, "first_name")
        self.assertEquals(string_meta.map_name, "a_b")
        self.assertEquals(string_meta.cc, "FirstName")
        self.assertEquals(string_meta.ccif, "firstName")
        self.assertEquals(string_meta.blueprint_type, "string")
        self.assertEquals(string_meta.client_class_name, "String")
        self.assertEquals(string_meta.required, "true")
        self.assertEquals(string_meta.trim, "true")
        self.assertEquals(string_meta.default, "null")
        self.assertEquals(string_meta.format, "null")
        self.assertEquals(string_meta.choices, "null")
        self.assertEquals(string_meta.min_length, "null")
        self.assertEquals(string_meta.max_length, "null")

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
        self.assertEquals(string_meta.name, "first_name")
        self.assertEquals(string_meta.map_name, "a_b")
        self.assertEquals(string_meta.cc, "FirstName")
        self.assertEquals(string_meta.ccif, "firstName")
        self.assertEquals(string_meta.blueprint_type, "string")
        self.assertEquals(string_meta.client_class_name, "String")
        self.assertEquals(string_meta.required, "false")
        self.assertEquals(string_meta.trim, "false")
        self.assertEquals(string_meta.default, "\"default\"")
        self.assertEquals(string_meta.format, "\"[a-z]{2,8}\"")
        self.assertEquals(string_meta.choices, ["a", "b", "c"])
        self.assertEquals(string_meta.min_length, 2)
        self.assertEquals(string_meta.max_length, 8)

    def test_integer_default(self):
        integer_type = types.Integer()

        blueprint = integer_type.blueprint()
        blueprint["map_name"] = "a_b"
        integer_meta = AttributeMetaData("max_size", blueprint)
        self.assertEquals(integer_meta.name, "max_size")
        self.assertEquals(integer_meta.map_name, "a_b")
        self.assertEquals(integer_meta.cc, "MaxSize")
        self.assertEquals(integer_meta.ccif, "maxSize")
        self.assertEquals(integer_meta.blueprint_type, "integer")
        self.assertEquals(integer_meta.client_class_name, "Integer")
        self.assertEquals(integer_meta.required, "true")
        self.assertEquals(integer_meta.default, "null")
        self.assertEquals(integer_meta.choices, "null")
        self.assertEquals(integer_meta.minimum, "null")
        self.assertEquals(integer_meta.maximum, "null")

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
        self.assertEquals(integer_meta.name, "max_size")
        self.assertEquals(integer_meta.map_name, "a_b")
        self.assertEquals(integer_meta.cc, "MaxSize")
        self.assertEquals(integer_meta.ccif, "maxSize")
        self.assertEquals(integer_meta.blueprint_type, "integer")
        self.assertEquals(integer_meta.client_class_name, "Integer")
        self.assertEquals(integer_meta.required, "false")
        self.assertEquals(integer_meta.default, 3)
        self.assertEquals(integer_meta.choices, [1, 3, 5])
        self.assertEquals(integer_meta.minimum, 1)
        self.assertEquals(integer_meta.maximum, 5)

    def test_float_default(self):
        float_type = types.Float()

        blueprint = float_type.blueprint()
        blueprint["map_name"] = "a_b"
        float_meta = AttributeMetaData("max_size", blueprint)
        self.assertEquals(float_meta.name, "max_size")
        self.assertEquals(float_meta.map_name, "a_b")
        self.assertEquals(float_meta.cc, "MaxSize")
        self.assertEquals(float_meta.ccif, "maxSize")
        self.assertEquals(float_meta.blueprint_type, "float")
        self.assertEquals(float_meta.client_class_name, "Float")
        self.assertEquals(float_meta.required, "true")
        self.assertEquals(float_meta.default, "null")
        self.assertEquals(float_meta.choices, "null")
        self.assertEquals(float_meta.minimum, "null")
        self.assertEquals(float_meta.maximum, "null")

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
        self.assertEquals(float_meta.name, "max_size")
        self.assertEquals(float_meta.map_name, "a_b")
        self.assertEquals(float_meta.cc, "MaxSize")
        self.assertEquals(float_meta.ccif, "maxSize")
        self.assertEquals(float_meta.blueprint_type, "float")
        self.assertEquals(float_meta.client_class_name, "Float")
        self.assertEquals(float_meta.required, "false")
        self.assertEquals(float_meta.default, 3.3)
        self.assertEquals(float_meta.choices, [1.1, 3.3, 5.5])
        self.assertEquals(float_meta.minimum, 1.1)
        self.assertEquals(float_meta.maximum, 5.5)

    def test_boolean_default(self):
        boolean_type = types.Boolean()

        blueprint = boolean_type.blueprint()
        blueprint["map_name"] = "a_b"
        boolean_meta = AttributeMetaData("is_admin", blueprint)
        self.assertEquals(boolean_meta.name, "is_admin")
        self.assertEquals(boolean_meta.map_name, "a_b")
        self.assertEquals(boolean_meta.cc, "IsAdmin")
        self.assertEquals(boolean_meta.ccif, "isAdmin")
        self.assertEquals(boolean_meta.blueprint_type, "boolean")
        self.assertEquals(boolean_meta.client_class_name, "Boolean")
        self.assertEquals(boolean_meta.required, "true")
        self.assertEquals(boolean_meta.default, "null")

    def test_boolean_given_values(self):
        boolean_type = types.Boolean(
            required=False,
            default=True
        )

        blueprint = boolean_type.blueprint()
        blueprint["map_name"] = "a_b"
        boolean_meta = AttributeMetaData("is_admin", blueprint)
        self.assertEquals(boolean_meta.name, "is_admin")
        self.assertEquals(boolean_meta.map_name, "a_b")
        self.assertEquals(boolean_meta.cc, "IsAdmin")
        self.assertEquals(boolean_meta.ccif, "isAdmin")
        self.assertEquals(boolean_meta.blueprint_type, "boolean")
        self.assertEquals(boolean_meta.client_class_name, "Boolean")
        self.assertEquals(boolean_meta.required, "false")
        self.assertEquals(boolean_meta.default, "true")

        boolean_type = types.Boolean(
            required=False,
            default=False
        )

        blueprint = boolean_type.blueprint()
        blueprint["map_name"] = "a_b"
        boolean_meta = AttributeMetaData("is_admin", blueprint)
        self.assertEquals(boolean_meta.name, "is_admin")
        self.assertEquals(boolean_meta.map_name, "a_b")
        self.assertEquals(boolean_meta.cc, "IsAdmin")
        self.assertEquals(boolean_meta.ccif, "isAdmin")
        self.assertEquals(boolean_meta.blueprint_type, "boolean")
        self.assertEquals(boolean_meta.client_class_name, "Boolean")
        self.assertEquals(boolean_meta.required, "false")
        self.assertEquals(boolean_meta.default, "false")

    def test_datetime_default(self):
        datetime_type = types.DateTime()

        blueprint = datetime_type.blueprint()
        blueprint["map_name"] = "a_b"
        datetime_meta = AttributeMetaData("created_date", blueprint)
        self.assertEquals(datetime_meta.name, "created_date")
        self.assertEquals(datetime_meta.map_name, "a_b")
        self.assertEquals(datetime_meta.cc, "CreatedDate")
        self.assertEquals(datetime_meta.ccif, "createdDate")
        self.assertEquals(datetime_meta.blueprint_type, "datetime")
        self.assertEquals(datetime_meta.client_class_name, "DateTime")
        self.assertEquals(datetime_meta.required, "true")
        self.assertEquals(datetime_meta.default, "null")
        self.assertEquals(datetime_meta.timezone, "false")
        self.assertEquals(datetime_meta.utc, "false")

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
        self.assertEquals(datetime_meta.name, "created_date")
        self.assertEquals(datetime_meta.map_name, "a_b")
        self.assertEquals(datetime_meta.cc, "CreatedDate")
        self.assertEquals(datetime_meta.ccif, "createdDate")
        self.assertEquals(datetime_meta.blueprint_type, "datetime")
        self.assertEquals(datetime_meta.client_class_name, "DateTime")
        self.assertEquals(datetime_meta.required, "false")
        self.assertEquals(datetime_meta.default, "prestans.types.DateTime.NOW")
        self.assertEquals(datetime_meta.timezone, "true")
        self.assertEquals(datetime_meta.utc, "true")

    def test_date_default(self):
        datetime_type = types.Date()

        blueprint = datetime_type.blueprint()
        blueprint["map_name"] = "a_b"
        datetime_meta = AttributeMetaData("created_date", blueprint)
        self.assertEquals(datetime_meta.name, "created_date")
        self.assertEquals(datetime_meta.map_name, "a_b")
        self.assertEquals(datetime_meta.cc, "CreatedDate")
        self.assertEquals(datetime_meta.ccif, "createdDate")
        self.assertEquals(datetime_meta.blueprint_type, "date")
        self.assertEquals(datetime_meta.client_class_name, "Date")
        self.assertEquals(datetime_meta.required, "true")
        self.assertEquals(datetime_meta.default, "null")

    def test_date_given_values(self):
        datetime_type = types.Date(
            required=False,
            default=types.Date.TODAY
        )

        blueprint = datetime_type.blueprint()
        blueprint["map_name"] = "a_b"
        datetime_meta = AttributeMetaData("created_date", blueprint)
        self.assertEquals(datetime_meta.name, "created_date")
        self.assertEquals(datetime_meta.map_name, "a_b")
        self.assertEquals(datetime_meta.cc, "CreatedDate")
        self.assertEquals(datetime_meta.ccif, "createdDate")
        self.assertEquals(datetime_meta.blueprint_type, "date")
        self.assertEquals(datetime_meta.client_class_name, "Date")
        self.assertEquals(datetime_meta.required, "false")
        self.assertEquals(datetime_meta.default, "prestans.types.Date.TODAY")

    def test_time_default(self):
        datetime_type = types.Time()

        blueprint = datetime_type.blueprint()
        blueprint["map_name"] = "a_b"
        datetime_meta = AttributeMetaData("opening_time", blueprint)
        self.assertEquals(datetime_meta.name, "opening_time")
        self.assertEquals(datetime_meta.map_name, "a_b")
        self.assertEquals(datetime_meta.cc, "OpeningTime")
        self.assertEquals(datetime_meta.ccif, "openingTime")
        self.assertEquals(datetime_meta.blueprint_type, "time")
        self.assertEquals(datetime_meta.client_class_name, "Time")
        self.assertEquals(datetime_meta.required, "true")
        self.assertEquals(datetime_meta.default, "null")

    def test_time_given_values(self):
        datetime_type = types.Time(
            required=False,
            default=types.Time.NOW
        )

        blueprint = datetime_type.blueprint()
        blueprint["map_name"] = "a_b"
        datetime_meta = AttributeMetaData("opening_time", blueprint)
        self.assertEquals(datetime_meta.name, "opening_time")
        self.assertEquals(datetime_meta.map_name, "a_b")
        self.assertEquals(datetime_meta.cc, "OpeningTime")
        self.assertEquals(datetime_meta.ccif, "openingTime")
        self.assertEquals(datetime_meta.blueprint_type, "time")
        self.assertEquals(datetime_meta.client_class_name, "Time")
        self.assertEquals(datetime_meta.required, "false")
        self.assertEquals(datetime_meta.default, "prestans.types.Time.NOW")

    def test_data_url_file_default(self):
        data_url_file_type = types.DataURLFile()

        blueprint = data_url_file_type.blueprint()
        blueprint["map_name"] = "b_a"
        data_url_file_meta = AttributeMetaData("file_download", blueprint)
        self.assertEquals(data_url_file_meta.name, "file_download")
        self.assertEquals(data_url_file_meta.map_name, "b_a")
        self.assertEquals(data_url_file_meta.cc, "FileDownload")
        self.assertEquals(data_url_file_meta.ccif, "fileDownload")
        self.assertEquals(data_url_file_meta.blueprint_type, "data_url_file")
        self.assertEquals(data_url_file_meta.client_class_name, "DataURLFile")
        self.assertEquals(data_url_file_meta.required, "true")
        self.assertEquals(data_url_file_meta.allowed_mime_types, [])

    def test_data_url_file_given_values(self):
        data_url_file_type = types.DataURLFile(
            required=False,
            allowed_mime_types=["text/plain"]
        )

        blueprint = data_url_file_type.blueprint()
        blueprint["map_name"] = "b_a"
        data_url_file_meta = AttributeMetaData("file_download", blueprint)
        self.assertEquals(data_url_file_meta.name, "file_download")
        self.assertEquals(data_url_file_meta.map_name, "b_a")
        self.assertEquals(data_url_file_meta.cc, "FileDownload")
        self.assertEquals(data_url_file_meta.ccif, "fileDownload")
        self.assertEquals(data_url_file_meta.blueprint_type, "data_url_file")
        self.assertEquals(data_url_file_meta.client_class_name, "DataURLFile")
        self.assertEquals(data_url_file_meta.required, "false")
        self.assertEquals(data_url_file_meta.allowed_mime_types, ["text/plain"])

    def test_model(self):
        class User(types.Model):
            first_name = types.String()

        blueprint = User().blueprint()
        blueprint["map_name"] = "b_a"
        data_url_file_meta = AttributeMetaData("my_model", blueprint)
        self.assertEquals(data_url_file_meta.name, "my_model")
        self.assertEquals(data_url_file_meta.map_name, "b_a")
        self.assertEquals(data_url_file_meta.cc, "MyModel")
        self.assertEquals(data_url_file_meta.ccif, "myModel")
        self.assertEquals(data_url_file_meta.blueprint_type, "model")
        self.assertEquals(data_url_file_meta.client_class_name, "Model")
        self.assertEquals(data_url_file_meta.required, "true")
        self.assertEquals(data_url_file_meta.model_template, "User")

    def test_array_basic_type(self):
        array = types.Array(element_template=types.String(default="default"))

        blueprint = array.blueprint()
        blueprint["map_name"] = "b_a"
        array_meta = AttributeMetaData("user_tags", blueprint)
        self.assertEquals(array_meta.name, "user_tags")
        self.assertEquals(array_meta.map_name, "b_a")
        self.assertEquals(array_meta.cc, "UserTags")
        self.assertEquals(array_meta.ccif, "userTags")
        self.assertEquals(array_meta.blueprint_type, "array")
        self.assertEquals(array_meta.client_class_name, "Array")
        self.assertEquals(array_meta.required, "true")
        self.assertEquals(array_meta.min_length, "null")
        self.assertEquals(array_meta.max_length, "null")
        self.assertFalse(array_meta.element_template_is_model)
        self.assertEquals(array_meta.element_template.blueprint_type, "string")
        self.assertEquals(array_meta.element_template.default, "\"default\"")

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
        self.assertEquals(array_meta.name, "user_records")
        self.assertEquals(array_meta.map_name, "b_a")
        self.assertEquals(array_meta.cc, "UserRecords")
        self.assertEquals(array_meta.ccif, "userRecords")
        self.assertEquals(array_meta.blueprint_type, "array")
        self.assertEquals(array_meta.client_class_name, "Array")
        self.assertEquals(array_meta.required, "true")
        self.assertEquals(array_meta.min_length, 1)
        self.assertEquals(array_meta.max_length, 10)
        self.assertTrue(array_meta.element_template_is_model)
        self.assertEquals(array_meta.element_template, "User")

