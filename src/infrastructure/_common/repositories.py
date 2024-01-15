
import dataclasses
from typing import List

from src.core.exceptions import RepositoryException


class BaseModelRepository:
    class_model = None
    class_entity = None

    def get(self, pk: int) -> object:
        instance = self.class_model.objects.filter(pk=pk).values().first()
        
        if not instance:
            raise RepositoryException(Exception(f'{pk} pk does not exist'), f'record not found.')
        
        return self.class_entity(**instance)

    def get_availables(self) -> List[object]:
        return list(map(lambda value: self.class_entity(**value), self.class_model.objects.values()))

    def create(self, **kwargs):
        try:
            instance_dict = dataclasses.asdict(**kwargs)
        
            self.class_model.objects.create(**instance_dict)

        except Exception as err:
            raise RepositoryException(err, 'error when trying to create model instance.')

    def update(self, pk: int, instance: object):
        try:
            instance_dict = dataclasses.asdict(instance)

            self.class_model.objects.filter(pk=pk).update(**instance_dict)

        except Exception as err:
            raise RepositoryException(err, 'error when trying to update model instance.')
        
    def delete(self, pk: int):
        try:
            self.class_model.objects.filter(pk=pk).delete()

        except Exception as err:
            raise RepositoryException(err, 'error when trying to delete model instance.')
