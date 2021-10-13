from abc import ABCMeta, abstractmethod

class AppBaseException(Exception):
    __metaclass__ = ABCMeta

    def __init__(self, message):
        self.message = message

    @property
    @abstractmethod
    def status_code(self):
        pass


class NotFound(AppBaseException):
    status_code = 404


class BadRequest(AppBaseException):
    status_code = 400


class MissingAttribute(BadRequest):
    pass


class Unauthorized(AppBaseException):
    status_code = 401
