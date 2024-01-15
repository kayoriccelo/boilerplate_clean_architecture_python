from src.interface._common.validators import (
    BaseValidator, CharValidatorField, ChoiceValidatorField, DateValidatorField
)
from src.infrastructure.orm.django.apps.account.choices import C_GENDER_ACCOUNT


class AccountCreateValidator(BaseValidator):
    first_name = CharValidatorField(label="First Name")
    last_name = CharValidatorField(label="Last Name")
    number_identity = CharValidatorField(label="Number Identity")
    date_birth = DateValidatorField(label="Date Birth")
    gender = ChoiceValidatorField(label='Gender', choices=C_GENDER_ACCOUNT)


class AccountUpdateValidator(BaseValidator):
    first_name = CharValidatorField(label="First Name")
    last_name = CharValidatorField(label="Last Name")
    number_identity = CharValidatorField(label="Number Identity")
    date_birth = DateValidatorField(label="Date Birth")
    gender = ChoiceValidatorField(label='Gender', choices=C_GENDER_ACCOUNT)
