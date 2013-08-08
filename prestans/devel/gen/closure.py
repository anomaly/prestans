import prestans.devel.gen

class AttributeMetaData(object):

    #used for
    def __str__(self):
        return "%s" % (self._name)

    def __init__(self, name, blueprint):
        self._name = name
        self._blueprint = blueprint

class Model(object):

    def __init__(self, model_file):
        self._model_file = model_file

    def run(self):

        inspector = prestans.devel.gen.Inspector(model_file=self._model_file)
        blueprints = inspector.inspect()

        attributes = list()
        for model_blueprint in blueprints:

            for field_name, field_blueprint in model_blueprint['fields'].iteritems():

                attribute = AttributeMetaData(name=field_name, blueprint=field_blueprint)
                print attribute

        return 0

class Filter(object):

    def __init__(self):
        pass