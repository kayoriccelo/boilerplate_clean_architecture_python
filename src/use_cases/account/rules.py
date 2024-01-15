from src.use_cases._common.rules import BaseRules


class AccountRules(BaseRules):
    def __account_already_created(self):
        return False
    
    def __account_is_being_used(self):
        return False

    def can_create(self, **kwargs):
        self.execute_callback(self.__account_already_created)

        return self._can
    
    def can_update(self, **kwargs):
        return self._can
    
    def can_delete(self, **kwargs):
        self.execute_callback(self.__account_is_being_used)

        return self._can
