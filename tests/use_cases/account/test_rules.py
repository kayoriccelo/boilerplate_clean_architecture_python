import pytest

from src.core.exceptions import SystemException, UseCaseRuleException
from src.use_cases.account.rules import AccountRules

from tests._common.use_case import BaseUseCaseRuleTest


@pytest.mark.order(20000)
class TestAccountRules(BaseUseCaseRuleTest):
    rules_class = AccountRules
    
    def test_can_create(self, account_entity, account_repository):
        try:
            self.rules.can_create(instance=account_entity, repository=account_repository)

            assert True

        except UseCaseRuleException:
            assert False

    def test_can_create_exception_repository(self, account_entity, account_repository):
        try:
            account_repository.active_exception = True

            self.rules.can_create()

            assert False

        except SystemException as err:
            assert err.message == 'repository not found in AccountRules'

        finally:
            account_repository.active_exception = False
    
        try:
            account_repository.active_exception = True

            self.rules.can_create(instance=account_entity)

            assert False

        except SystemException as err:
            assert err.message == 'repository not found in AccountRules'

        finally:
            account_repository.active_exception = False

    def test_can_create_exception_instance(self, account_repository):
        try:
            account_repository.active_exception = True

            self.rules.can_create(repository=account_repository)

            assert False

        except SystemException as err:
            assert err.message == 'instance not found in AccountRules'

        finally:
            account_repository.active_exception = False

    def test_can_create_exception_account_already_created(self, account_entity, account_repository):
        try:
            account_repository.active_exception = True

            self.rules.can_create(instance=account_entity, repository=account_repository)

            assert False

        except UseCaseRuleException as err:
            assert err.message == 'account already created'

        finally:
            account_repository.active_exception = False
