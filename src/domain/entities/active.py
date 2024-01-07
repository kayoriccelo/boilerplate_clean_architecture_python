from dataclasses import dataclass


@dataclass
class Active:
    description: str = None
    account: int = None
    broker: int = None
