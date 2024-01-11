
class BaseViewSet:
    serializer_many = False
    repository_class = None
    controller_class = None
    serializer_class = None

    def __start_repository(self) -> any:
        try:
            return self.repository_class()
        
        except:
            raise Exception('error when trying to instantiate the repository.')
    
    def __start_controller(self):
        try:
            repository = self.__start_repository()

            self.controller = self.controller_class(repository)

        except:
            raise Exception('error when trying to instantiate the controller.')
        
    def __start_serializer(self):
        try:
            self.serializer = self.serializer_class(many=self.serializer_many)

        except:
            raise Exception('error when trying to instantiate the serializer.')

    def __init__(self, **kwargs: any) -> None:
        super().__init__(**kwargs)

        self.__start_controller()
        self.__start_serializer()
