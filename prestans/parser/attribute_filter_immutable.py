

class AttributeFilterImmutable(object):

    def __init__(self, attribute_filter):
        """
        Creates an immutable attribute filter based on a given mutable one.
        """
        self._key_map = dict()
        self._visible_keys = set()

        self._populate_from_filter(attribute_filter)

    def _populate_from_filter(self, attribute_filter):
        for key in attribute_filter.keys():
            if attribute_filter.is_filter_at_key(key):
                self._key_map[key] = AttributeFilterImmutable(getattr(attribute_filter, key))
                if self._key_map[key].are_any_attributes_visible():
                    self._visible_keys.add(key)
            else:
                self._key_map[key] = attribute_filter.is_attribute_visible(key)

                if self._key_map[key] is True:
                    self._visible_keys.add(key)

    def keys(self):
        return sorted(self._key_map.keys())

    def __contains__(self, key):
        return key in self._key_map

    def is_filter_at_key(self, key):
        """
        return True if attribute is a sub filter
        """
        return isinstance(self._key_map[key], self.__class__)

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
        return key in self._visible_keys

    def are_any_attributes_visible(self):
        """
        checks to see if any attributes are set to true
        """
        return len(self._visible_keys) > 0

    def are_all_attributes_visible(self):
        """
        checks to see if all attributes are set to true
        """
        return len(self._key_map) == len(self._visible_keys)

    def as_dict(self):
        """
        turns attribute filter object into python dictionary
        """
        output_dictionary = dict()

        for key, value in iter(self._key_map.items()):
            if isinstance(value, bool):
                output_dictionary[key] = value
            elif isinstance(value, self.__class__):
                output_dictionary[key] = value.as_dict()

        return output_dictionary

    def __getattr__(self, key):

        value = self._key_map.get(key)

        if value is not None:
            return value
        else:
            return super(AttributeFilterImmutable, self).__getattribute__(key)
