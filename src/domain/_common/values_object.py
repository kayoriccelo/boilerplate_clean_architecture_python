
class ValueObject:
    default: any = None

    def __init__(self, **kwargs) -> None:
        self.default = kwargs.get('default', self.default)

        self.set_name(self.__class__.__name__, id(self))

    def set_name(self, prefix, key):
        self.targe_name = f'__{prefix.lower()}_{key}'

    def __get__(self, instance, owner):
        value = self.default

        if hasattr(instance, self.targe_name):
            value = getattr(instance, self.targe_name)
        
        else:
            setattr(instance, self.targe_name, value)

        return value
    
    def __set__(self, instance, value=None):
        setattr(instance, self.targe_name, value)
