
from src.use_cases._common.state import BaseState
from src.domain.entities.account import StatusAccount


class AccountState(BaseState):
    def situation_active(self):
        return self.status == StatusAccount.ACTIVE.value

    def situation_inactive(self):
        return self.status == StatusAccount.INACTIVE.value
    
    def can_create(self, **kwargs):
        self._kwargs = kwargs

        return self._can
    
    def can_update(self, **kwargs):
        self._kwargs = kwargs

        self.execute_callback([self.situation_active])

        return self._can
    
    def can_delete(self, **kwargs):
        self._kwargs = kwargs

        return self._can
