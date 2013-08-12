import prestans.devel.gen

class AttributeMetaData(object):

    #used for
    def __str__(self):
        return "%s" % (self._name)

    def __init__(self, name, blueprint):
        self._name = name
        self._blueprint = blueprint

        self._type = blueprint['type']
        if self._type == 'string':
            self._required = blueprint['constraints']['required']
        elif self._type == 'integer':
            self._required = blueprint['constraints']['required']
        elif self._type == 'float':
            self._required = blueprint['constraints']['required']
        elif self._type == 'boolean':
            self._required = blueprint['constraints']['required']

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def required(self):
        return self._required

class Model(object):

    def __init__(self, model_file):
        self._model_file = model_file

    def run(self):

        inspector = prestans.devel.gen.Inspector(model_file=self._model_file)
        blueprints = inspector.inspect()

        for model_blueprint in blueprints:

            attributes = list()

            for field_name, field_blueprint in model_blueprint['fields'].iteritems():

                attribute = AttributeMetaData(name=field_name, blueprint=field_blueprint)
                attributes.append(attribute)

            #write out template
            



        return 0

class Filter(object):

    def __init__(self):
        pass