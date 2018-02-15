import inspect

from prestans import exception
from prestans.types import Array
from prestans.types import DataCollection


class AttributeFilter(object):
    """
      {
        field_name0: true,
        field_name1: false,
        collection_name0: true,
        collection_name1: false,
        collection_name2: {
            sub_field_name0: true,
            sub_field_name1: false
        }
      }
    """

    def __init__(self, from_dictionary=None, template_model=None, is_array_scalar=False, **kwargs):
        """
        Creates an attribute filter object, optionally populates from a
        dictionary of booleans
        """
        # todo: is_array_scalar currently does nothing, fix or remove
        # todo: adding it as property breaks keys and other methods in current implementation

        if from_dictionary:
            self._init_from_dictionary(from_dictionary, template_model)

        for name, value in iter(kwargs.items()):
            if name in self.__dict__:
                setattr(self, name, value)
            else:
                raise KeyError(name)

    @classmethod
    def from_model(cls, model_instance, default_value=False, **kwargs):
        """
        wrapper for Model's get_attribute_filter
        """

        if not isinstance(model_instance, DataCollection):
            raise TypeError("model_instance must be a subclass of \
                prestans.types.DataCollection, %s given" % (model_instance.__class__.__name__))
        elif isinstance(model_instance, Array) and model_instance.is_scalar:
            return AttributeFilter(is_array_scalar=True)
        attribute_filter_instance = model_instance.get_attribute_filter(default_value)

        # kwargs support
        for name, value in iter(kwargs.items()):
            if name in attribute_filter_instance:
                setattr(attribute_filter_instance, name, value)
            else:
                raise KeyError(name)

        return attribute_filter_instance

    def blueprint(self):
        """
        :return: blueprint
        :rtype: dict
        """
        blueprint = dict()
        for key in self.keys():
            blueprint[key] = self.is_attribute_visible(key)

        return blueprint

    def conforms_to_template_filter(self, template_filter):
        """
        Check AttributeFilter conforms to the rules set by the template

         - If self, has attributes that template_filter does not contain, throw Exception
         - If sub list found, perform the first check
         - If self has a value for an attribute, assign to final AttributeFilter
         - If not found, assign value from template

         todo: rename as current name is mis-leading
        """

        if not isinstance(template_filter, self.__class__):
            raise TypeError("AttributeFilter can only check conformance against \
                another template filter, %s provided" % template_filter.__class__.__name__)

        # keys from the template
        template_filter_keys = template_filter.keys()
        # Keys from the object itself
        this_filter_keys = self.keys()

        # 1. Check to see if the client has provided unwanted keys
        unwanted_keys = set(this_filter_keys) - set(template_filter_keys)
        if len(unwanted_keys) > 0:
            raise exception.AttributeFilterDiffers(list(unwanted_keys))

        # 2. Make a attribute_filter that we send back
        evaluated_attribute_filter = AttributeFilter()

        # 3. Evaluate the differences between the two, with template_filter as the standard
        for template_key in template_filter_keys:

            if template_key in this_filter_keys:

                value = getattr(self, template_key)

                # if sub filter and boolean provided with of true, create default filter with value of true
                if isinstance(value, bool) and \
                   value is True and \
                   isinstance(getattr(template_filter, template_key), AttributeFilter):
                    setattr(evaluated_attribute_filter, template_key, getattr(template_filter, template_key))
                elif isinstance(value, bool):
                    setattr(evaluated_attribute_filter, template_key, value)
                elif isinstance(value, self.__class__):
                    # Attribute lists sort themselves out, to produce sub Attribute Filters
                    template_sub_list = getattr(template_filter, template_key)
                    this_sub_list = getattr(self, template_key)
                    setattr(
                        evaluated_attribute_filter, template_key,
                        this_sub_list.conforms_to_template_filter(template_sub_list)
                    )
            else:
                setattr(evaluated_attribute_filter, template_key, getattr(template_filter, template_key))

        return evaluated_attribute_filter

    def keys(self):
        """
        :returns: a list of usable keys
        :rtype: list

        """

        keys = list()

        for attribute_name, type_instance in inspect.getmembers(self):

            # ignore parameters with __ and if they are methods
            if attribute_name.startswith('__') or inspect.ismethod(type_instance):

                continue

            keys.append(attribute_name)

        return keys

    def __contains__(self, key):
        return key in self.__dict__

    def is_filter_at_key(self, key):
        """
        return True if attribute is a sub filter
        """

        if key in self:
            attribute_status = getattr(self, key)
            if isinstance(attribute_status, self.__class__):
                return True

        return False

    def is_attribute_visible(self, key):
        """
        Returns True if an attribute is visible
        If attribute is an instance of AttributeFilter, it returns True if all attributes
        of the sub filter are visible.

        :param key: name of attribute to check
        :type key: str
        :return: whether attribute is visible
        :rtype: bool
        """
        if key in self:
            attribute_status = getattr(self, key)
            if isinstance(attribute_status, bool) and attribute_status is True:
                return True
            elif isinstance(attribute_status, self.__class__) and attribute_status.are_any_attributes_visible():
                return True

        return False

    def are_any_attributes_visible(self):
        """
        checks to see if any attributes are set to true
        """

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if isinstance(type_instance, bool) and type_instance is True:
                return True
            elif isinstance(type_instance, self.__class__) and type_instance.are_all_attributes_visible() is True:
                return True

        return False

    def are_all_attributes_visible(self):
        """
        checks to see if all attributes are set to true
        """

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods
                continue

            if isinstance(type_instance, bool) and type_instance is False:
                return False
            elif isinstance(type_instance, self.__class__) and type_instance.are_all_attributes_visible() is False:
                return False

        return True

    def set_all_attribute_values(self, value):
        """
        sets all the attribute values to the value and propagate to any children
        """

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods
                continue

            if isinstance(type_instance, bool):
                self.__dict__[attribute_name] = value
            elif isinstance(type_instance, self.__class__):
                type_instance.set_all_attribute_values(value)

    def as_dict(self):
        """
        turns attribute filter object into python dictionary
        """

        output_dictionary = dict()

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if isinstance(type_instance, bool):
                output_dictionary[attribute_name] = type_instance
            elif isinstance(type_instance, self.__class__):
                output_dictionary[attribute_name] = type_instance.as_dict()

        return output_dictionary

    def _init_from_dictionary(self, from_dictionary, template_model=None):
        """
        Private helper to init values from a dictionary, wraps children into
        AttributeFilter objects

        :param from_dictionary: dictionary to get attribute names and visibility from
        :type from_dictionary: dict
        :param template_model:
        :type template_model: DataCollection
        """

        if not isinstance(from_dictionary, dict):
            raise TypeError("from_dictionary must be of type dict, %s \
                provided" % from_dictionary.__class__.__name__)

        rewrite_map = None
        if template_model is not None:

            if not isinstance(template_model, DataCollection):
                msg = "template_model should be a prestans model %s provided" % template_model.__class__.__name__
                raise TypeError(msg)

            rewrite_map = template_model.attribute_rewrite_reverse_map()

        for key, value in iter(from_dictionary.items()):

            target_key = key

            # minify support
            if rewrite_map is not None:
                target_key = rewrite_map[key]

            # ensure that the key exists in the template model
            if template_model is not None and target_key not in template_model:

                unwanted_keys = list()
                unwanted_keys.append(target_key)
                raise exception.AttributeFilterDiffers(unwanted_keys)

            # check to see we can work with the value
            if not isinstance(value, (bool, dict)):
                raise TypeError("AttributeFilter input for key %s must be \
                    boolean or dict, %s provided" % (key, value.__class__.__name__))

            # Either keep the value of wrap it up with AttributeFilter
            if isinstance(value, bool):
                setattr(self, target_key, value)
            elif isinstance(value, dict):

                sub_map = None
                if template_model is not None:

                    sub_map = getattr(template_model, target_key)

                    # prestans Array support
                    if isinstance(sub_map, Array):
                        sub_map = sub_map.element_template

                setattr(self, target_key, AttributeFilter(from_dictionary=value, template_model=sub_map))

    def __setattr__(self, key, value):
        """
        Overrides setattr to allow only booleans or an AttributeFilter
        """

        # Values should either be boolean or type of self
        if isinstance(value, bool) and key in self.__dict__ and isinstance(self.__dict__[key], self.__class__):
            self.__dict__[key].set_all_attribute_values(value)
            return
        elif isinstance(value, (bool, self.__class__)):
            self.__dict__[key] = value
            return

        raise TypeError("%s name in %s must be of type Boolean or AttributeFilter, given %s" %
                        (key, self.__class__.__name__, value.__class__.__name__))
