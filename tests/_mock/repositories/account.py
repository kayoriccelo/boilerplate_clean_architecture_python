from typing import List
from src.core.exceptions.messages import (
    ERROR_CREATE_MODEL_INSTANCE_MESSAGE_EXCEPTION, ERROR_DELETE_MODEL_INSTANCE_MESSAGE_EXCEPTION, 
    ERROR_UPDATE_MODEL_INSTANCE_MESSAGE_EXCEPTION, PK_NOT_EXIST_MESSAGE_EXCEPTION, 
    RECORD_NOT_FOUND_MESSAGE_EXCEPTION
)
from src.domain.entities.account import Account

from tests._common.mock import BaseRepositoryMock


class AccountRepositoryMock(BaseRepositoryMock):
    def get(self, pk: int) -> object:
        self._simulate_exception(
            RECORD_NOT_FOUND_MESSAGE_EXCEPTION, Exception(PK_NOT_EXIST_MESSAGE_EXCEPTION % pk)
        )
        
        return self.instance_entity

    def available(self) -> List[object]:        
        return [self.instance_entity]
    
    def create(self, instance: object) -> object:
        self._simulate_exception(ERROR_CREATE_MODEL_INSTANCE_MESSAGE_EXCEPTION)
        
        return self.instance_entity

    def update(self, instance: object) -> object:
        self._simulate_exception(ERROR_UPDATE_MODEL_INSTANCE_MESSAGE_EXCEPTION)
        
        return self.instance_entity
    
    def delete(self, instance: object) -> object:
        self._simulate_exception(ERROR_DELETE_MODEL_INSTANCE_MESSAGE_EXCEPTION)

    def account_exists(self, account: Account) -> bool:
        if self.active_exception:
            return True

        return False
