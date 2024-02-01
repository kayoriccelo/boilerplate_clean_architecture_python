
import pytest

from src.core.exceptions.messages import ALREADY_CREATED_MESSAGE_EXCEPTION, NOT_FOUND_IN_MESSAGE_EXCEPTION
from src.core.exceptions.types import SystemException, UseCaseRuleException
from src.use_cases.account.rules import AccountRules

from tests._common.use_case import BaseUseCaseRuleTest


class TestAccountRules(BaseUseCaseRuleTest):
    rules_class = AccountRules
    
    def test_can_create(self, account_entity, account_repository):
        try:
            self.rules.can_create(instance=account_entity, repository=account_repository)

        except UseCaseRuleException:
            assert False

    def test_can_create_exception_repository(self, account_repository):
        with pytest.raises(SystemException) as info:
            account_repository.active_exception = True

            self.rules.can_create()

        assert info.value.message == NOT_FOUND_IN_MESSAGE_EXCEPTION % ('repository', 'AccountRules')

    def test_can_create_exception_instance(self, account_repository):
        with pytest.raises(SystemException) as info:
            account_repository.active_exception = True

            self.rules.can_create(repository=account_repository)

        assert info.value.message == NOT_FOUND_IN_MESSAGE_EXCEPTION % ('instance', 'AccountRules')

    def test_can_create_exception_account_already_created(self, account_entity, account_repository):
        with pytest.raises(SystemException) as info:
            account_repository.active_exception = True

            self.rules.can_create(instance=account_entity, repository=account_repository)

        assert info.value.message == ALREADY_CREATED_MESSAGE_EXCEPTION % 'account'
