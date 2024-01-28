
from src.domain.entities import Account
from src.infrastructure._common.repositories import BaseModelRepository
from src.infrastructure.orm.django.apps.account.models import AccountModel


class AccountModelRepository(BaseModelRepository):
    class_model = AccountModel
    class_entity = Account

    def account_exists(self, account: Account) -> bool:
        accounts_model = self.class_model.objects.filter(
            number_identity=account.number_identity
        )

        return accounts_model.exists()
