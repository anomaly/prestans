import unittest

from prestans.types import DataURLFile


class DataURLFileUnitTest(unittest.TestCase):

    def test_generate_filename(self):
        pass

    def test_required(self):
        data_url_file = DataURLFile()
        self.assertEquals(data_url_file.required, True)

        data_url_file = DataURLFile(required=False)
        self.assertEquals(data_url_file.required, False)

    def test_allowed_mime_types(self):
        data_url_file = DataURLFile()
        self.assertEquals(data_url_file.allowed_mime_types, [])

        data_url_file = DataURLFile(allowed_mime_types=["image/png", "text/plain"])
        self.assertEquals(data_url_file.allowed_mime_types, ["image/png", "text/plain"])

    def test_description(self):
        data_url_file = DataURLFile()
        self.assertEquals(data_url_file.description, None)

        data_url_file = DataURLFile(description="description")
        self.assertEquals(data_url_file.description, "description")

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

    @unittest.skip
    def test_mime_type(self):
        red_dot = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        data_url_file = DataURLFile()
        data_url_file.validate(red_dot)
        self.assertEquals(data_url_file.mime_type, "image/png")

    def test_file_contents(self):
        pass

    def test_base64_contents(self):
        pass

    def test_validate(self):
        pass

    def test_save(self):
        pass

    def test_as_serializable(self):
        pass