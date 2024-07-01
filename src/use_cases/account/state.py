
from src.use_cases._common.state import BaseState
from src.domain.entities.account import StatusAccount


class AccountState(BaseState):
    def situation_active(self):
        return self.status == StatusAccount.ACTIVE.value

    def situation_inactive(self):
        return self.status == StatusAccount.INACTIVE.value
        
    def can_update(self, **kwargs):
        return False
    
    def can_delete(self, **kwargs):
        return False


class AccountActiveState(AccountState):
    _status_permission = [StatusAccount.INACTIVE.value]

    def can_update(self, **kwargs):
        return True
    
    def can_delete(self, **kwargs):
        return True


class AccountInactiveState(AccountState):
    _status_permission = []
