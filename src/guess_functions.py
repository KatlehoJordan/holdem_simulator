import os
import sys
from typing import Callable

from click import clear

from src.config import logger
from src.guess_result import GuessResult
from src.hand import SHOULD_CALL_STRING, SHOULD_NOT_CALL_STRING, Hand
from src.hole_cards import HoleCards

STANDARD_COLOR = "\033[0m"
BLUE_COLOR = "\033[94m"
RED_COLOR = "\033[31m"
YELLOW_COLOR = "\033[93m"
TWO_NEW_LINES = "\n\n"
VISUAL_BREAK = "*" * 80


def clear_console() -> None:
    print("\033c", end="", flush=True)


def _flexible_input(message: str) -> str:
    if sys.stdin.isatty():
        txt = input(message)
    else:
        logger.train(message)
        txt = sys.stdin.readline().strip()
    return txt


def _format_yellow_notification(
    prompt: str, prompt_color: str = YELLOW_COLOR, standard_color: str = STANDARD_COLOR
) -> str:
    return prompt_color + prompt + standard_color


def _start_pad(message: str, pad: str = TWO_NEW_LINES) -> str:
    return pad + message


def _end_pad(message: str, pad: str = TWO_NEW_LINES) -> str:
    return message + pad


def _start_and_end_pad(message: str, pad: str = TWO_NEW_LINES) -> str:
    return _start_pad(_end_pad(message, pad), pad)


def _handle_quit(user_input: str, pad: str = TWO_NEW_LINES) -> str:
    if user_input.lower() in ["q", "quit"]:
        message = _start_pad("You chose to quit. Goodbye!", pad)
        message = _end_pad(message, pad)
        logger.train(message)
        exit()
    return user_input


def _reset_color_with_end_pad(
    message: str, standard_color: str = STANDARD_COLOR
) -> str:
    return _end_pad(message + standard_color)


def _reset_color_with_both_side_padding(message: str) -> str:
    message = _start_pad(message)
    return _reset_color_with_end_pad(message)


def _format_yellow_prompt(prompt: str) -> str:
    return _format_yellow_notification(prompt) + ":"


def input_with_escape_hatch_with_quit_prompt(
    message: str, visual_break: str = VISUAL_BREAK
) -> str:
    quit_at_any_time = _get_quit_message(visual_break)
    user_input = _flexible_input(quit_at_any_time + message + "\n> ")
    return _handle_quit(user_input)


def _get_quit_message(visual_break: str = VISUAL_BREAK):
    quit_message = "Press 'q' or 'quit' to quit"
    padded_message = _start_and_end_pad(quit_message)
    quit_at_any_time = _end_pad(visual_break + padded_message + visual_break)
    return quit_at_any_time


def _input_with_escape_hatch_without_quit_prompt(message: str) -> str:
    user_input = _flexible_input(_format_yellow_notification(message) + "\n> ")
    return _handle_quit(user_input)


def _correct_guess(correct_color: str = BLUE_COLOR) -> None:
    message = _reset_color_with_both_side_padding(correct_color + "Correct!")
    logger.train(message)


def _wrong_guess(incorrect_color: str = RED_COLOR) -> None:
    message = _reset_color_with_both_side_padding(incorrect_color + "WRONG!")
    logger.train(message)


def _guess_and_check(
    show_info_function: Callable[[], None],
    guess_prompt: str,
    actual_value: str,
    show_answer_function: Callable[[], None],
) -> GuessResult:
    logger.train(_get_quit_message())
    show_info_function()
    user_input = _input_with_escape_hatch_without_quit_prompt(guess_prompt)
    logger.train(f"User input was: {user_input}")
    if str(user_input) == str(actual_value):
        _correct_guess()
        guess_result = GuessResult.CORRECT
    else:
        _wrong_guess()
        guess_result = GuessResult.INCORRECT
    show_answer_function()
    _input_with_escape_hatch_without_quit_prompt("\nPress enter/return to proceed")
    clear_console()
    return guess_result


def guess_if_should_call_bet(
    hand: Hand,
    should_call_string: str = SHOULD_CALL_STRING,
    should_not_call_string: str = SHOULD_NOT_CALL_STRING,
) -> GuessResult:
    return _guess_and_check(
        hand.show_info_for_finding_if_should_call,
        f"Should you call the bet? '{should_call_string}' for true, '{should_not_call_string}' for false",
        hand.should_call,
        hand.show_if_should_call,
    )


def guess_pot_size(hand: Hand) -> None:
    _guess_and_check(
        hand.show_bets,
        "Guess pot size",
        str(hand.pot_size),
        hand.show_pot_size,
    )


def guess_hole_cards_win_probability(hand: Hand) -> None:
    _guess_and_check(
        hand.show_your_hole_cards,
        "Guess hole cards' win probability",
        hand.hole_cards_prob_to_win,
        hand.show_prob_to_win,
    )


# TODO: Modify this function to be more appropriate for heads-up situations as big blind and small blind
def guess_prob_needed_to_call(hand: Hand) -> None:
    _guess_and_check(
        hand.show_info_for_finding_prob_needed_to_call,
        "Guess win probability needed to call",
        hand.prob_needed_to_call,
        hand.show_prob_needed_to_call,
    )


# TODO: Likely deprecate all below
# def guess_hole_cards_summed_value(hole_cards: HoleCards) -> None:
#     _guess_and_check(
#         "Guess hole cards' summed value",
#         str(hole_cards.summed_value),
#         hole_cards.show_summed_value,
#     )


# def guess_hole_cards_hi_card_value(hole_cards: HoleCards) -> None:
#     _guess_and_check(
#         "Guess hole cards' hi card value",
#         str(hole_cards.hi_card.value),
#         hole_cards.show_hi_card_value,
#     )


# def guess_hole_cards_lo_card_value(hole_cards: HoleCards) -> None:
#     _guess_and_check(
#         "Guess hole cards' lo card value",
#         str(hole_cards.lo_card.value),
#         hole_cards.show_lo_card_value,
#     )


# def guess_hole_cards_base_strength(hole_cards: HoleCards) -> None:
#     _guess_and_check(
#         "Guess hole cards' base strength",
#         str(hole_cards.base_strength),
#         hole_cards.show_base_strength,
#     )


# def guess_hole_cards_pair_bonus(hole_cards: HoleCards) -> None:
#     _guess_and_check(
#         "Guess hole cards' pair bonus",
#         str(hole_cards.pocket_pair_bonus),
#         hole_cards.show_pair_bonus,
#     )


# def guess_hole_cards_flush_potential_bonus(hole_cards: HoleCards) -> None:
#     _guess_and_check(
#         "Guess hole cards' flush potential bonus",
#         str(hole_cards.flush_potential_bonus),
#         hole_cards.show_flush_potential_bonus,
#     )


# def guess_hole_cards_straight_potential_bonus(hole_cards: HoleCards) -> None:
#     _guess_and_check(
#         "Guess hole cards' straight potential bonus",
#         str(hole_cards.straight_potential_bonus),
#         hole_cards.show_straight_potential_bonus,
#     )
