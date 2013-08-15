from prestans import types

class StringSample(types.Model):
	string_required = types.String(required=True)
	string_not_required = types.String(required=False)
	string_default = types.String(default="Hello World")
	string_min_length = types.String(min_length=1)
	string_max_length = types.String(max_length=5)
	string_choices = types.String(choices=["A", "B", "C"])

class IntegerSample(types.Model):
	integer_required = types.Integer(required=True)
	integer_not_required = types.Integer(required=False)
	integer_default = types.Integer(default=6)
	integer_minimum = types.Integer(minimum=1)
	integer_maximum = types.Integer(maximum=5)
	integer_choices = types.Integer(choices=[1, 2, 3])

class FloatSample(types.Model):
	float_required = types.Float(required=True)
	float_not_required = types.Float(required=False)
	float_default = types.Float(default=6.0)
	float_minimum = types.Float(minimum=1.0)
	float_maximum = types.Float(maximum=5.0)
	float_choices = types.Float(choices=[1.1, 2.2, 3.3])

class BooleanSample(types.Model):
	boolean_required = types.Boolean(required=True)
	boolean_not_required = types.Boolean(required=False)
	boolean_default = types.Boolean(default=True)

class DateTime(types.Model):
	datetime_required = types.DateTime(required=True)
	datetime_not_required = types.DateTime(required=False)
	datetime_default_now = types.DateTime(default=types.DateTime.CONSTANT.NOW)
	datetime_default_string = types.DateTime(default="2013-01-01 12:01:34")

class Date(types.Model):
	date_required = types.Date(required=True)
	date_not_required = types.Date(required=False)
	date_default_today = types.Date(default=types.Date.CONSTANT.TODAY)
	date_default_string = types.Date(default="2013-01-02")

class Time(types.Model):
	time_required = types.Date(required=True)
	time_not_required = types.Date(required=False)
	time_default_now = types.Date(default=types.Time.CONSTANT.NOW)

class ModelSample(types.Model):
	integer_sample = IntegerSample()
	string_sample = StringSample()
	string_title = types.String(required=True)

class ArraySample(types.Model):
	model_array = types.Array(element_template=IntegerSample())
	integer_array = types.Array(element_template=types.Integer())
	string_array = types.Array(element_template=types.String())
	string_title = types.String(required=True)
