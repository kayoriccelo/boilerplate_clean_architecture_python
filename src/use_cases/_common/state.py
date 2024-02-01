
from src.core.exceptions.messages import NOT_FOUND_IN_MESSAGE_EXCEPTION, OPERATION_WITHOUT_PERMISSION_MESSAGE_EXCEPTION
from src.core.exceptions.types import SystemException, UseCaseStateException


class BaseState:
    """
    BaseState class is a base class for all states in the application.

    It provides a set of common methods and properties that can be used by all states.

    Attributes:
        _exception (bool): A flag indicating whether to raise an exception if the operation is not allowed.
        _can (bool): A flag indicating whether the operation is allowed.
        _kwargs (dict): A dictionary of keyword arguments.
        _field_name (str): The name of the field that stores the status.
    """

    _exception = True
    _can = True
    _kwargs = {}
    _field_name = 'status'

    def _get_value_in_kwargs(self, name, required=True):
        """
        A helper method to get a value from the keyword arguments.

        Args:
            name (str): The name of the argument.
            required (bool, optional): A flag indicating whether the argument is required. Defaults to True.

        Raises:
            SystemException: If the argument is not found and required is True.

        Returns:
            Any: The value of the argument.
        """
        
        value = self._kwargs.get(name, None)

        if not value and required:
            raise SystemException(None, NOT_FOUND_IN_MESSAGE_EXCEPTION % (name, type(self).__name__))

        return value

    @property
    def status(self):
        """
        A property that returns the status. It will retrieve the value from the instance if it hasn't been set yet.

        Returns:
            Any: The status.
        """

        if not hasattr(self, '_status'):
            instance = self._get_value_in_kwargs('instance')

            value = getattr(instance, self._field_name)

            setattr(self, '_status', value)

        return getattr(self, '_status')

    def execute_exception(self):
        """
        A method that executes the exception logic. It will check the _exception flag and raise an exception if necessary.

        Returns:
            bool: The _can flag.
        """

        self._exception = self._kwargs.get('exception', self._exception)

        if not self._can and self._exception:
            raise UseCaseStateException(None, OPERATION_WITHOUT_PERMISSION_MESSAGE_EXCEPTION)

        return self._can

    def execute_callback(self, callbacks):
        """
        A method that executes the callback logic. It will iterate through the callbacks and check the _can flag.

        Args:
            callbacks (list): A list of callbacks.

        Returns:
            bool: The _can flag.
        """

        for callback in callbacks:
            if self._can:
                self._can = callback()

        return self.execute_exception()
