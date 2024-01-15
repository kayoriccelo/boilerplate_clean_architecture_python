
from http.client import BAD_REQUEST, OK
from typing import Tuple

from src.core.exceptions import RepositoryException, UseCaseException, ValidatorException


class BaseController:
    business_class = None
    
    def __init__(self, repository: object):
        self.business = self.business_class(repository)

    def get(self, pk: int) -> Tuple[dict, int]:
        try:
            instance = self.business.get(pk)

        except RepositoryException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'error': str(err)}, BAD_REQUEST.value

        except ValidatorException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'error': str(err)}, BAD_REQUEST.value

        except UseCaseException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'error': str(err)}, BAD_REQUEST.value

        return instance, OK.value

    def list(self, page: int, page_size: int) -> Tuple[list, int]:
        try:
            instances = self.business.get_availables(page, page_size)
            
        except RepositoryException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'error': str(err)}, BAD_REQUEST.value
        
        except ValidatorException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'error': str(err)}, BAD_REQUEST.value

        except UseCaseException as err:
            # TODO - Kayo: display nice message and send error message to technical control.
            return {'error': str(err)}, BAD_REQUEST.value

        return instances, OK.value
