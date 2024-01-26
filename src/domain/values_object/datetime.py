
from datetime import datetime

from src.core.exceptions import ValueObjectExcepiton
from src.domain._common.values_object import ValueObject


class DateTimeValue(ValueObject):
    auto_add = False

    def __init__(self, **kwargs) -> None:
        self.auto_add = kwargs.get('auto_add', self.auto_add)

        super().__init__(**kwargs)

    def __set__(self, instance, value=None):
        if self.auto_add:
            if hasattr(instance, self.targe_name):
                value = getattr(instance, self.targe_name)
                
                if not value:
                    setattr(instance, self.targe_name, datetime.now())

        else:
            if type(value) == str:
                try:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M")

                except Exception:
                    try:
                        value = datetime.strptime(value, "%Y-%m-%d")
                        
                    except Exception:
                        raise ValueObjectExcepiton('format invalid')
                
        setattr(instance, self.targe_name, value)
