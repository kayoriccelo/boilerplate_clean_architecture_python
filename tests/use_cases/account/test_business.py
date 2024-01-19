from datetime import datetime

from src.core.exceptions import UseCaseBusinessException
from src.domain.entities.account import Account
from src.infrastructure.orm.django.apps.account.repositories import AccountModelRepository
from src.use_cases.account.business import AccountBusiness

from tests._common.use_case import BaseUseCaseBusinessTest


class TestAccountBusiness(BaseUseCaseBusinessTest):
    entity_class = Account
    repository_class = AccountModelRepository
    business_class = AccountBusiness

    @property
    def data(self):
        return {
            'id': 1,
            'first_name': 'Kayo',
            'last_name': 'Riccelo',
            'number_identity': '12345678910',
            'date_birth': datetime(2000, 1, 1),
            'gender': 1,
            'status': 1
        }

    def test_create(self):
        try:
            self.business.create(instance=self.entity, repository=self.repository)

            assert True

        except UseCaseBusinessException:
            assert False

    def test_update(self):
        try:
            self.entity.first_name = 'Kayo Update'
            self.entity.last_name = 'Riccelo Update'

            self.business.update(instance=self.entity, repository=self.repository)

            assert True

        except UseCaseBusinessException:
            assert False
