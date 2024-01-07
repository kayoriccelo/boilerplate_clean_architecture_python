from dataclasses import dataclass
from typing import List


@dataclass
class Management:
    description: str = None
    payout: float = 0
    value_investing: float = 0
    stop_loss: float = 0
    stop_win: float = 0
    time_candle: int = 0
    number_candles: int = 0
    expiration: int = 0
    status: int = None
    account: int = None
    active: List[int] = []
    cycles: List[int] = []


@dataclass
class ManagementByStrategy:
    use_candle_color_filter: bool = False
    initial_candle_color_filter: float = 0
    final_candle_color_filter: float = 0 

    use_candle_color_filter_result: bool = False
    initial_candle_color_filter_result: float = 0
    final_candle_color_filter_result: float = 0

    use_candle_similarity_filter: bool = False
    levels_candle_similarity_filter: int = 0
    initial_candle_similarity_filter: float = 0
    final_candle_similarity_filter: float = 0

    use_candle_similarity_filter_result: bool = False
    levels_candle_similarity_filter_result: int = 0
    initial_candle_similarity_filter_result: float = 0
    final_candle_similarity_filter_result: float = 0 

    use_trader_mood: bool = False
    initial_trader_mood: float = 0
    final_trader_mood: float = 0

    strategy: int = None
    management: int = None


@dataclass
class ManagementAssertiveness:
    initial: float = 0
    final: float = 0

    management: int = None
