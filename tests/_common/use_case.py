import pytest


class BaseUseCaseRuleTest:
    rules_class = None

    @property
    def rules(self):
        return self.rules_class()


class BaseUseCaseBusinessTest:
    business_class = None
    _business = None
    
    @pytest.fixture(scope="class", autouse=True)
    def account_business(self, account_repository):
        return self.business_class(repository=account_repository)
