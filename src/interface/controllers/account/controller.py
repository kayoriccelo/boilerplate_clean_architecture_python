from src.interface._common.controller import BaseController
from src.interface.controllers.account.validators import (
    AccountCreateValidator, AccountUpdateValidator
)

from src.use_cases.account.business import AccountBusiness

from src.domain.entities.account import Account


class AccountController(BaseController):
    business_class = AccountBusiness

    def create(self, **kwargs) -> int:
        def do_create():
            validator = AccountCreateValidator()
            validator.is_valid(kwargs)

            account = Account(**self.validator.data)

            self.business.create(account)

        return self._to_try(do_create)

    def update(self, **kwargs) -> int:
        def do_update():
            validator = AccountUpdateValidator()
            validator.is_valid(kwargs)

            account = Account(**self.validator.data)

            self.business.update(account)
        
        return self._to_try(do_update)

    def delete(self, pk: int) -> int:
        def do_delete():
            self.business.delete(pk)

        return self._to_try(do_delete)