
from src.core.exceptions import UseCaseRuleException


class BaseRules:
    _exception = True
    _can = True
    _kwargs = {}

    def execute_exception(self, message):
        if self._exception:
            raise UseCaseRuleException('', message)

        return True

    def execute_callback(self, callback):
        if not self._can:
            self._can = callback()
            
        else:
            callback()
