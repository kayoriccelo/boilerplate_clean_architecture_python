
from src.interface._common.controller import BaseController
from src.interface.controllers.account.validators import (
    AccountCreateValidator, AccountUpdateValidator
)
from src.interface.presenters.account import AccountPresenter
from src.use_cases.account.business import AccountBusiness
from src.domain.entities.account import Account


class AccountController(BaseController):
    business_class = AccountBusiness
    persenter_class = AccountPresenter

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
