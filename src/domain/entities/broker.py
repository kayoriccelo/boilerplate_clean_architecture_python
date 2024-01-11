from dataclasses import dataclass
from datetime import datetime

from src.domain.entities import Account


@dataclass
class Broker:
    id: int = None
    created: datetime = datetime.now()
    description: str = None
    account: Account = None
