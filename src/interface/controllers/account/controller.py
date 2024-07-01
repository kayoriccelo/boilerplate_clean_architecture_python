from typing import Tuple

from src.interface._common.controller import BaseController
from src.interface.controllers.account.validators import (
    AccountCreateValidator, AccountUpdateValidator
)
from src.interface.presenters.account import AccountPresenter
from src.use_cases.account.business import AccountBusiness
from src.domain.entities.account import Account


class AccountController(BaseController):
    business_class = AccountBusiness
    presenter_class = AccountPresenter

    def get(self, pk: int) -> Tuple[dict, int]:
        def do_get():
            result = self.business.get(pk)

            return self.presenter.parse(result)

        return self._to_try(do_get)

    def list(self, page: int, page_size: int) -> Tuple[list, int]:
        def do_list():
            payload = self.business.available(page, page_size)

            data = ([self.presenter.parse(item) for item in payload['results']])

            return {
                'results': data,
                'count': payload['count'],
                'pages': payload['pages']
            }

        return self._to_try(do_list)

    def create(self, **kwargs) -> int:
        def do_create():
            validator = AccountCreateValidator()
            validator.is_valid(kwargs)

            account = Account(**validator.data)

            payload = self.business.create(instance=account, repository=self.business.repository)

            return self.presenter.parse(payload)

        return self._to_try(do_create)

    def update(self, **kwargs) -> int:
        def do_update():
            validator = AccountUpdateValidator()
            validator.is_valid(kwargs)

            account = Account(**validator.data)

            payload = self.business.update(instance=account, repository=self.business.repository)
        
            return self.presenter.parse(payload)
        
        return self._to_try(do_update)

    def delete(self, **kwargs) -> int:
        def do_delete():
            return self.business.delete(**kwargs)

        return self._to_try(do_delete)
