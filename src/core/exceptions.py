
class SystemException(Exception):
    def __init__(self, error, message):
        self.error = error
        self.message = message


class ValueObjectException(SystemException): pass


class EntityException(SystemException): pass


class UseCaseRuleException(SystemException): pass


class UseCaseStateException(SystemException): pass


class UseCaseBusinessException(SystemException): pass


class ValidatorException(SystemException):
    def __init__(self, error, message, errors=[]):
        super().__init__(error, message)

        self.errors = errors


class RepositoryException(SystemException): pass


class ViewsetException(SystemException): pass
