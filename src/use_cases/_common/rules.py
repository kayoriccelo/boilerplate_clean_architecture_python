
class BaseRules:    
    def can_create(self, **kwargs):
        raise NotImplementedError('method not implemented.')
    
    def can_update(self, **kwargs):
        raise NotImplementedError('method not implemented.')
    
    def can_delete(self, **kwargs):
        raise NotImplementedError('method not implemented.')
