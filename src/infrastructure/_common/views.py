
from src.core.exceptions.types import ViewsetException
from src.core.exceptions.messages import (
    ERROR_INSTANTIATE_CONTROLLER_MESSAGE_EXCEPTION,
    ERROR_INSTANTIATE_REPOSITORY_MESSAGE_EXCEPTION
)


class BaseViewSet:
    """Base ViewSet class that provides common methods and attributes for all ViewSets."""

    repository_class = None
    controller_class = None
    presenter_class = None

    def __start_repository(self) -> any:
        """Method to instantiate the repository."""

        try:
            return self.repository_class()
        
        except Exception as err:
            raise ViewsetException(
                err, ERROR_INSTANTIATE_REPOSITORY_MESSAGE_EXCEPTION
            )
    
    def __start_controller(self):
        """Method to instantiate the controller."""

        repository = self.__start_repository()

        try:
            self.controller = self.controller_class(repository)

        except Exception as err:
            raise ViewsetException(
                err, ERROR_INSTANTIATE_CONTROLLER_MESSAGE_EXCEPTION
            )

    def __init__(self, **kwargs: any) -> None:
        """Method to initialize the BaseViewSet."""
        
        super().__init__(**kwargs)

        self.__start_controller()