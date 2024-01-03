from typing import List


class Cycle:
    sequence: int = None
    status: int = None

    martingale: bool = False
    martingale_levels: int = 0
    martingale_multipler: float = 0
    martingale_reverse: bool = False
    
    soros: bool = False
    soros_levels: int = 0
    soros_percentage_profit: float = 0
    
    account: int = None
