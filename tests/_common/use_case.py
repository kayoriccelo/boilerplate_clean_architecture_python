import pytest


class BaseUseCaseRuleTest:
    rules_class = None

    @property
    def rules(self):
        return self.rules_class()


class BaseUseCaseBusinessTest:
    business_class = None
    
    @pytest.fixture(scope="class", autouse=True)
    def account_business(self, account_repository):
        return self.business_class(repository=account_repository)


class BaseUseCaseStateTest:
    state_class = None
    
    @property
    def state(self):
        return self.state_class()
