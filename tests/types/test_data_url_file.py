import unittest

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
    def test_required(self):
        data_url_file = DataURLFile()
        self.assertEquals(data_url_file.required, True)

        data_url_file = DataURLFile(required=False)
        self.assertEquals(data_url_file.required, False)


class DataURLFileAllowedMimeTypes(unittest.TestCase):

    def test_allowed_mime_types(self):
        data_url_file = DataURLFile()
        self.assertEquals(data_url_file.allowed_mime_types, [])

        data_url_file = DataURLFile(allowed_mime_types=["image/png", "text/plain"])
        self.assertEquals(data_url_file.allowed_mime_types, ["image/png", "text/plain"])


class DataURLFileDescription(unittest.TestCase):

    def test_description(self):
        data_url_file = DataURLFile()
        self.assertEquals(data_url_file.description, None)

        data_url_file = DataURLFile(description="description")
        self.assertEquals(data_url_file.description, "description")


class DataURLFileBlueprint(unittest.TestCase):

    def test_blueprint(self):
        data_url_file = DataURLFile()
        blueprint = data_url_file.blueprint()
        self.assertEquals(blueprint["type"], "data_url_file")
        self.assertEquals(blueprint["constraints"]["required"], True)
        self.assertEquals(blueprint["constraints"]["allowed_mime_types"], [])
        self.assertEquals(blueprint["constraints"]["description"], None)

        data_url_file = DataURLFile(required=False, allowed_mime_types=["image/png"], description="description")
        blueprint = data_url_file.blueprint()
        self.assertEquals(blueprint["type"], "data_url_file")
        self.assertEquals(blueprint["constraints"]["required"], False)
        self.assertEquals(blueprint["constraints"]["allowed_mime_types"], ["image/png"])
        self.assertEquals(blueprint["constraints"]["description"], "description")


class DataURLFileMimeType(unittest.TestCase):

    @unittest.skip
    def test_mime_type(self):
        red_dot = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        data_url_file = DataURLFile()
        data_url_file.validate(red_dot)
        self.assertEquals(data_url_file.mime_type, "image/png")


class DataURLFileFileContents(unittest.TestCase):

    def test_file_contents(self):
        pass


class DataURLFileBase64Contents(unittest.TestCase):

    def test_base64_contents(self):
        pass

class DataURLFileValidate(unittest.TestCase):

    def test_validate(self):
        pass


class DataURLFileSave(unittest.TestCase):

    def test_save(self):
        pass


class DataURLFileAsSerializable(unittest.TestCase):

    def test_as_serializable(self):
        pass