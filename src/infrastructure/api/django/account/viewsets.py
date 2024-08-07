from src.infrastructure.api.django._common.viewsets import (
    BaseCreateViewSet, BaseDeleteViewSet, BaseGetViewSet, BaseListViewSet, BaseUpdateViewSet
)
from src.infrastructure.api.django.account.serializers import AccountSerializer
from src.infrastructure.orm.django.apps.account.repositories import AccountModelRepository
from src.interface.controllers import AccountController


class AccountViewSetMixin:
    repository_class = AccountModelRepository
    controller_class = AccountController
    serializer_class = AccountSerializer


class AccountGetViewSet(AccountViewSetMixin, BaseGetViewSet): pass
    

class AccountListViewSet(AccountViewSetMixin, BaseListViewSet): pass
    

class AccountCreateViewSet(AccountViewSetMixin, BaseCreateViewSet): pass
    

class AccountUpdateViewSet(AccountViewSetMixin, BaseUpdateViewSet): pass


class AccountDeleteViewSet(AccountViewSetMixin, BaseDeleteViewSet): pass
