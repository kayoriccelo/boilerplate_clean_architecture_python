
from src.core.exceptions import ValueObjectExcepiton
from src.domain._common.values_object import ValueObject


class CharValue(ValueObject):
    max_length = -1

    def __init__(self, **kwargs) -> None:
        self.max_length = kwargs.get('max_length', self.max_length)

        super().__init__(**kwargs)

    def __set__(self, instance, value=None):
        if type(value) == str:
            if len(value) > self.max_length:
                ValueObjectExcepiton(f'The maximum length is {self.max_length}.')

        else:
            ValueObjectExcepiton('Format invalid.')
            
        setattr(instance, self.targe_name, value)
