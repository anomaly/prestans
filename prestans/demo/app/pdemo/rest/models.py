from prestans import types

class StringSample(types.Model):
	string_required = types.String(required=True)
	string_not_required = types.String(required=False)
	string_default = types.String(default="Hello World")
	string_min_length = types.String(min_length=1)
	string_max_length = types.String(max_length=5)
	string_choices = types.String(choices=["A", "B", "C"])

class IntegerSample(types.Model):
	integer_sample = types.Integer(required=True)
	integer_not_required = types.Integer(required=False)

StringSample.integer_sample = IntegerSample()
StringSample.integer_sample_array = types.Array(element_template=IntegerSample())
