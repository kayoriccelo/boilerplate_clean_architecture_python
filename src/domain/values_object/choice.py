
from src.domain._common.values_object import ValueObject


class ChoiceValue(ValueObject):
    enum = None

    def __init__(self, **kwargs) -> None:
        self.enum = kwargs.get('enum', self.enum)

        super().__init__(**kwargs)

    def __set__(self, instance, value=None):            
        setattr(instance, self.targe_name, value)
