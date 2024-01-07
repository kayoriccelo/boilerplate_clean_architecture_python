from dataclasses import dataclass
from datetime import datetime


@dataclass
class Account:
    id: int = None
    created: datetime = None
    first_name: str = None
    last_name: str = None
    number_identity: str = None
    date_birth: datetime = None
    gender: int = None
    status: int = None
