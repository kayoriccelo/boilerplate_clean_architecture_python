
from src.domain._common.metaclass import EntityMetaclass


class BaseEntity:
    """
    Base class for all entities in the system.

    This class provides the basic functionality for all entities, including
    the ability to convert the entity to a dictionary representation.
    """

    __metaclass__ = EntityMetaclass

    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            if not attribute.startswith('__'):
                setattr(self, attribute, value)

    def asdict(self):
        """
        Converts the entity to a dictionary representation.

        Returns:
            dict: The dictionary representation of the entity.
        """

        dictionary = dict()

        for attribute in dir(self):
            if attribute.startswith('__'): continue
            if callable(getattr(self, attribute)): continue
            if getattr(self, attribute) is None: continue

            dictionary[attribute] = getattr(self, attribute)

        return dictionary
