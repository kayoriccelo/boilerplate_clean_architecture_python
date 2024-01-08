from http import HTTPStatus
from typing import Tuple

from src.use_cases.account import AccountUseCase


class AccountController:
    def __init__(self, repository: object):
        self.use_case = AccountUseCase(repository)

    def get(self, pk: int) -> Tuple[dict, int]:
        try:
            account = self.use_case.get(pk)

        except Exception as err:
            return {'error': err.message}, HTTPStatus.NOT_FOUND.value

        
        return account, HTTPStatus.OK.value

    def list(self) -> Tuple[list, int]:
        accounts = self.use_case.get_availables()

        return accounts, HTTPStatus.OK.value

    def create(self, data: dict) -> int:
        self.use_case.create(data)
        
        return HTTPStatus.OK.value

    def update(self, data: dict) -> int:
        self.use_case.update(data)

        return HTTPStatus.OK.value

    def delete(self, pk: int) -> int:
        self.use_case.delete(pk)

        return HTTPStatus.OK.value