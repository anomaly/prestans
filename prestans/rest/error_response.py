import sys
import webob

from prestans import exception


class ErrorResponse(webob.Response):
    """
    ErrorResponse is a specialised webob.Response, it is responsible for writing
    out a message in the following format; using the currently selected serializer

      {
          "code": 404,
          "message": "This is an error message",
          "trace": [
            {
                "key": "value"
            }
          ]
      }
    """

    def __init__(self, raised_exception, serializer):

        super(ErrorResponse, self).__init__()

        self._exception = raised_exception
        self._serializer = serializer
        self._message = raised_exception.message
        self._stack_trace = raised_exception.stack_trace
        # self._trace = None

        # IETF hash dropped the X- prefix for custom headers
        # http://stackoverflow.com/q/3561381
        # http://tools.ietf.org/html/draft-saintandre-xdash-00

        from prestans import __version__ as version
        if not isinstance(version, str):
            version = version.encode("latin1")
        self.headers.add('Prestans-Version', version)

        self.content_type = self._serializer.content_type()
        self.status = raised_exception.http_status

    # @property
    # def trace(self):
    #     return self._trace
    #
    # def append_to_trace(self, trace_entry):
    #     """
    #     Use this to append to the stack trace
    #     """
    #     self._trace.append(trace_entry)

    def __call__(self, environ, start_response):

        # we have received a custom error response model, use it instead
        if isinstance(self._exception, exception.ResponseException) and self._exception.response_model:
            body_as_string = self._serializer.dumps(self._exception.response_model.as_serializable())
        # pack into default format for error response
        else:
            error_dict = {
                "code": self.status_int,
                "message": self._message,
                "trace": self._stack_trace
            }

            body_as_string = self._serializer.dumps(error_dict)

        self.content_length = len(body_as_string)

        start_response(self.status, self.headerlist)

        return [body_as_string.encode("utf-8")]
