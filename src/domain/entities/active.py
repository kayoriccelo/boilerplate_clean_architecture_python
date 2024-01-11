from dataclasses import dataclass
from datetime import datetime

from src.domain.entities import Account, Broker


@dataclass
class Active:
    id: int = None
    created: datetime = datetime.now()
    description: str = None
    account: Account = None
    broker: Broker = None
