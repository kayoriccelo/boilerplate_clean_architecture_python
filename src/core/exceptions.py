class SystemException(Exception):
    def __init__(self, error, message):
        self.error = error
        self.message = message


class ValueObjectExcepiton(SystemException): pass


class EntityException(SystemException): pass


class UseCaseRuleException(SystemException): pass


class UseCaseBusinessException(SystemException): pass


class ControllerException(SystemException): pass


class ValidatorException(SystemException): pass


class PresenterException(SystemException): pass


class RepositoryException(SystemException): pass


class ViewsetException(SystemException): pass
