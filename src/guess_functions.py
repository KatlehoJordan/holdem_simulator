import os
import sys
from typing import Callable

from click import clear

from src.config import logger
from src.hand import Hand
from src.hole_cards import HoleCards

STANDARD_COLOR = "\033[0m"
BLUE_COLOR = "\033[94m"
RED_COLOR = "\033[31m"
YELLOW_COLOR = "\033[93m"


def clear_console() -> None:
    print("\033c", end="", flush=True)


def _flexible_input(message: str) -> str:
    if sys.stdin.isatty():
        txt = input(message)
    else:
        logger.train(message)
        txt = sys.stdin.readline().strip()
    return txt


def _handle_quit(user_input: str) -> str:
    if user_input.lower() in ["q", "quit"]:
        logger.train("\n\nYou chose to quit. Goodbye!\n\n")
        exit()
    return user_input


def _format_yellow_notification(prompt: str) -> str:
    return YELLOW_COLOR + prompt + STANDARD_COLOR


def _format_yellow_prompt(prompt: str) -> str:
    return _format_yellow_notification(prompt) + ": "


def input_with_escape_hatch_with_quit_prompt(message: str) -> str:
    quit_at_any_time = (
        "*" * 80 + "\n('q' or 'quit' at any time to quit)\n" + "*" * 80 + "\n\n"
    )
    user_input = _flexible_input(quit_at_any_time + message + "\n> ")
    return _handle_quit(user_input)


def _input_with_escape_hatch_without_quit_prompt(message: str) -> str:
    user_input = _flexible_input(_format_yellow_notification(message) + "\n> ")
    return _handle_quit(user_input)


def _correct_guess():
    logger.train("\n\n" + BLUE_COLOR + "Correct!" + STANDARD_COLOR + "\n\n")


def _wrong_guess():
    logger.train(f"\n\n" + RED_COLOR + "WRONG!" + STANDARD_COLOR + "\n\n")


def _guess_and_check_common(
    guess_prompt: str,
    actual_value: str,
    show_value_func: Callable[[], None],
    first_guess: bool,
):
    if first_guess:
        user_input = _input_with_escape_hatch_without_quit_prompt(
            _format_yellow_prompt(guess_prompt)
        )
    else:
        user_input = input_with_escape_hatch_with_quit_prompt(
            _format_yellow_prompt(guess_prompt)
        )
    if str(user_input) == str(actual_value):
        _correct_guess()
    else:
        _wrong_guess()
    show_value_func()
    _input_with_escape_hatch_without_quit_prompt("\nPress enter/return to proceed")
    clear_console()


def _first_guess_and_check(
    guess_prompt: str, actual_value: str, show_value_func: Callable[[], None]
):
    _guess_and_check_common(
        guess_prompt, actual_value, show_value_func, first_guess=True
    )


def _typical_guess_and_check(
    guess_prompt: str, actual_value: str, show_value_func: Callable[[], None]
):
    _guess_and_check_common(
        guess_prompt, actual_value, show_value_func, first_guess=False
    )


def guess_pot_size(hand: Hand) -> None:
    _first_guess_and_check("Guess pot size", str(hand.pot_size), hand.show_pot_size)


def guess_pot_odds(hand: Hand) -> None:
    _typical_guess_and_check("Guess pot odds", hand.pot_odds, hand.show_pot_odds)


def guess_hole_cards_summed_value(hole_cards: HoleCards) -> None:
    _typical_guess_and_check(
        "Guess hole cards' summed value",
        str(hole_cards.summed_value),
        hole_cards.show_summed_value,
    )


def guess_hole_cards_hi_card_value(hole_cards: HoleCards) -> None:
    _typical_guess_and_check(
        "Guess hole cards' hi card value",
        str(hole_cards.hi_card.value),
        hole_cards.show_hi_card_value,
    )


def guess_hole_cards_lo_card_value(hole_cards: HoleCards) -> None:
    _typical_guess_and_check(
        "Guess hole cards' lo card value",
        str(hole_cards.lo_card.value),
        hole_cards.show_lo_card_value,
    )


def guess_hole_cards_base_strength(hole_cards: HoleCards) -> None:
    _typical_guess_and_check(
        "Guess hole cards' base strength",
        str(hole_cards.base_strength),
        hole_cards.show_base_strength,
    )


def guess_hole_cards_pair_bonus(hole_cards: HoleCards) -> None:
    _typical_guess_and_check(
        "Guess hole cards' pair bonus",
        str(hole_cards.pocket_pair_bonus),
        hole_cards.show_pair_bonus,
    )


def guess_hole_cards_flush_potential_bonus(hole_cards: HoleCards) -> None:
    _typical_guess_and_check(
        "Guess hole cards' flush potential bonus",
        str(hole_cards.flush_potential_bonus),
        hole_cards.show_flush_potential_bonus,
    )


def guess_hole_cards_straight_potential_bonus(hole_cards: HoleCards) -> None:
    _typical_guess_and_check(
        "Guess hole cards' straight potential bonus",
        str(hole_cards.straight_potential_bonus),
        hole_cards.show_straight_potential_bonus,
    )
