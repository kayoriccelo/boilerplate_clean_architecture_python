

class BaseBuilder:
    def build(self, **kwargs) -> object:
        raise NotImplementedError('Implementation of the required method.')


class BaseStateBuilder(BaseBuilder):
    STATE_CLASSES = {}
        
    def build(self, **kwargs) -> object:
        state_class = self.STATE_CLASSES.get(kwargs['status'])

        return state_class(kwargs['model_object'])
