
from src.core.exceptions.types import ValueObjectException
from src.core.exceptions.messages import (
    FORMAT_INVALID_MESSAGE_EXCEPTION, MAX_LENGHT_MESSAGE_EXCEPTION
)
from src.domain._common.values_object import ValueObject


class CharValue(ValueObject):
    max_length = -1

    def __init__(self, **kwargs) -> None:
        self.max_length = kwargs.get('max_length', self.max_length)

        super().__init__(**kwargs)

    def __set__(self, instance, value=None):
        if type(value) == str:
            if len(value) > self.max_length:
                ValueObjectException(MAX_LENGHT_MESSAGE_EXCEPTION % self.max_length)

        else:
            ValueObjectException(FORMAT_INVALID_MESSAGE_EXCEPTION)
            
        setattr(instance, self.target_name, value)
