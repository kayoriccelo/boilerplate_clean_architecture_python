
from src.core.exceptions.messages import (
    CHANGE_STATUS_NOT_ALLOWED_MESSAGE_EXCEPTION, NOT_FOUND_IN_MESSAGE_EXCEPTION, OPERATION_WITHOUT_PERMISSION_MESSAGE_EXCEPTION
)
from src.core.exceptions.types import SystemException, UseCaseStateException


class BaseState:
    _exception: bool = True
    _can: bool = True
    _kwargs: dict = {}
    _field_name: str = 'status'
    _status_permission: list = []
    _instance: object = None

    def __init__(self, instance) -> None:
        self._instance = instance

    def _get_value_in_kwargs(self, name: str, required: bool = True) -> any:
        value = self._kwargs.get(name, None)

        if not value and required:
            raise SystemException(None, NOT_FOUND_IN_MESSAGE_EXCEPTION % (name, type(self).__name__))

        return value

    def execute_exception(self) -> bool:
        self._exception = self._kwargs.get('exception', self._exception)

        if not self._can and self._exception:
            raise UseCaseStateException(None, OPERATION_WITHOUT_PERMISSION_MESSAGE_EXCEPTION)

        return self._can
    
    def set_status(self, status):
        if not status in self._status_permission:
            raise UseCaseStateException(None, CHANGE_STATUS_NOT_ALLOWED_MESSAGE_EXCEPTION)

        setattr(self._instance, self._field_name, status)
        self._instance.save()
