from typing import get_type_hints
from functools import wraps
from inspect import getfullargspec

def validate_input(obj, **kwargs):
    hints = get_type_hints(obj)

    # iterate all type hints
    for attr_name, attr_type in hints.items():
        if attr_name == 'return':
            continue

        if not isinstance(kwargs[attr_name], attr_type):
            raise TypeError(
                'Argument %r is not of type %s' % (attr_name, attr_type)
            )

def type_check(decorator):
    @wraps(decorator)
    def wrapped_decorator(*args, **kwargs):
        # translate *args into **kwargs
        func_args = getfullargspec(decorator)[0]
        kwargs.update(dict(zip(func_args, args)))

        validate_input(decorator, **kwargs)
        return decorator(**kwargs)

    return wrapped_decorator
