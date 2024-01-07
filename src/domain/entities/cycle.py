from dataclasses import dataclass
from typing import List


@dataclass
class Cycle:
    sequence: int = None
    status: int = None

    martingale: bool = False
    martingale_levels: int = 0
    martingale_multipler: float = 0
    martingale_reverse: bool = False
    
    serums: bool = False
    serums_levels: int = 0
    serums_percentage_profit: float = 0
    
    account: int = None
