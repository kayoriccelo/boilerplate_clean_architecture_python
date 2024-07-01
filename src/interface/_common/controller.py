from http.client import INTERNAL_SERVER_ERROR, OK

from src.core.useful import send_email_error
from src.core.exceptions.types import (
    RepositoryException, UseCaseRuleException, UseCaseBusinessException, ValidatorException
)
from src.core.exceptions.messages import (
    INCONSISTENCY_MESSAGE_FOUND, INCONSISTENCY_MESSAGE_FOUND_SYSTEM
)


class BaseController:
    """
    The BaseController class is a base class for all controllers in the application. It provides
    a set of common methods and functionality that can be used by all controllers.

    Attributes:
        business_class (object): The business class that is used to perform business logic.
        presenter_class (object): The presenter class that is used to present data to the user.

    """

    business_class = None
    presenter_class = None

    def __init__(self, repository: object, serializer_class: object):
        self.business = self.business_class(repository)
        self.presenter = self.presenter_class(serializer_class)

    def _to_try(self, callback):
        """
        A helper function that wraps a function in a try/except block.

        Args:
            callback (function): The function that is being wrapped.

        Returns:
            tuple: A tuple containing the result of the function and the HTTP status code.

        """

        try:
            payload = callback()

        except ValidatorException as err:
            return {
                'type': 'validator',
                'message': err.message,
                'errors': err.errors
            }, INTERNAL_SERVER_ERROR.value

        except UseCaseRuleException as err:
            return {
                'type': 'rule',
                'message': err.message
            }, INTERNAL_SERVER_ERROR.value

        except UseCaseBusinessException as err:
            send_email_error(err)

            return {
                'type': 'business',
                'message': INCONSISTENCY_MESSAGE_FOUND % err.message
            }, INTERNAL_SERVER_ERROR.value

        except RepositoryException as err:
            send_email_error(err)

            return {
                'type': 'repository',
                'message': INCONSISTENCY_MESSAGE_FOUND_SYSTEM
            }, INTERNAL_SERVER_ERROR.value

        except Exception as err:
            send_email_error(err)

            return {
                'type': 'generic',
                'message': INCONSISTENCY_MESSAGE_FOUND_SYSTEM
            }, INTERNAL_SERVER_ERROR.value

        return payload, OK.value
