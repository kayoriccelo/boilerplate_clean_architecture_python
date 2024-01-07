from dataclasses import dataclass
from datetime import datetime, time
from typing import List


@dataclass
class Strategy:
    created: datetime = datetime.now()
    description: str = None
    status: int = None
    account: int = None
    cycles: List[int] = []


@dataclass
class StrategyQuadrant:
    created: datetime = datetime.now()
    status: int = None
    strategy: int = None


@dataclass
class StrategyTime:
    created: datetime = datetime.now()
    start: time = None
    end: time = None
    type: int = None
    status: int = None
    strategy_quadrant: int = None


@dataclass
class StrategyCandle:
    created: datetime = datetime.now()
    sequence: int = None
    color: int = None
    compare: bool = False
    conditional: bool = False
    status: int = None
    strategy: int = None
