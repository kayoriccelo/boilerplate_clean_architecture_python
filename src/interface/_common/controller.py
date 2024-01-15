
from http.client import BAD_REQUEST, OK
from typing import Tuple

from src.core.exceptions import RepositoryException, UseCaseException, ValidatorException


class BaseController:
    business_class = None
    
    def __init__(self, repository: object):
        self.business = self.business_class(repository)

    def _to_try(self, callback):
        try:
            result = callback()

        except RepositoryException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'error': str(err)}, BAD_REQUEST.value

        except ValidatorException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'error': str(err)}, BAD_REQUEST.value

        except UseCaseException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'error': str(err)}, BAD_REQUEST.value
        
        return result, OK.value

    def get(self, pk: int) -> Tuple[dict, int]:
        def do_get():
            return self.business.get(pk)
        
        return self._to_try(do_get)

    def list(self, page: int, page_size: int) -> Tuple[list, int]:
        def do_list():
            return self.business.get_availables(page, page_size)
        
        return self._to_try(do_list)
