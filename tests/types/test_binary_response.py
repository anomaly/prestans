import unittest

from prestans.types import BinaryResponse


class BinaryResponseUnitTest(unittest.TestCase):

    def test_mime_type(self):
        binary_response = BinaryResponse()
        self.assertIsNone(binary_response.mime_type)

        mime_type_a = "text/plain"
        binary_response = BinaryResponse(mime_type=mime_type_a)
        self.assertEquals(binary_response.mime_type, mime_type_a)

        mime_type_b = "image/png"
        binary_response = BinaryResponse()
        self.assertIsNone(binary_response.mime_type)
        binary_response.mime_type = mime_type_b
        self.assertEquals(binary_response.mime_type, mime_type_b)

    def test_file_name(self):
        binary_response = BinaryResponse()
        self.assertIsNone(binary_response.file_name)

        file_name_a = "file.csv"
        binary_response = BinaryResponse(file_name=file_name_a)
        self.assertEquals(binary_response.file_name, file_name_a)

        file_name_b = "file.txt"
        binary_response = BinaryResponse()
        self.assertIsNone(binary_response.file_name)
        binary_response.file_name = file_name_b
        self.assertEquals(binary_response.file_name, file_name_b)

    def test_as_attachment(self):
        binary_response = BinaryResponse()
        self.assertTrue(binary_response.as_attachment)

        binary_response.as_attachment = False
        self.assertFalse(binary_response.as_attachment)

    def test_contents(self):
        binary_response = BinaryResponse()
        self.assertIsNone(binary_response.contents)

        contents = "contents of binary response"
        binary_response.contents = contents
        self.assertEquals(binary_response.contents, contents)

    def test_content_length(self):
        binary_response = BinaryResponse()
        self.assertEquals(binary_response.content_length, 0)

        contents = "contents of binary response"
        binary_response.contents = contents
        self.assertEquals(binary_response.contents, contents)
        self.assertEquals(binary_response.content_length, len(contents))

    def test_validate(self):
        binary_response = BinaryResponse()
        self.assertFalse(binary_response.validate())
