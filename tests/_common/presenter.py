import pytest


class BasePresenterTest:
    presenter_class = None
    serializer_class = None

    @pytest.fixture(scope="class", autouse=True)
    def account_presenter(self):
        return self.presenter_class(self.serializer_class)
