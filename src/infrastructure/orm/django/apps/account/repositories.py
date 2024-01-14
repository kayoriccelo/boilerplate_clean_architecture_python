from src.domain.entities import Account
from src.infrastructure._common.repositories import BaseModelRepository
from src.infrastructure.orm.django.apps.account.models import AccountModel


class AccountModelRepository(BaseModelRepository):
    class_model = AccountModel
    class_entity = Account
