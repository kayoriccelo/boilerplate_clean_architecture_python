from src.infrastructure.api.django.views.base import (
    BaseCreateViewSet, BaseDeleteViewSet, BaseGetViewSet, BaseListViewSet, BaseUpdateViewSet
)
from src.infrastructure.orm.django.account.repositories import AccountModelRepository
from src.infrastructure.serializers.account import AccountSerializer
from src.interface.controllers.account import AccountController


class AccountViewSetMixin:
    repository_class = AccountModelRepository
    controller_class = AccountController
    serializer_class = AccountSerializer
    

class AccountGetViewSet(AccountViewSetMixin, BaseGetViewSet): pass
    

class AccountListViewSet(AccountViewSetMixin, BaseListViewSet): pass
    

class AccountCreateViewSet(AccountViewSetMixin, BaseCreateViewSet): pass
    

class AccountUpdateViewSet(AccountViewSetMixin, BaseUpdateViewSet): pass


class AccountDeleteViewSet(AccountViewSetMixin, BaseDeleteViewSet): pass
