
class BaseEntityTest:
    @property
    def data(self):
        raise NotImplementedError('Implementation of the required method.')
    
    def test_create(self):
        raise NotImplementedError('Implementation of the required method.')
    
    def test_update(self):
        raise NotImplementedError('Implementation of the required method.')
