from validators import string, integer, integer_list_item
import sys
import types
import re


valid_names = re.compile(r'^[a-zA-Z0-9]+$')


class BaseAWSObject(object):
    def __init__(self, **kwargs):

        self.propnames = self.props.keys()
        self.title = kwargs['title']

        self.attributes = [
            'Condition', 'CreationPolicy', 'DeletionPolicy', 'DependsOn',
            'Metadata', 'UpdatePolicy', 'UpdateReplacePolicy',
        ]

        print(self.propnames)

        for k, (_, required) in self.props.items():
            v = getattr(type(self), k, None)
            if v is not None and k not in kwargs:
                self.__setattr__(k, v)

        # Now that it is initialized, populate it with the kwargs
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __getattr__(self, name):
        # If pickle loads this object, then __getattr__ will cause
        # an infinite loop when pickle invokes this object to look for
        # __setstate__ before attributes is "loaded" into this object.
        # Therefore, short circuit the rest of this call if attributes
        # is not loaded yet.
        name = self.title
        if "attributes" not in self.__dict__:
            print(self.__dict__)
            raise AttributeError(name)
        try:
            if name in self.attributes:
                return self.resource[name]
            else:
                return self.properties.__getitem__(name)
        except KeyError:
            # Fall back to the name attribute in the object rather than
            # in the properties dict. This is for non-OpenStack backwards
            # compatibility since OpenStack objects use a "name" property.
            if name == 'name':
                return self.__getattribute__('title')
                print(name)
            raise AttributeError(name)


    def __setattr__(self, name, value):
        if name in self.__dict__.keys() \
                or '_BaseAWSObject__initialized' not in self.__dict__:
            return dict.__setattr__(self, name, value)
        elif name in self.propnames:
            # Check the type of the object and compare against what we were
            # expecting.
            expected_type = self.props[name][0]

            # If it's a function, call it...
            if isinstance(expected_type, types.FunctionType):
                try:
                    value = expected_type(value)
                except Exception:
                    sys.stderr.write(
                        "%s: %s.%s function validator '%s' threw "
                        "exception:\n" % (self.__class__,
                                          self.title,
                                          name,
                                          expected_type.__name__))
                    raise
                return self.properties.__setitem__(name, value)



            # If it's a list of types, check against those types...
            elif isinstance(expected_type, list):
                # If we're expecting a list, then make sure it is a list
                if not isinstance(value, list):
                    self._raise_type(name, value, expected_type)

                # Iterate over the list and make sure it matches our
                # type checks (as above accept AWSHelperFn because
                # we can't do the validation ourselves)
                for v in value:
                    if not isinstance(v, tuple(expected_type)):
                        self._raise_type(name, v, expected_type)
                # Validated so assign it
                return self.properties.__setitem__(name, value)

            # Final validity check, compare the type of value against
            # expected_type which should now be either a single type or
            # a tuple of types.
            elif isinstance(value, expected_type):
                return self.properties.__setitem__(name, value)
            else:
                self._raise_type(name, value, expected_type)

    def _raise_type(self, name, value, expected_type):
        raise TypeError('%s: %s.%s is %s, expected %s' % (self.__class__,
                                                          self.title,
                                                          name,
                                                          type(value),
                                                          expected_type))

    def validate_title(self):
        if not valid_names.match(self.title):
            raise ValueError('Name "%s" not alphanumeric' % self.title)
        else:
            print(self.title)

    def validate(self):
        pass

    def no_validation(self):
        self.do_validation = False
        return self

    @classmethod
    def from_dict(cls, title, d):
        return cls._from_dict(title, **d)

    def _validate_props(self):
        for k, (_, required) in self.props.items():
            if required and k not in self.properties:
                rtype = getattr(self, 'resource_type', "<unknown type>")
                title = getattr(self, 'title')
                msg = "Resource %s required in type %s" % (k, rtype)
                if title:
                    msg += " (title: %s)" % title
                raise ValueError(msg)


class AWSProperty(BaseAWSObject):
    """
    Used for CloudFormation Resource Property objects
    http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/
    aws-product-property-reference.html
    """
    dictname = None

    def __init__(self, title=None, **kwargs):
        super(AWSProperty, self).__init__(title, **kwargs)


def encode_to_dict(obj):
    if hasattr(obj, 'to_dict'):
        # Calling encode_to_dict to ensure object is
        # nomalized to a base dictionary all the way down.
        return encode_to_dict(obj.to_dict())
    elif isinstance(obj, (list, tuple)):
        new_lst = []
        for o in list(obj):
            new_lst.append(encode_to_dict(o))
        return new_lst
    elif isinstance(obj, dict):
        props = {}
        for name, prop in obj.items():
            props[name] = encode_to_dict(prop)

        return props
    # This is useful when dealing with external libs using
    # this format. Specifically awacs.
    elif hasattr(obj, 'JSONrepr'):
        return encode_to_dict(obj.JSONrepr())
    return obj