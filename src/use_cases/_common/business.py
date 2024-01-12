from typing import List


class BaseBusiness:
    rules_class = None

    def __init__(self, repository: object):
        self.repository = repository
        self.rule = self.rules_class()

    def get(self, pk: int) -> object:
        return self.repository.get(pk)

    def get_availables(self, page: int, page_size: int) -> dict:
        availables = self.repository.get_availables()

        pages = []
        results = []
        
        if len(availables) > 0:
            pages = [availables[i:i+page_size] for i in range(0, len(availables), page_size)]
            results = pages[page - 1]
        
        return {
            'count': len(availables),
            'pages': len(pages),
            'results': results
        }

    def create(self, **kwargs):
        self.rule.can_create(**kwargs)

        self.repository.create(**kwargs)

    def update(self, **kwargs):
        self.rule.can_update(**kwargs)

        self.repository.create(**kwargs)

    def delete(self, **kwargs):
        self.rule.can_delete(**kwargs)

        self.repository.delete(**kwargs)
