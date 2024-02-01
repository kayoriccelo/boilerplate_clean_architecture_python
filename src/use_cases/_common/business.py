
from src.core.exceptions.messages import (
    ACCESS_PAGE_LISTING_MESSAGE_EXCEPTION, CREATE_LISTING_RECORD_MESSAGE_EXCEPTION, CREATE_RECORD_MESSAGE_EXCEPTION
)
from src.core.exceptions.types import UseCaseBusinessException


class BaseBusiness:
    """
    Base Business class that implements the core business logic for the application.

    This class is responsible for enforcing business rules, managing the state of the system, and interacting with the data store.

    Attributes:
        repository (object): The repository object that is used to interact with the data store.
        entity_class (type): The entity class that is used to map data between the business layer and the data store.
        rules_class (type): The rules class that is used to enforce business rules.
        state_class (type): The state class that is used to manage the state of the system.
    """

    entity_class = None
    rules_class = None
    state_class = None

    def __init__(self, repository: object):
        """
        Initialize the BaseBusiness class.

        Args:
            repository (object): The repository object that is used to interact with the data store.
        """

        self.repository = repository
        self.rule = self.rules_class()
        self.state = self.state_class()

    def get(self, pk: int) -> object:
        """
        Get an entity from the data store based on the specified primary key.

        Args:
            pk (int): The primary key of the entity to retrieve.

        Returns:
            The entity that was retrieved from the data store.

        Raises:
            UseCaseBusinessException: If an error occurs while retrieving the entity.
        """

        instance = self.repository.get(pk)

        try:
            instance_entity = self.entity_class(**instance.asdict())
        
        except Exception as err:
            raise UseCaseBusinessException(err, CREATE_RECORD_MESSAGE_EXCEPTION)
        
        return instance_entity

    def available(self, page: int, page_size: int) -> dict:
        """
        Get a list of available entities from the data store.

        Args:
            page (int): The page number of the results to retrieve.
            page_size (int): The number of results to retrieve per page.

        Returns:
            A dictionary containing the count of available entities, the number of pages of results, and the list of entities.

        Raises:
            UseCaseBusinessException: If an error occurs while retrieving the entities.
        """

        pages = []
        results = []

        available = self.repository.available()

        try:
            available = [self.entity_class(**available.asdict()) for available in available]

        except Exception as err:
            raise UseCaseBusinessException(err, CREATE_LISTING_RECORD_MESSAGE_EXCEPTION)
        
        if len(available) > 0:
            try:
                pages = [available[i:i+page_size] for i in range(0, len(available), page_size)]
            
                results = pages[page - 1]

            except Exception as err:
                raise UseCaseBusinessException(err, ACCESS_PAGE_LISTING_MESSAGE_EXCEPTION % page)
        
        return {
            'count': len(available),
            'pages': len(pages),
            'results': results
        }

    def create(self, **kwargs):
        """
        Create an entity in the data store.

        Args:
            **kwargs: The keyword arguments that are used to create the entity.

        Returns:
            The entity that was created in the data store.

        Raises:
            UseCaseBusinessException: If an error occurs while creating the entity.
        """

        self.rule.can_create(**kwargs)

        return self.repository.create(kwargs['instance'])

    def update(self, **kwargs):
        """
        Update an entity in the data store.

        Args:
            **kwargs: The keyword arguments that are used to update the entity.

        Returns:
            The entity that was updated in the data store.

        Raises:
            UseCaseBusinessException: If an error occurs while updating the entity.
        """

        self.state.can_update(**kwargs)

        self.rule.can_update(**kwargs)

        return self.repository.update(kwargs['instance'])

    def delete(self, **kwargs):
        """
        Delete an entity from the data store.

        Args:
            **kwargs: The keyword arguments that are used to delete the entity.

        Returns:
            The entity that was deleted from the data store.

        Raises:
            UseCaseBusinessException: If an error occurs while deleting the entity.
        """

        self.state.can_delete(**kwargs)

        self.rule.can_delete(**kwargs)

        return self.repository.delete(kwargs['instance'])
