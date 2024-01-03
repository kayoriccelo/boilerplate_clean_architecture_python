from datetime import datetime, time
from typing import List


class Strategy:
    created: datetime = datetime.now()
    description: str = None
    status: int = None
    account: int = None
    cycles: List[int] = []


class StrategyQuadrant:
    created: datetime = datetime.now()
    status: int = None
    strategy: int = None


class StrategyTime:
    created: datetime = datetime.now()
    start: datetime = None
    end: datetime = None
    type: int = None
    status: int = None
    strategy_quadrant: int = None


class StrategyCandle:
    created: datetime = datetime.now()
    sequence: int = None
    color: int = None
    compare: bool = False
    conditional: bool = False
    status: int = None
    strategy: int = None
