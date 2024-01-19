import pytest


@pytest.mark.django_db
class BaseUseCaseRuleTest:
    entity_class = None
    repository_class = None
    rules_class = None

    @property
    def data(self):
        raise NotImplementedError('Implementation of the required method.')

    @property
    def entity(self):
        return self.entity_class(**self.data)

    @property
    def repository(self):
        return self.repository_class()
    
    @property
    def rules(self):
        return self.rules_class()


@pytest.mark.django_db
class BaseUseCaseBusinessTest:
    entity_class = None
    repository_class = None
    business_class = None

    @property
    def data(self):
        raise NotImplementedError('Implementation of the required method.')

    @property
    def entity(self):
        return self.entity_class(**self.data)

    @property
    def repository(self):
        return self.repository_class()
    
    @property
    def business(self):
        return self.business_class(self.repository)
