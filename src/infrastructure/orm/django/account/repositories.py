
import dataclasses
from typing import List

from src.domain.entities.account import Account
from src.infrastructure.orm.django.account.models import AccountModel


class AccountModelRepository:
    def get(self, pk: int) -> Account:
        account_model = AccountModel.objects.filter(pk=pk).values().first()
        
        if not account_model:
            raise Exception(f'{pk} account pk does not exist.')
        
        return Account(**account_model)

    def get_availables(self) -> List[Account]:
        return list(map(lambda value: Account(**value), AccountModel.objects.values()))

    def create(self, account: Account):
        try:
            account_dict = dataclasses.asdict(account)
        
            AccountModel.objects.create(**account_dict)

        except:
            raise Exception('error when trying to create account model.')

    def update(self, pk: int, account: Account):
        try:
            account_dict = dataclasses.asdict(account)

            AccountModel.objects.filter(pk=pk).update(**account_dict)

        except:
            raise Exception('error when trying to update account model.')
