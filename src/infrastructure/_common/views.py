
from src.core.exceptions import ViewException


class BaseViewSet:
    repository_class = None
    controller_class = None
    presenter_class = None

    def __start_repository(self) -> any:
        try:
            return self.repository_class()
        
        except:
            raise ViewException('error when trying to instantiate the repository.')
    
    def __start_controller(self):
        repository = self.__start_repository()

        try:
            self.controller = self.controller_class(repository)

        except:
            raise ViewException('error when trying to instantiate the controller.')

    def __init__(self, **kwargs: any) -> None:
        super().__init__(**kwargs)

        self.__start_controller()
