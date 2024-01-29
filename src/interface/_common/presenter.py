
class BasePresenter:
    serializer_class = None

    def __init__(self, serializer_class: any) -> None:
        self.serializer_class = serializer_class

    def parse(self, instance: object) -> dict:
        result = self.serializer_class(instance)

        if hasattr(result, 'data'):
            self.data = result.data
            
        else:
            self.data = result

        return self.data
