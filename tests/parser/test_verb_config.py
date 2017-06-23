from prestans.parser import VerbConfig
from prestans.types import Array
from prestans.types import Boolean
from prestans.types import Float
from prestans.types import Integer
from prestans.types import String


def test_verb_config_boolean_array():
    boolean_array = Array(element_template=Boolean())
    VerbConfig(response_template=boolean_array)


def test_verb_config_float_array():
    float_array = Array(element_template=Float())
    VerbConfig(response_template=float_array)


def test_verb_config_integer_array():
    integer_array = Array(element_template=Integer())
    VerbConfig(response_template=integer_array)


def test_verb_config_string_array():
    string_array = Array(element_template=String())
    VerbConfig(response_template=string_array)