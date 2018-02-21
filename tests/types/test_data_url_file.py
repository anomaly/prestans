from mock import patch
import sys
import unittest

from prestans import exception
from prestans.types import DataURLFile


class DataURLFileGenerateFilename(unittest.TestCase):

    def test_correct_length_and_type(self):
        filename = DataURLFile.generate_filename()
        self.assertIsInstance(filename, str)
        self.assertEquals(len(filename), 32)

    def test_different_each_time(self):
        filename_a = DataURLFile.generate_filename()
        filename_b = DataURLFile.generate_filename()
        filename_c = DataURLFile.generate_filename()

        self.assertNotEquals(filename_a, filename_b)
        self.assertNotEquals(filename_a, filename_c)
        self.assertNotEquals(filename_b, filename_c)


class DataURLFileRequired(unittest.TestCase):

    def test_default_true(self):
        data_url_file = DataURLFile()
        self.assertEquals(data_url_file.required, True)

    def test_custom_false(self):
        data_url_file = DataURLFile(required=False)
        self.assertEquals(data_url_file.required, False)

    def test_custom_true(self):
        data_url_file = DataURLFile(required=True)
        self.assertEquals(data_url_file.required, True)


class DataURLFileAllowedMimeTypes(unittest.TestCase):

    def test_default_empty_array(self):
        data_url_file = DataURLFile()
        self.assertEquals(data_url_file.allowed_mime_types, [])

    def test_set_array(self):
        data_url_file = DataURLFile(allowed_mime_types=["image/png", "text/plain"])
        self.assertEquals(data_url_file.allowed_mime_types, ["image/png", "text/plain"])

    def test_set_single(self):
        data_url_file = DataURLFile(allowed_mime_types="image/png")
        self.assertEquals(data_url_file.allowed_mime_types, ["image/png"])


class DataURLFileDescription(unittest.TestCase):

    def test_default(self):
        data_url_file = DataURLFile()
        self.assertEquals(data_url_file.description, None)

    def test_custom(self):
        data_url_file = DataURLFile(description="description")
        self.assertEquals(data_url_file.description, "description")


class DataURLFileBlueprint(unittest.TestCase):

    def test_default(self):
        data_url_file = DataURLFile()
        blueprint = data_url_file.blueprint()
        self.assertEquals(blueprint["type"], "data_url_file")
        self.assertEquals(blueprint["constraints"]["required"], True)
        self.assertEquals(blueprint["constraints"]["allowed_mime_types"], [])
        self.assertEquals(blueprint["constraints"]["description"], None)

    def test_custom(self):
        data_url_file = DataURLFile(required=False, allowed_mime_types=["image/png"], description="description")
        blueprint = data_url_file.blueprint()
        self.assertEquals(blueprint["type"], "data_url_file")
        self.assertEquals(blueprint["constraints"]["required"], False)
        self.assertEquals(blueprint["constraints"]["allowed_mime_types"], ["image/png"])
        self.assertEquals(blueprint["constraints"]["description"], "description")


class DataURLFileMimeType(unittest.TestCase):

    def test_mime_type_correctly_parsed(self):
        red_dot = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        data_url_file = DataURLFile()
        validated = data_url_file.validate(red_dot)
        self.assertEquals(validated.mime_type, "image/png")


class DataURLFileFileContents(unittest.TestCase):

    def test_file_contents_correctly_parsed(self):
        red_dot = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        data_url_file = DataURLFile()
        validated = data_url_file.validate(red_dot)
        self.assertEquals(validated.file_contents, b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x05\x00\x00\x00\x05\x08\x06\x00\x00\x00\x8do&\xe5\x00\x00\x00\x1cIDAT\x08\xd7c\xf8\xff\xff?\xc3\x7f\x06 \x05\xc3 \x12\x84\xd01\xf1\x82X\xcd\x04\x00\x0e\xf55\xcb\xd1\x8e\x0e\x1f\x00\x00\x00\x00IEND\xaeB`\x82')


class DataURLFileBase64Contents(unittest.TestCase):

    def test_base64_contents_correctly_parsed(self):
        red_dot = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        data_url_file = DataURLFile()
        validated = data_url_file.validate(red_dot)
        self.maxDiff = None
        self.assertEquals(validated.base64_contents, b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==')


class DataURLFileValidate(unittest.TestCase):

    def test_required_true_raises_exception_when_given_none(self):
        self.assertRaises(exception.RequiredAttributeError, DataURLFile(required=True).validate, None)

    def test_required_false_returns_none_when_given_none(self):
        self.assertEquals(DataURLFile(required=False).validate(None), None)

    def test_bad_type_raises_exception(self):
        self.assertRaises(exception.ParseFailedError, DataURLFile().validate, 1234)

    def test_invalid_mime_type_raises_exception(self):
        red_dot = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        self.assertRaises(exception.InvalidChoiceError, DataURLFile(allowed_mime_types="image/jpeg").validate, red_dot)


class DataURLFileSave(unittest.TestCase):

    def test_calls_open_with_correct_args(self):
        red_dot = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        from mock import mock_open

        validated = DataURLFile().validate(red_dot)

        open_path = "__builtin__.open" if sys.version_info < (3,) else "builtins.open"

        with patch(open_path, mock_open()) as mock_file:

            validated.save("path/file.png")
            mock_file.assert_called_once_with("path/file.png", "wb")

            handle = mock_file()
            handle.write.assert_called_once_with(validated._file_contents)
            handle.close.assert_called_once()


class DataURLFileAsSerializable(unittest.TestCase):

    def test_as_serializable(self):
        red_dot = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        data_url_file = DataURLFile()
        validated = data_url_file.validate(red_dot)

        serialized = data_url_file.as_serializable(validated)

        self.maxDiff = None
        self.assertEquals(serialized, red_dot)
