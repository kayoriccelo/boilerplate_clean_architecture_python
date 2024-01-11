from src.use_cases._common.rules import BaseRules


class AccountRules(BaseRules):    
    def can_create(self, **kwargs):
        return True
    
    def can_update(self, **kwargs):
        return True
    
    def can_delete(self, **kwargs):
        return True
