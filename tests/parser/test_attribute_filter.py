from prestans.parser import AttributeFilter
from prestans.types import Array
from prestans.types import Boolean
from prestans.types import Float
from prestans.types import Integer
from prestans.types import String


def test_from_model_boolean_array():
    boolean_array = Array(element_template=Boolean())
    AttributeFilter.from_model(model_instance=boolean_array, default_value=True)


def test_from_model_float_array():
    float_array = Array(element_template=Float())
    AttributeFilter.from_model(model_instance=float_array, default_value=True)


def test_from_model_integer_array():
    integer_array = Array(element_template=Integer())
    AttributeFilter.from_model(model_instance=integer_array, default_value=True)


def test_from_model_string_array():
    string_array = Array(element_template=String())
    AttributeFilter.from_model(model_instance=string_array, default_value=True)
