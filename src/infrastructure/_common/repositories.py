
from typing import List
from django.forms import model_to_dict

from src.core.exceptions import RepositoryException


class BaseModelRepository:
    class_model = None
    class_entity = None

    def get(self, pk: int) -> object:
        instance = self.class_model.objects.filter(id=pk).values().first()
        
        if not instance:
            err = Exception(f'pk {pk} does not exist')

            raise RepositoryException(err, 'record not found')
        
        return self.class_entity(**instance)

    def get_availables(self) -> List[object]:
        return list(
            map(lambda value: self.class_entity(**value), self.class_model.objects.values())
        )

    def create(self, instance: object) -> object:
        try:
            instance_dict = instance.asdict()
        
            instance_model = self.class_model.objects.create(**instance_dict)

            instance_dict = model_to_dict(
                instance_model, 
                fields=[field.name for field in instance_model._meta.fields]
            )

            return self.class_entity(**instance_dict)

        except Exception as err:
            raise RepositoryException(err, 'error when trying to create model instance')

    def update(self, instance: object) -> object:
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
            raise RepositoryException(err, 'error when trying to update model instance')
        
    def delete(self, instance: object) -> object:
        try:
            return self.class_model.objects.filter(id=instance.id).delete()

        except Exception as err:
            raise RepositoryException(err, 'error when trying to delete model instance')
