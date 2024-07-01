
from datetime import datetime

from src.domain._common.entity import BaseEntity
from src.domain.entities.enums import GenderAccount, StatusAccount
from src.domain.values_object import (
    UUIDValue, DateTimeValue, CharValue, ChoiceValue, DateValue
)


class Account(BaseEntity):
    id = UUIDValue()
    created = DateTimeValue(auto_add=True, default=datetime.now())
    first_name = CharValue(max_length=200)
    last_name = CharValue(max_length=200)
    number_identity = CharValue(max_length=20)
    date_birth = DateValue()
    gender = ChoiceValue(enum=GenderAccount)
    status = ChoiceValue(enum=StatusAccount, default=StatusAccount.ACTIVE.value)
