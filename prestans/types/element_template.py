from prestans.types import DataType
from prestans.types import ScalarType
from prestans.types import DataStructure
from prestans.types import DataCollection

from prestans.types import Boolean
from prestans.types import Float
from prestans.types import Integer
from prestans.types import String

import inspect


class ElementTemplate(object):

    def __init__(self, class_ref, **kwargs):
        self._class_ref = class_ref
        self._class_instance = None
        self._kwargs = kwargs

        if not inspect.isclass(self._class_ref):
            raise TypeError("class_ref must be a class reference" % ElementTemplate.__name__)

        # if issubclass(self._class_ref, DataType):
        #     msg = "element_template must be a DataType subclass; given %s " % element_template.__name__
        #     raise TypeError(msg)
        #
        # self._element_template = element_template
        #
        # # force required to be True if basic type in  use
        # if issubclass(element_template, DataType) and \
        #    not issubclass(element_template, DataCollection) and \
        #    not issubclass(element_template, DataStructure):
        #     element_template._required = True

    @property
    def class_ref(self):
        return self._class_ref

    @property
    def class_instance(self):
        """
        :return:
        :rtype: prestans.types.DataType
        """
        if self._class_instance is None:
            if issubclass(self._class_ref, ScalarType) or issubclass(self.class_ref, DataStructure):
                self._class_instance = self.class_ref(**self._kwargs)
            else:
                self._class_instance = self.class_ref()

        return self._class_instance

    @property
    def is_scalar(self):
        """
        :return:
        :rtype: bool
        """
        return issubclass(self.class_ref, ScalarType)

    @property
    def is_data_structure(self):
        return issubclass(self.class_ref, DataStructure)

    @property
    def blueprint(self):
        return self.class_instance.blueprint()

    def validate(self, value, attribute_filter=None, minified=False):
        """
        :param value:
        :type value: list | None
        :param attribute_filter:
        :type attribute_filter: prestans.parser.AttributeFilter
        :param minified:
        :type minified: bool
        :return:
        """
        if issubclass(self.class_ref, DataCollection):
            validated_value = self.class_instance.validate(value, attribute_filter, minified)
        else:
            validated_value = self.class_instance.validate(value)

        return validated_value

    def as_serializable(self, array_element, attribute_filter=None, minified=False):
        """
        :param array_element:
        :param attribute_filter:
        :param minified:
        :type minified: bool
        :return:
        """
        serialized_value = None

        if issubclass(self._class_ref, DataCollection):
            serialized_value = array_element.as_serializable(attribute_filter, minified)
        elif issubclass(self._class_ref, DataStructure):
            serialized_value = self._class_ref().as_serializable(array_element)
        elif issubclass(self._class_ref, DataType):
            serialized_value = array_element

        return serialized_value

    def attribute_rewrite_map(self):
        if issubclass(self._class_ref, DataCollection):
            return self._class_ref().attribute_rewrite_map()
        else:
            return None

    def attribute_rewrite_reverse_map(self):
        if issubclass(self._class_ref, DataCollection):
            return self._class_ref().attribute_rewrite_reverse_map()
        else:
            return None

    def get_attribute_filter(self, default_value=False):
        attribute_filter = None

        if issubclass(self._class_ref, DataCollection):
            attribute_filter = self._class_ref().get_attribute_filter(default_value)
        elif issubclass(self._class_ref, DataType) or issubclass(self._class_ref, DataStructure):
            attribute_filter = default_value

        return attribute_filter
