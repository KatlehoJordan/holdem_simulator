from src.make_round_to_percent_string import make_round_to_percent_string
from src.config import WIN_RATIO_STRING

ROUNDED_DOWN_TO_NEAREST_STRING = " rounded down to nearest "


def make_win_ratio_rounded_down_string(
    win_ratio_string: str = WIN_RATIO_STRING,
    rounded_down_to_nearest_string: str = ROUNDED_DOWN_TO_NEAREST_STRING,
) -> str:
    round_to_percent_string = make_round_to_percent_string()
    win_ratio_rounded_down_string = (
        f"{win_ratio_string}{rounded_down_to_nearest_string}{round_to_percent_string}"
    )
    return win_ratio_rounded_down_string
