from prestans import types


class MyModel(types.Model):
    name = types.String(required=True)