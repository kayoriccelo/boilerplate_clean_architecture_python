
class BaseRules:
    _exception = True
    _can = True
    _kwargs = {}

    def execute_callback(self, callback):
        if not self._can:
            self._can = callback()
