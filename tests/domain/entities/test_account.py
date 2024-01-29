
from datetime import datetime

from src.domain.entities.account import Account

from tests._common.entity import BaseEntityTest


class TestAccountEntity(BaseEntityTest):
    def test_create(self, account_data):
        account = Account(**account_data)

        first_name_valid = account.first_name == 'Kayo'
        last_name_valid = account.last_name == 'Riccelo'
        number_identity_valid = account.number_identity == '12345678910'
        date_birth_valid = account.date_birth == datetime(2000, 1, 1).date()
        gender_valid = account.gender == 1

        assert (
            first_name_valid and last_name_valid and number_identity_valid and 
            date_birth_valid and gender_valid
        )

    def test_update(self, account_entity):
        account_entity.first_name = 'Kayo Update'
        account_entity.last_name = 'Riccelo Update'
        account_entity.number_identity = '9999999999'
        account_entity.date_birth = datetime(2020, 1, 1).date()

        first_name_valid = account_entity.first_name == 'Kayo Update'
        last_name_valid = account_entity.last_name == 'Riccelo Update'
        number_identity_valid = account_entity.number_identity == '9999999999'
        date_birth_valid = account_entity.date_birth == datetime(2020, 1, 1).date()
        gender_valid = account_entity.gender == 1

        assert (
            first_name_valid and last_name_valid and number_identity_valid and 
            date_birth_valid and gender_valid
        )
