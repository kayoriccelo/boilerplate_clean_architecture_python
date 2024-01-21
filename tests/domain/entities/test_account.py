import pytest
from datetime import datetime

from src.domain.entities.account import Account

from tests._common.entity import BaseEntityTest

@pytest.mark.order(10000)
class TestAccountEntity(BaseEntityTest):
    @property
    def data(self):
        return {
            'first_name': 'Kayo',
            'last_name': 'Riccelo',
            'number_identity': '12345678910',
            'date_birth': datetime(2000, 1, 1),
            'gender': 1,
        }

    def test_create(self):
        account = Account(**self.data)

        first_name_valid = account.first_name == 'Kayo'
        last_name_valid = account.last_name == 'Riccelo'
        number_identity_valid = account.number_identity == '12345678910'
        date_birth_valid = account.date_birth == datetime(2000, 1, 1)
        gender_valid = account.gender == 1

        assert (
            first_name_valid and last_name_valid and number_identity_valid and 
            date_birth_valid and gender_valid
        )

    def test_update(self):
        account = Account(**self.data)

        account.first_name = 'Kayo Update'
        account.last_name = 'Riccelo Update'
        account.number_identity = '9999999999'
        account.date_birth = datetime(2020, 1, 1)

        first_name_valid = account.first_name == 'Kayo Update'
        last_name_valid = account.last_name == 'Riccelo Update'
        number_identity_valid = account.number_identity == '9999999999'
        date_birth_valid = account.date_birth == datetime(2020, 1, 1)
        gender_valid = account.gender == 1

        assert (
            first_name_valid and last_name_valid and number_identity_valid and 
            date_birth_valid and gender_valid
        )
