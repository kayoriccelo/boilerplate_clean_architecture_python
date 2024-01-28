
import pytest
from datetime import datetime

from src.domain.entities.account import Account

from tests._mock.repositories.account import AccountRepositoryMock


@pytest.fixture(scope="session")
def account_data():
    return {
        'id': 1,
        'first_name': 'Kayo',
        'last_name': 'Riccelo',
        'number_identity': '12345678910',
        'date_birth': datetime(2000, 1, 1).date(),
        'gender': 1,
    }


@pytest.fixture(scope="session")
def account_entity(account_data):
    return Account(**account_data)


@pytest.fixture(scope="session")
def account_repository(account_entity):
    return AccountRepositoryMock(account_entity)
