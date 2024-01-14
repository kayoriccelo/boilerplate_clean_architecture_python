from src.domain.entities import Active
from src.infrastructure._common.repositories import BaseModelRepository
from src.infrastructure.orm.django.apps.active.models import ActiveModel


class ActiveModelRepository(BaseModelRepository):
    class_model = ActiveModel
    class_entity = Active