import dataclasses

from src.core.exceptions import UseCaseException


class BaseBusiness:
    entity_class = None
    rules_class = None

    def __init__(self, repository: object):
        self.repository = repository
        self.rule = self.rules_class()

    def get(self, pk: int) -> object:
        instance_model = self.repository.get(pk)

        try:
            instance_entity = self.entity_class(**dataclasses.asdict(instance_model))
        
        except Exception as e:
            raise UseCaseException(f'The entity cannot be instantiated. {str(e)}')
        
        return instance_entity

    def get_availables(self, page: int, page_size: int) -> dict:
        pages = []
        results = []

        availables = self.repository.get_availables()

        try:
            availables = [self.entity_class(**dataclasses.asdict(available)) for available in availables]

        except Exception as e:
            raise UseCaseException(f'Entities cannot be instantiated. {str(e)}')
        
        if len(availables) > 0:
            try:
                pages = [availables[i:i+page_size] for i in range(0, len(availables), page_size)]
            
            except Exception as e:
                raise UseCaseException(f'Unable to perform pagination. {str(e)}')
            
            try:
                results = pages[page - 1]

            except Exception as e:
                raise UseCaseException(f'Unable to access the page. {str(e)}')
        
        return {
            'count': len(availables),
            'pages': len(pages),
            'results': results
        }

    def create(self, instance: object, **kwargs):
        self.rule.can_create(instance)

        self.repository.create(instance)

    def update(self, instance: object, **kwargs):
        self.rule.can_update(instance)

        self.repository.create(instance)

    def delete(self, instance: object, **kwargs):
        self.rule.can_delete(instance)

        self.repository.delete(instance)
