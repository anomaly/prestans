import sys

if sys.version_info < (3,):
    integer_types = (int, long)
else:
    integer_types = (int,)


if sys.version_info < (3,):
    string_types = (str, unicode)
else:
    string_types = (str,)
