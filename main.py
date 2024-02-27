from click import clear

from src.guess_functions import (
    clear_console,
    guess_hole_cards_base_strength,
    guess_hole_cards_flush_potential_bonus,
    guess_hole_cards_hi_card_value,
    guess_hole_cards_lo_card_value,
    guess_hole_cards_pair_bonus,
    guess_hole_cards_straight_potential_bonus,
    guess_hole_cards_summed_value,
    guess_pot_odds,
    guess_pot_size,
    input_with_escape_hatch,
)
from src.hand import Hand
from src.hole_cards import HoleCards
from src.rank import VALID_RANKS_DICT, Rank

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


def main(
    starting_prompt: str = STARTING_PROMPT,
    continuation_prompt: str = CONTINUATION_PROMPT,
) -> None:
    clear_console()
    user_input = input_with_escape_hatch(starting_prompt)
    if user_input.lower() not in ["y", "", "n", "0"]:
        print("You did not enter a valid response. Please try again.")
        user_input = input_with_escape_hatch(starting_prompt)
    elif user_input.lower() in ["q", "quit", "n", "0", "exit"]:
        print("You chose not to train. Goodbye!")
        exit()
    else:
        while user_input.lower() in ["y", ""]:
            clear_console()
            hand = Hand()
            guess_pot_size(hand)
            guess_pot_odds(hand)
            # TODO: Determine how to re-implement the following functions
            # cutoffs = make_cutoffs_based_on_n_players_df()
            # guess_n_players_beat(p_hand, cutoffs)
            hole_cards = HoleCards()
            guess_hole_cards_summed_value(hole_cards)
            guess_hole_cards_hi_card_value(hole_cards)
            guess_hole_cards_lo_card_value(hole_cards)
            guess_hole_cards_base_strength(hole_cards)
            guess_hole_cards_pair_bonus(hole_cards)
            guess_hole_cards_flush_potential_bonus(hole_cards)
            guess_hole_cards_straight_potential_bonus(hole_cards)
            # TODO: Determine how to re-implement the following print statement
            # print(cutoffs, row.names = FALSE)

            user_input = input_with_escape_hatch(continuation_prompt)

    # TODO: Check if Queens are coming out to 29 or 30 and compare to R results
    # TODO: Implement tests that ensure known hands have expected relative ranks, as previously implemented in R
    # TODO: Validate math and corrections implemented by src.scaling_constants and used in the HoleCards class


if __name__ == "__main__":
    main()
