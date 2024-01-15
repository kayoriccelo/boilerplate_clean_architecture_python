from http.client import BAD_REQUEST, OK

from src.core.exceptions import (
    EntityException, RepositoryException, UseCaseException, ValidatorException
)
from src.interface._common.controller import BaseController
from src.interface.controllers.account.validators import (
    AccountCreateValidator, AccountUpdateValidator
)

from src.use_cases.account.business import AccountBusiness

from src.domain.entities.account import Account


class AccountController(BaseController):
    business_class = AccountBusiness

    def create(self, **kwargs) -> int:
        try:
            validator = AccountCreateValidator()
            validator.is_valid(kwargs)

            account = Account(**self.validator.data)

            self.business.create(account)

        except RepositoryException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'message': str(err)}, BAD_REQUEST.value

        except ValidatorException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'message': str(err)}, BAD_REQUEST.value

        except UseCaseException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'message': str(err)}, BAD_REQUEST.value
        
        except EntityException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'message': str(err)}, BAD_REQUEST.value
        
        return OK.value

    def update(self, **kwargs) -> int:
        try:
            validator = AccountUpdateValidator()
            validator.is_valid(kwargs)

            account = Account(**self.validator.data)

            self.business.update(account)

        except RepositoryException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'message': str(err)}, BAD_REQUEST.value
        
        except ValidatorException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'message': str(err)}, BAD_REQUEST.value

        except UseCaseException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'message': str(err)}, BAD_REQUEST.value
        
        except EntityException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'message': str(err)}, BAD_REQUEST.value

        return OK.value

    def delete(self, pk: int) -> int:
        try:
            self.business.delete(pk)

        except RepositoryException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'message': str(err)}, BAD_REQUEST.value

        except ValidatorException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'message': str(err)}, BAD_REQUEST.value

        except UseCaseException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'message': str(err)}, BAD_REQUEST.value
        
        except EntityException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'message': str(err)}, BAD_REQUEST.value

        return OK.value