from src.domain.entities import Broker
from src.infrastructure._common.repositories import BaseModelRepository
from src.infrastructure.django.apps.broker.models import BrokerModel


class BrokerModelRepository(BaseModelRepository):
    class_model = BrokerModel
    class_entity = Broker
