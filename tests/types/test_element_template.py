import unittest

from prestans.types import ElementTemplate


class ElementTemplateClassRef(unittest.TestCase):

    def test_constructor_and_property(self):
        class MyClass(object):
            pass

        element_template = ElementTemplate(MyClass)
        self.assertEqual(element_template.class_ref, MyClass)


class ElementTemplateClassInstance(unittest.TestCase):

    def test_constructor_and_property(self):
        class MyClass(object):
            pass

        element_template = ElementTemplate(MyClass)
        self.assertEqual(element_template.class_ref, MyClass)
        self.assertIsNone(element_template._class_instance)
        self.assertTrue(isinstance(element_template.class_instance, MyClass))
        self.assertIsNotNone(element_template._class_instance)
