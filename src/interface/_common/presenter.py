
class BasePresenter:
    """
    Base class for presenters.

    Responsible for parsing data from the database into a format that can be consumed by the view.
    """
    
    serializer_class = None

    def __init__(self, serializer_class: any) -> None:
        """
        Initialize the presenter.

        Args:
            serializer_class (any): The serializer class to use for parsing data.
        """

        self.serializer_class = serializer_class

    def parse(self, instance: object) -> dict:
        """
        Parse the data from the instance.

        Args:
            instance (object): The instance to parse.

        Returns:
            dict: The parsed data.
        """

        result = self.serializer_class(instance)

        if hasattr(result, 'data'):
            self.data = result.data

        else:
            self.data = result

        return self.data