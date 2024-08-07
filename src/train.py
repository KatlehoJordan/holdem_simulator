from typing import Union

from src.config import logger

# TODO: Likely deprecate many imports
# from src.hole_cards import HoleCards
# from src.deck import Deck
from src.guess_functions import (  # guess_hole_cards_base_strength,; guess_hole_cards_flush_potential_bonus,; guess_hole_cards_hi_card_value,; guess_hole_cards_lo_card_value,; guess_hole_cards_pair_bonus,; guess_hole_cards_straight_potential_bonus,; guess_hole_cards_summed_value,
    clear_console,
    guess_hole_cards_win_probability,
    guess_if_should_call_bet,
    guess_pot_size,
    guess_prob_needed_to_call,
    input_with_escape_hatch_with_quit_prompt,
)
from src.guess_result import GuessResult
from src.hand import Hand
from src.players_ahead_of_you import PlayersAheadOfYou

COMMON_PROMPT = """
'y' or enter for yes
'n' or '0' for no
"""

STARTING_PROMPT = f"""
Do you want to train?
{COMMON_PROMPT}
"""

CONTINUATION_PROMPT = f"""
Do you want to train again?
{COMMON_PROMPT}
"""


# TODO: When training, tally how many times a simulation is run for each of x players, how many times you should call, the fraction of the total, the number and fraction of times you guess correctly when you should call, the number and fraction of times you guess incorrectly
def train(
    n_players_ahead_of_you: Union[int, None] = None,
    starting_prompt: str = STARTING_PROMPT,
    continuation_prompt: str = CONTINUATION_PROMPT,
):
    logger.set_logging_level("TRAINING INFO")
    user_input = input_with_escape_hatch_with_quit_prompt(starting_prompt)
    if user_input.lower() not in ["y", "", "n", "0"]:
        print("You did not enter a valid response. Please try again.")
        user_input = input_with_escape_hatch_with_quit_prompt(starting_prompt)
    elif user_input.lower() in ["q", "quit", "n", "0", "exit"]:
        print("You chose not to train. Goodbye!")
        exit()
    else:
        while user_input.lower() in ["y", ""]:
            clear_console()
            if n_players_ahead_of_you is None:
                hand = Hand()
            else:
                hand = Hand(
                    n_players_ahead_of_you=PlayersAheadOfYou(
                        n_players_ahead_of_you=n_players_ahead_of_you
                    )
                )
            hand_guess_result = guess_if_should_call_bet(hand)
            if hand_guess_result == GuessResult.INCORRECT:
                guess_pot_size(hand)
                guess_hole_cards_win_probability(hand)
                guess_prob_needed_to_call(hand)
                logger.train("\nYou guessed incorrectly the first time.\n")
                logger.train("\nNow you've seen the breakdown, so try again.\n")
                guess_if_should_call_bet(hand)
            # TODO: (Maybe deprecated) Determine how to re-implement the following functions
            # cutoffs = make_cutoffs_based_on_n_players_df()
            # guess_n_players_beat(p_hand, cutoffs)
            # deck = Deck()
            # hole_cards = HoleCards(deck=deck)
            # TODO: (Maybe deprecated) many of these guessing functions
            # guess_hole_cards_summed_value(hole_cards)
            # guess_hole_cards_hi_card_value(hole_cards)
            # guess_hole_cards_lo_card_value(hole_cards)
            # guess_hole_cards_base_strength(hole_cards)
            # guess_hole_cards_pair_bonus(hole_cards)
            # guess_hole_cards_flush_potential_bonus(hole_cards)
            # guess_hole_cards_straight_potential_bonus(hole_cards)
            # TODO: (Maybe deprecated) Determine how to re-implement the following print statement
            # print(cutoffs, row.names = FALSE)

            user_input = input_with_escape_hatch_with_quit_prompt(continuation_prompt)
