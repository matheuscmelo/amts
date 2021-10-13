from exceptions import MissingAttribute
from flask import request


class verify_attributes(object):

    def __init__(self, attributes):
        self.attributes = attributes

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request_json = request.get_json()
            for attr in self.attributes:
                if attr not in request_json:
                    raise MissingAttribute(f"Missing attribute: {attr}")
            return f(*args, **kwargs)

        return wrapper
