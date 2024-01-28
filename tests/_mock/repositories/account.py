from typing import List
from src.domain.entities.account import Account

from tests._common.mock import BaseRepositoryMock


class AccountRepositoryMock(BaseRepositoryMock):
    def get(self, pk: int) -> object:
        self._simulate_exception('record not found', Exception(f'pk {pk} does not exist'))
        
        return self.instance_entity

    def get_availables(self) -> List[object]:        
        return [self.instance_entity]
    
    def create(self, instance: object) -> object:
        self._simulate_exception('error when trying to create model instance')
        
        return self.instance_entity

    def update(self, instance: object) -> object:
        self._simulate_exception('error when trying to update model instance')
        
        return self.instance_entity
    
    def delete(self, instance: object) -> object:
        self._simulate_exception('error when trying to delete model instance')

    def account_exists(self, account: Account) -> bool:
        if self.active_exception:
            return True

        return False
