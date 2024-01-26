
from src.domain._common.values_object import ValueObject


class UUIDValue(ValueObject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
    def __set__(self, instance, value=None):
        setattr(instance, self.targe_name, value)
