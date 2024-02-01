
from typing import Any, Callable

from src.core.exceptions.messages import NOT_FOUND_IN_MESSAGE_EXCEPTION
from src.core.exceptions.types import SystemException, UseCaseRuleException


class BaseRules:
    """
    Base class for rules.

    This class provides methods for managing the state of the rule,
    including exception management and callback execution.
    In addition, it provides a method for getting a value in kwargs.
    """

    _exception: bool = True
    _can: bool = True
    _kwargs: dict = {}

    def _get_value_in_kwargs(self, name: str, required: bool = True) -> Any:
        """
        Get a value from the keyword arguments.

        This method checks if the value is present in kwargs and, if necessary,
        if it has been provided. If the value is not present and is required,
        an error will be generated.

        Args:
            name (str): The name of the argument.
            required (bool, optional): Whether the argument is required. Defaults to True.

        Raises:
            SystemException: If the argument is not found and required is True.

        Returns:
            Any: The value of the argument.
        """

        value = self._kwargs.get(name, None)

        if not value and required:
            raise SystemException(None, NOT_FOUND_IN_MESSAGE_EXCEPTION % (name, type(self).__name__))

        return value

    def execute_exception(self, message: str) -> bool:
        """
        Execute an exception.

        This method checks if exceptions are enabled and, if so,
        executes an exception. Then it returns the rule state.

        Args:
            message (str): The message of the exception.

        Raises:
            UseCaseRuleException: If exceptions are enabled.

        Returns:
            bool: The rule state.
        """

        if self._exception:
            raise UseCaseRuleException("", message)

        return self.can

    def execute_callback(self, callback: Callable[[], bool]) -> None:
        """
        Execute a callback.

        This method checks if the callback returned True and, if not,
        calls the callback. Then it checks if the callback returned False and, if so,
        generates an exception.

        Args:
            callback (Callable[[], bool]): The callback to execute.

        Raises:
            SystemException: If the callback returns False and the rule state is False.
        """
        
        if not self._can:
            self._can = callback()

        else:
            callback()
