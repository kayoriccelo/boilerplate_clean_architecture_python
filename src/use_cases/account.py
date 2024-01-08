from typing import List

from src.domain.entities.account import Account


class AccountUseCase:
    def __init__(self, account_repo: object):
        self.account_repo = account_repo

    def get(self, pk: int) -> Account:
        return self.account_repo.get(pk)

    def get_availables(self) -> List[Account]:
        return self.account_repo.get_availables()

    def create(self, account: Account):
        # TODO - Kayo: add rules.

        self.account_repo.create(account)

    def update(self, pk: int, account: Account):
        # TODO - Kayo: add rules.

        self.account_repo.create(pk, account)

    def delete(self, pk: int):
        # TODO - Kayo: add rules.

        self.account_repo.delete(pk)
