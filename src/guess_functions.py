from typing import Callable

from src.config import logger
from src.hand import Hand


def correct_guess():
    logger.info("\n\n\033[92mCorrect!\033[0m\n\n")


def wrong_guess():
    logger.info(f"\n\n\033[91mWRONG!\033[0m\n\n")


def guess_and_check(
    guess_prompt: str, actual_value: str, show_value_func: Callable[[], None]
):
    user_input = input(guess_prompt)
    if str(user_input) == str(actual_value):
        correct_guess()
    else:
        wrong_guess()
    show_value_func()


def guess_pot_size(hand: Hand) -> None:
    guess_and_check("Guess pot size: ", str(hand.pot_size), hand.show_pot_size)


def guess_pot_odds(hand: Hand) -> None:
    guess_and_check("Guess pot odds: ", hand.pot_odds, hand.show_pot_odds)
