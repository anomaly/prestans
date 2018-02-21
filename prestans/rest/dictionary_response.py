from prestans.rest import Response


class DictionaryResponse(Response):
    """
    DictionaryResponse serializes dictionaries using the selected_serializer
    """

    @property
    def body(self):
        """
        Overridden response does not support md5, text or json properties. _app_iter
        is set using rules defined by prestans.

        body getter will return the validated prestans model.

        webob does the heavy lifting with headers.
        """
        return self._app_iter

    @body.setter
    def body(self, value):

        # value should be a dict
        if not isinstance(value, dict):
            raise TypeError("%s is not a dictionary" % value.__class__.__name__)

        #: _app_iter assigned to value
        #: we need to serialize the contents before we know the length
        #: deffer the content_length property to be set by getter
        self._app_iter = value

    def __call__(self, environ, start_response):

        if not isinstance(self.body, dict):
            raise TypeError("body is not a dict")

        start_response(self.status, self.headerlist)

        # attempt serializing via registered serializer
        body_as_string = self._selected_serializer.dumps(self.body)

        if not isinstance(body_as_string, str):
            raise TypeError("%s dumps must return a python str not %s" % (
                self._selected_serializer.__class__.__name__,
                body_as_string.__class__.__name__)
            )

        # set content_length
        self.content_length = len(body_as_string)

        return [body_as_string]
