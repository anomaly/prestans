import webob

from prestans import exception
from prestans.http import STATUS
from prestans.parser import AttributeFilter
from prestans import serializer
from prestans.types import Array
from prestans.types import BinaryResponse
from prestans.types import DataCollection
from prestans.types import Model


class Response(webob.Response):
    """
    Response is the writable HTTP response. It inherits and leverages
    from webob.Response to do the heavy lifting of HTTP Responses. It adds to
    webob.Response prestans customisations.

    Overrides content_type property to use prestans' serializers with the set body
    """

    def __init__(self, charset, logger, serializers, default_serializer):

        super(Response, self).__init__()

        self._logger = logger
        self._serializers = serializers
        self._default_serializer = default_serializer
        self._selected_serializer = None
        self._template = None
        self._app_iter = []
        self._minify = False
        self._attribute_filter = None
        self._template = None
        self._charset = charset

        #:
        #: IETF hash dropped the X- prefix for custom headers
        #: http://stackoverflow.com/q/3561381
        #: http://tools.ietf.org/html/draft-saintandre-xdash-00
        #:
        from prestans import __version__ as version
        if not isinstance(version, str):
            version = version.encode("latin1")

        self.headers.add('Prestans-Version', version)

    @property
    def minify(self):
        return self._minify

    @minify.setter
    def minify(self, value):
        self._minify = value

    @property
    def logger(self):
        return self._logger

    @property
    def supported_mime_types(self):
        return [serializer.content_type() for serializer in self._serializers]

    @property
    def supported_mime_types_str(self):
        return ''.join(str(mime_type) + ',' for mime_type in self.supported_mime_types)[:-1]

    @property
    def selected_serializer(self):
        return self._selected_serializer

    @property
    def default_serializer(self):
        return self._default_serializer

    def _set_serializer_by_mime_type(self, mime_type):
        """
        :param mime_type:
        :return:

        used by content_type_set to set get a reference to the appropriate serializer
        """

        # ignore if binary response
        if isinstance(self._app_iter, BinaryResponse):
            self.logger.info("ignoring setting serializer for binary response")
            return

        for available_serializer in self._serializers:
            if available_serializer.content_type() == mime_type:
                self._selected_serializer = available_serializer
                self.logger.info("set serializer for mime type: %s" % mime_type)
                return

        self.logger.info("could not find serializer for mime type: %s" % mime_type)
        raise exception.UnsupportedVocabularyError(mime_type, self.supported_mime_types_str)

    @property
    def template(self):
        """
        is an instance of prestans.types.DataType; mostly a subclass of prestans.types.Model
        """
        return self._template

    @template.setter
    def template(self, value):

        if value is not None and (not isinstance(value, DataCollection) and
                                  not isinstance(value, BinaryResponse)):
            raise TypeError("template in response must be of type prestans.types.DataCollection or subclass")

        self._template = value

    #:
    #: Attribute filter setup
    #:

    @property
    def attribute_filter(self):
        return self._attribute_filter

    @attribute_filter.setter
    def attribute_filter(self, value):

        if value is not None and not isinstance(value, AttributeFilter):
            msg = "attribute_filter in response must be of type prestans.types.AttributeFilter"
            raise TypeError(msg)

        self._attribute_filter = value

    def _content_type__get(self):
        """
        Get/set the Content-Type header (or None), *without* the
        charset or any parameters.

        If you include parameters (or ``;`` at all) when setting the
        content_type, any existing parameters will be deleted;
        otherwise they will be preserved.
        """
        header = self.headers.get('Content-Type')
        if not header:
            return None
        return header.split(';', 1)[0]

    def _content_type__set(self, value):

        # skip for responses that have no body
        if self.status_code in [STATUS.NO_CONTENT, STATUS.PERMANENT_REDIRECT, STATUS.TEMPORARY_REDIRECT]:
            self.logger.info("attempt to set Content-Type to %s being ignored due to empty response" % value)
            self._content_type__del()
        else:
            self._set_serializer_by_mime_type(value)

            if ';' not in value:
                header = self.headers.get('Content-Type', '')
                if ';' in header:
                    params = header.split(';', 1)[1]
                    value += ';' + params
            self.headers['Content-Type'] = value

            self.logger.info("Content-Type set to: %s" % value)

    def _content_type__del(self):
        self.headers.pop('Content-Type', None)

    # content_type; overrides webob.Response line 606
    content_type = property(
        _content_type__get,
        _content_type__set,
        _content_type__del,
        doc=_content_type__get.__doc__
    )

    # body; overrides webob.Response line 324
    @property
    def body(self):
        """
        Overridden response does not support md5, text or json properties. _app_iter
        is set using rules defined by prestans.

        body getter will return the validated prestans model.

        webob does the heavy lifting with headers.
        """

        #: If template is null; return an empty iterable
        if self.template is None:
            return []

        return self._app_iter

    @body.setter
    def body(self, value):

        #: If not response template; we have to assume its NO_CONTENT
        #: hence do not allow setting the body
        if self.template is None:
            raise AssertionError("response_template is None; handler can't return a response")

        #: value should be a subclass prestans.types.DataCollection
        if not isinstance(value, DataCollection) and \
                not isinstance(value, BinaryResponse):
            msg = "%s is not a prestans.types.DataCollection or prestans.types.BinaryResponse subclass" % (
                value.__class__.__name__
            )
            raise TypeError(msg)

        #: Ensure that it matches the return type template
        if not value.__class__ == self.template.__class__:
            msg = "body must of be type %s, given %s" % (
                self.template.__class__.__name__,
                value.__class__.__name__
            )
            raise TypeError(msg)

        #: If it's an array then ensure that element_template matches up
        if isinstance(self.template, Array) and \
           not isinstance(value.element_template, self.template.element_template.__class__):
            msg = "array elements must of be type %s, given %s" % (
                self.template.element_template.__class__.__name__,
                value.element_template.__class__.__name__
            )
            raise TypeError(msg)

        #: _app_iter assigned to value
        #: we need to serialize the contents before we know the length
        #: deffer the content_length property to be set by getter
        self._app_iter = value

    # body = property(_body__get, _body__set, _body__set)

    def register_serializers(self, serializers):
        """
        Adds extra serializers; generally registered during the handler lifecycle
        """
        for new_serializer in serializers:

            if not isinstance(new_serializer, serializer.Base):
                msg = "registered serializer %s.%s does not inherit from prestans.serializer.Serializer" % (
                    new_serializer.__module__,
                    new_serializer.__class__.__name__
                )
                raise TypeError(msg)

        self._serializers = self._serializers + serializers

    def __call__(self, environ, start_response):
        """
        Overridden WSGI application interface
        """

        # prestans equivalent of webob.Response line 1022
        if self.template is None or self.status_code == STATUS.NO_CONTENT:

            self.content_type = None

            start_response(self.status, self.headerlist)

            if self.template is not None:
                self.logger.warn("handler returns No Content but has a response_template; set template to None")

            return []

        # ensure what we are able to serialize is serializable
        if not isinstance(self._app_iter, DataCollection) and \
           not isinstance(self._app_iter, BinaryResponse):

            if isinstance(self._app_iter, list):
                app_iter_type = "list"
            else:
                app_iter_type = self._app_iter.__name__

            msg = "handler returns content of type %s; not a prestans.types.DataCollection subclass" % (
                app_iter_type
            )
            raise TypeError(msg)

        if isinstance(self._app_iter, DataCollection):

            #: See if attribute filter is completely invisible
            if self.attribute_filter is not None:

                #: Warning to say nothing is visible
                if not self.attribute_filter.are_any_attributes_visible():
                    self.logger.warn("attribute_filter has all the attributes turned \
                        off, handler will return an empty response")

                #: Warning to say none of the fields match
                model_attribute_filter = None
                if isinstance(self._app_iter, Array):
                    model_attribute_filter = AttributeFilter. \
                        from_model(self._app_iter.element_template)
                elif isinstance(self._app_iter, Model):
                    model_attribute_filter = AttributeFilter. \
                        from_model(self._app_iter)

                if model_attribute_filter is not None:
                    try:
                        model_attribute_filter.conforms_to_template_filter(self.attribute_filter)
                    except exception.AttributeFilterDiffers as exp:
                        exp.request = self.request
                        self.logger.warn("%s" % exp)

            # body should be of type DataCollection try; attempt calling
            # as_serializable with available attribute_filter
            serializable_body = self._app_iter.as_serializable(self.attribute_filter, self.minify)

            #: attempt serializing via registered serializer
            stringified_body = self._selected_serializer.dumps(serializable_body)

            # if not isinstance(stringified_body, str):
            #     msg = "%s dumps must return a python str not %s" % (
            #         self._selected_serializer.__class__.__name__,
            #         stringified_body.__class__.__name__
            #     )
            #     raise TypeError(msg)

            #: set content_length
            self.content_length = len(stringified_body)

            start_response(self.status, self.headerlist)

            return [stringified_body.encode("utf-8")]

        elif isinstance(self._app_iter, BinaryResponse):

            if self._app_iter.content_length == 0 or \
                    self._app_iter.mime_type is None or \
                    self._app_iter.file_name is None:
                msg = "Failed to write binary response with content_length %i; mime_type %s; file_name %s" % (
                    self._app_iter.content_length,
                    self._app_iter.mime_type,
                    self._app_iter.file_name
                )
                self.logger.warn(msg)
                self.status = STATUS.INTERNAL_SERVER_ERROR
                self.content_type = "text/plain"
                return []

            # set the content type
            self.content_type = self._app_iter.mime_type

            #: Add content disposition header
            if self._app_iter.as_attachment:
                attachment = "attachment; filename=\"%s\"" % self._app_iter.file_name
                if not isinstance(attachment, str):
                    attachment = attachment.encode("latin1")

                self.headers.add("Content-Disposition", attachment)
            else:
                inline = "inline; filename=\"%s\"" % self._app_iter.file_name
                if not isinstance(inline, str):
                    inline = inline.encode("latin1")

                self.headers.add("Content-Disposition", inline)

            #: Write out response
            self.content_length = self._app_iter.content_length

            start_response(self.status, self.headerlist)
            return [self._app_iter.contents]

        else:
            raise AssertionError("prestans failed to write a binary or textual response")

    def __str__(self):
        #: Overridden so webob's __str__ skips serializing the body
        super(Response, self).__str__(skip_body=True)