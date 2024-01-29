
from src.core.exceptions import UseCaseBusinessException


class BaseBusiness:
    entity_class = None
    rules_class = None
    state_class = None

    def __init__(self, repository: object):
        self.repository = repository
        self.rule = self.rules_class()
        self.state = self.state_class()

    def get(self, pk: int) -> object:
        instance = self.repository.get(pk)

        try:
            instance_entity = self.entity_class(**instance.asdict())
        
        except Exception as err:
            raise UseCaseBusinessException(err, 'create the record')
        
        return instance_entity

    def get_availables(self, page: int, page_size: int) -> dict:
        pages = []
        results = []

        availables = self.repository.get_availables()

        try:
            availables = [self.entity_class(**available.asdict()) for available in availables]

        except Exception as err:
            raise UseCaseBusinessException(err, 'create listing records')
        
        if len(availables) > 0:
            try:
                pages = [availables[i:i+page_size] for i in range(0, len(availables), page_size)]
            
                results = pages[page - 1]

            except Exception as err:
                raise UseCaseBusinessException(err, f'access page {page} of the listing')
        
        return {
            'count': len(availables),
            'pages': len(pages),
            'results': results
        }

    def create(self, **kwargs):
        self.state.can_create(**kwargs)

        self.rule.can_create(**kwargs)

        return self.repository.create(kwargs['instance'])

    def update(self, **kwargs):
        self.state.can_update(**kwargs)

        self.rule.can_update(**kwargs)

        return self.repository.update(kwargs['instance'])

    def delete(self, **kwargs):
        self.state.can_delete(**kwargs)

        self.rule.can_delete(**kwargs)

        return self.repository.delete(kwargs['instance'])
