from datetime import datetime

from src.core.exceptions import UseCaseRuleException
from src.infrastructure.orm.django.apps.account.repositories import AccountModelRepository
from src.use_cases.account.rules import AccountRules
from src.domain.entities.account import Account

from tests._common.use_case import BaseUseCaseRuleTest


class TestAccountRules(BaseUseCaseRuleTest):
    entity_class = Account
    repository_class = AccountModelRepository
    rules_class = AccountRules

    @property
    def data(self):
        return {
            'first_name': 'Kayo',
            'last_name': 'Riccelo',
            'number_identity': '12345678910',
            'date_birth': datetime(2000, 1, 1),
            'gender': 1,
        }

    def test_can_create(self):
        try:
            self.rules.can_create(instance=self.entity, repository=self.repository)

            assert True

        except UseCaseRuleException:
            assert False
