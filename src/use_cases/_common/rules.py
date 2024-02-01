
from typing import Any, Callable

from src.core.exceptions.messages import NOT_FOUND_IN_MESSAGE_EXCEPTION
from src.core.exceptions.types import SystemException, UseCaseRuleException


class BaseRules:
    """Base class for rules."""

    _exception: bool = True
    _can: bool = True
    _kwargs: dict = {}

    def _get_value_in_kwargs(self, name: str, required: bool = True) -> Any:
        """
        Get a value from the keyword arguments.

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

        Args:
            message (str): The message of the exception.

        Raises:
            UseCaseRuleException: If the exception is enabled.
        """

        if self._exception:
            raise UseCaseRuleException("", message)

        return self.can

    def execute_callback(self, callback: Callable[[], bool]) -> None:
        """
        Execute a callback.

        Args:
            callback (Callable[[], bool]): The callback to execute.

        Raises:
            SystemException: If the callback returns False and the can flag is False.
        """

        if not self._can:
            self._can = callback()

        else:
            callback()
