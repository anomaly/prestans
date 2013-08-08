from prestans import types

class StringSample(types.Model):
	string_required = types.String(required=True)
	string_not_required = types.String(required=False)

class IntegerSample(types.Model):
	integer_sample = types.Integer(required=True)
	integer_not_required = types.Integer(required=False)
