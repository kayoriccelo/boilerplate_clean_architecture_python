
import copy
import pytest

from src.core.exceptions.messages import OPERATION_WITHOUT_PERMISSION_MESSAGE_EXCEPTION
from src.core.exceptions.types import UseCaseStateException
from src.domain.entities.account import Account, StatusAccount
from src.use_cases.account.state import AccountState

from tests._common.use_case import BaseUseCaseStateTest


class TestAccountState(BaseUseCaseStateTest):
    state_class = AccountState

    def test_can_update(self, account_entity: Account):
        can = self.state.can_update(instance=account_entity, exception=False)

        assert can == True

    def test_can_update_exception(self, account_entity: Account):
        with pytest.raises(UseCaseStateException) as info:
            instance = copy.copy(account_entity)
            
            instance.status = StatusAccount.INACTIVE.value
            self.state.can_update(instance=instance, exception=True)

            del instance

        assert info.value.message == OPERATION_WITHOUT_PERMISSION_MESSAGE_EXCEPTION

    def test_can_delete(self, account_entity: Account):
        can = self.state.can_delete(instance=account_entity, exception=False)

        assert can == True

    def test_can_delete_exception(self, account_entity: Account):
        with pytest.raises(UseCaseStateException) as info:
            instance = copy.copy(account_entity)
            
            instance.status = StatusAccount.INACTIVE.value            
            self.state.can_delete(instance=instance, exception=True)

            del instance

        assert info.value.message == OPERATION_WITHOUT_PERMISSION_MESSAGE_EXCEPTION
