
from typing import List
from django.forms import model_to_dict

from src.core.exceptions.types import RepositoryException
from src.core.exceptions.messages import (
    ERROR_CREATE_MODEL_INSTANCE_MESSAGE_EXCEPTION, ERROR_DELETE_MODEL_INSTANCE_MESSAGE_EXCEPTION, 
    ERROR_UPDATE_MODEL_INSTANCE_MESSAGE_EXCEPTION, PK_NOT_EXIST_MESSAGE_EXCEPTION, 
    RECORD_NOT_FOUND_MESSAGE_EXCEPTION
)


class BaseModelRepository:
    """
    Base class for all model repositories.

    This class provides basic methods for interacting with the database,
    such as creating, updating, deleting, and retrieving model instances.
    """

    class_model = None
    class_entity = None

    def get(self, pk: int) -> object:
        """
        Retrieve an instance of the model based on its primary key.

        Args:
            pk (int): The primary key of the model instance to retrieve.

        Returns:
            The model instance with the specified primary key, or None if no instance was found.

        Raises:
            RepositoryException: If an error occurs while retrieving the instance.
        """

        instance = self.class_model.objects.filter(id=pk).values().first()

        if not instance:
            err = Exception(PK_NOT_EXIST_MESSAGE_EXCEPTION % pk)

            raise RepositoryException(err, RECORD_NOT_FOUND_MESSAGE_EXCEPTION)

        return self.class_entity(**instance)

    def available(self) -> List[object]:
        """
        Retrieve a list of all available model instances.

        Returns:
            A list of all available model instances.

        Raises:
            RepositoryException: If an error occurs while retrieving the instances.
        """

        return list(
            map(lambda value: self.class_entity(**value), self.class_model.objects.values())
        )

    def create(self, instance: object) -> object:
        """
        Create a new instance of the model.

        Args:
            instance (object): The instance of the model to create.

        Returns:
            The created instance of the model.

        Raises:
            RepositoryException: If an error occurs while creating the instance.
        """

        try:
            instance_dict = instance.asdict()

            instance_model = self.class_model.objects.create(**instance_dict)

            instance_dict = model_to_dict(
                instance_model,
                fields=[field.name for field in instance_model._meta.fields]
            )

            return self.class_entity(**instance_dict)

        except Exception as err:
            raise RepositoryException(err, ERROR_CREATE_MODEL_INSTANCE_MESSAGE_EXCEPTION)

    def update(self, instance: object) -> object:
        """
        Update an existing instance of the model.

        Args:
            instance (object): The instance of the model to update.

        Returns:
            The updated instance of the model.

        Raises:
            RepositoryException: If an error occurs while updating the instance.
        """

        try:
            instance_dict = instance.asdict()

            self.class_model.objects.filter(id=instance.id).update(**instance_dict)

            instance_model = self.class_model.objects.get(id=instance.id)

            instance_dict = model_to_dict(
                instance_model,
                fields=[field.name for field in instance_model._meta.fields]
            )

            return self.class_entity(**instance_dict)

        except Exception as err:
            raise RepositoryException(err, ERROR_UPDATE_MODEL_INSTANCE_MESSAGE_EXCEPTION)

    def delete(self, instance: object) -> object:
        """
        Delete an existing instance of the model.

        Args:
            instance (object): The instance of the model to delete.

        Returns:
            The number of instances deleted.

        Raises:
            RepositoryException: If an error occurs while deleting the instance.
        """
        
        try:
            return self.class_model.objects.filter(id=instance.id).delete()

        except Exception as err:
            raise RepositoryException(err, ERROR_DELETE_MODEL_INSTANCE_MESSAGE_EXCEPTION)