import pytest


class BaseControllerTest:
    controller_class = None
    serializer_class = None

    @pytest.fixture(scope="class", autouse=True)
    def account_controller(self, account_repository):
        return self.controller_class(account_repository, self.serializer_class)
