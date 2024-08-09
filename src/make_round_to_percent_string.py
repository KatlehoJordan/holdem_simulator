from src.config import ROUND_TO_PERCENT


def make_round_to_percent_string(round_to_percent: float = ROUND_TO_PERCENT) -> str:
    round_to_percent_string = f"{round_to_percent:.0%}"
    return round_to_percent_string
