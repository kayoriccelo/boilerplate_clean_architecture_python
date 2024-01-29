
from src.core.exceptions import SystemException, UseCaseStateException


class BaseState:
    _exception = True
    _can = True
    _kwargs = {}
    _field_name = 'status'

    def _get_value_in_kwargs(self, name, required=True):
        value = self._kwargs.get(name, None)

        if not value and required:
            raise SystemException(None, f'{name} not found in {type(self).__name__}')
        
        return value

    @property
    def status(self):
        if not hasattr(self, '_status'):
            instance = self._get_value_in_kwargs('instance')

            value = getattr(instance, self._field_name)

            setattr(self, '_status', value)

        return getattr(self, '_status')

    def execute_exception(self):
        self._exception = self._kwargs.get('exception', self._exception)

        if not self._can and self._exception:
            raise UseCaseStateException(None, 'Operation without permission')

    def execute_callback(self, callbacks):
        for callback in callbacks:
            if self._can:
                self._can = callback()

        return self.execute_exception()
