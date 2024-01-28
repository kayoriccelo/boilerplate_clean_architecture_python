
from src.use_cases._common.rules import BaseRules


class AccountRules(BaseRules):
    def __account_already_created(self):
        repository = self._get_value_in_kwargs('repository')
        account = self._get_value_in_kwargs('instance')

        account_exists = repository.account_exists(account)

        if account_exists:
            return self.execute_exception('account already created')
        
        return False
    
    def can_create(self, **kwargs):
        self._kwargs = kwargs

        self.execute_callback(self.__account_already_created)

        return self._can
    
    def can_update(self, **kwargs):
        self._kwargs = kwargs

        return self._can
    
    def can_delete(self, **kwargs):
        self._kwargs = kwargs
    
        return self._can
