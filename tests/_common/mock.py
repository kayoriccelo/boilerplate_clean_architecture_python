
from src.core.exceptions import RepositoryException


class BaseMock:
    active_exception = False
    exception_message = None
    exception_class = None
    
    def _simulate_exception(self, message: str, err: Exception = None):
        if self.active_exception:
            if not err:
                err = Exception('simulate error repository')

            raise self.exception_class(err, message)


class BaseRepositoryMock(BaseMock):
    exception_class = RepositoryException

    def __init__(self, instance_entity) -> None:
        self.instance_entity = instance_entity
