
from src.domain._common.metaclass import EntityMetaclass


class BaseEntity:
    __metaclass__ = EntityMetaclass

    def __init__(self, **kwargs):
        for attribute in dir(self):
            if attribute in kwargs:
                setattr(self, attribute, kwargs[attribute])
                
    def asdict(self):
        dictionary = dict()

        for attribute in dir(self):
            if not f'_' in attribute[0]:
                value = getattr(self, attribute)

                if not type(value).__name__ == 'method' and value:
                    dictionary[attribute] = value

        return dictionary