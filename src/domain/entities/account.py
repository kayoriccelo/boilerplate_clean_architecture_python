
from datetime import datetime
from enum import Enum

from src.domain._common.entity import BaseEntity
from src.domain.values_object import UUIDValue, DateTimeValue, CharValue, ChoiceValue


class StatusAccount(Enum):
    ACTIVE = 1
    INACTIVE = 2


class GenderAccount(Enum):
    MALE = 1
    FEMALE = 2


class Account(BaseEntity):
    id = UUIDValue()
    created = DateTimeValue(auto_add=True, default=datetime.now())
    first_name = CharValue(max_length=200)
    last_name = CharValue(max_length=200)
    number_identity = CharValue(max_length=20)
    date_birth = DateTimeValue()
    gender = ChoiceValue(enum=GenderAccount)
    status = ChoiceValue(enum=StatusAccount, default=StatusAccount.ACTIVE.value)
