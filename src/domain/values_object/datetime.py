
from datetime import datetime

from src.core.exceptions import ValueObjectException

from src.domain._common.values_object import ValueObject


class DateValue(ValueObject):
    auto_add = False

    def __init__(self, **kwargs) -> None:
        self.auto_add = kwargs.get('auto_add', self.auto_add)

        super().__init__(**kwargs)

    def __set__(self, instance, value=None):
        if self.auto_add:
            if hasattr(instance, self.targe_name):
                value = getattr(instance, self.targe_name)
                
                if not value:
                    setattr(instance, self.targe_name, datetime.now().date())

        else:
            if type(value) == str:
                regex = datetime.strptime

                try:
                    if regex(value, "%Y-%m-%d"):
                        value = datetime.strptime(value, "%Y-%m-%d").date()

                except Exception:
                    raise ValueObjectException('format invalid')
                            
        setattr(instance, self.targe_name, value)


class DateTimeValue(DateValue):
    def __set__(self, instance, value=None):
        if self.auto_add:
            if hasattr(instance, self.targe_name):
                value = getattr(instance, self.targe_name)
                
                if not value:
                    setattr(instance, self.targe_name, datetime.now())

        else:
            if type(value) == str:
                regex = datetime.strptime

                try:
                    if regex(value, "%Y-%m-%dT%H:%M"):
                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M")

                except Exception:
                    raise ValueObjectException('format invalid')
                            
        setattr(instance, self.targe_name, value)
