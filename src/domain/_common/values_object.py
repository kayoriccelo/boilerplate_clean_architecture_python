
class ValueObject:
    """
    A base class for immutable value objects.

    This class provides a way to define an immutable value object by defining a 
    default value and a way to set and retrieve its value.

    The default value can be set using the default class attribute. The value of 
    the object can be accessed using the __get__ and __set__ special methods.
    """

    default: any = None

    def __init__(self, **kwargs) -> None:
        self.default = kwargs.get('default', self.default)

        self.set_name(self.__class__.__name__, id(self))

    def set_name(self, prefix: str, key: int) -> None:
        """
        Set the name of the value object.

        Args:
            prefix: The prefix to use for the name.
            key: The unique key for the value object.
        """

        self.target_name = f"__{prefix.lower()}_{key}"

    def __get__(self, instance: any, owner: any) -> any:
        """
        Get the value of the value object.

        Args:
            instance: The instance of the value object.
            owner: The class of the value object.

        Returns:
            The value of the value object.
        """
       
        value = self.default

        if hasattr(instance, self.target_name):
            value = getattr(instance, self.target_name)

        else:
            setattr(instance, self.target_name, value)

        return value

    def __set__(self, instance: any, value: any = None) -> None:
        """
        Set the value of the value object.

        Args:
            instance: The instance of the value object.
            value: The value to set.
        """
        
        setattr(instance, self.target_name, value)
