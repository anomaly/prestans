from prestans.http import VERB


class Config(object):
    """
    Configuration that's attached to each handler to define rules for each
    HTTP Verb. All HTTP verbs in use must have a configuration defined.

    __init__ takes in a VerbConfig instance for each parameter with names
    adjacent to the HTTP verb.
    """

    def __init__(self, GET=None, HEAD=None, POST=None, PUT=None, PATCH=None, DELETE=None, OPTIONS=None):
        from prestans.parser import VerbConfig

        for verb in [GET, HEAD, POST, PUT, PATCH, DELETE, OPTIONS]:
            if verb is not None and not isinstance(verb, VerbConfig):
                raise TypeError("All Parser configs should be of type prestans.parser.VerbConfig")

        self._configs = dict()

        self._configs[VERB.GET] = GET
        self._configs[VERB.HEAD] = HEAD
        self._configs[VERB.POST] = POST
        self._configs[VERB.PUT] = PUT
        self._configs[VERB.PATCH] = PATCH
        self._configs[VERB.DELETE] = DELETE
        self._configs[VERB.OPTIONS] = OPTIONS

    def get_config_for_verb(self, verb):
        return self._configs[verb]

    @property
    def get(self):
        return self._configs[VERB.GET]

    @property
    def head(self):
        return self._configs[VERB.HEAD]

    @property
    def post(self):
        return self._configs[VERB.POST]

    @property
    def put(self):
        return self._configs[VERB.PUT]

    @property
    def patch(self):
        return self._configs[VERB.PATCH]

    @property
    def delete(self):
        return self._configs[VERB.DELETE]

    @property
    def options(self):
        return self._configs[VERB.OPTIONS]
