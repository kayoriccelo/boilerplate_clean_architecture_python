
from src.infrastructure.api.django.account.serializers import AccountSerializer
from src.interface.presenters.account import AccountPresenter

from tests._common.presenter import BasePresenterTest


class TestAccountPresenter(BasePresenterTest):
    presenter_class = AccountPresenter
    serializer_class = AccountSerializer

    def test_parse(self, account_entity, account_presenter):
        payload = account_presenter.parse(account_entity)

        assert self.serializer_class(account_entity).data == payload
