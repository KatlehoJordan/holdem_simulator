from src.config import logger
from src.deck import Deck

# TODO: Likely deprecate many imports
from src.guess_functions import (  # guess_hole_cards_base_strength,; guess_hole_cards_flush_potential_bonus,; guess_hole_cards_hi_card_value,; guess_hole_cards_lo_card_value,; guess_hole_cards_pair_bonus,; guess_hole_cards_straight_potential_bonus,; guess_hole_cards_summed_value,
    clear_console,
    guess_hole_cards_win_probability,
    guess_pot_size,
    guess_prob_needed_to_call,
    input_with_escape_hatch_with_quit_prompt,
)
from src.hand import Hand
from src.hole_cards import HoleCards

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


# TODO: Improve upon weightings so that the expected relative hand strengths are better (use the pytest tests). Actually, I think a better way is to simulate 1000s of games with random hands and then figure out the proportion of hands won with any given hold'em cards. Then, use that proportion to determine the relative strength of the hands. This is a Monte Carlo simulation.
# TODO: Use deck, hole_cards, and n_players to distribute hole_cards to n_players.
# TODO: (Maybe deprecated) Validate math and corrections implemented by src.scaling_constants and used in the HoleCards class
def train(
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
            hand = Hand()
            guess_pot_size(hand)
            guess_prob_needed_to_call(hand)
            guess_hole_cards_win_probability(hand)
            # TODO: (Maybe deprecated) Determine how to re-implement the following functions
            # cutoffs = make_cutoffs_based_on_n_players_df()
            # guess_n_players_beat(p_hand, cutoffs)
            # deck = Deck()
            # hole_cards = HoleCards(deck=deck)
            # TODO: Likely deprecate many of these guessing functions
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
