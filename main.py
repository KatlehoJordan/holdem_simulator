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
            # TODO: (Maybe deprecated) Determine how to re-implement the following functions
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
            # TODO: (Maybe deprecated) Determine how to re-implement the following print statement
            # print(cutoffs, row.names = FALSE)

            user_input = input_with_escape_hatch(continuation_prompt)

    # TODO: Improve upon weightings so that the expected relative hand strengths are better (use the pytest tests). Actually, I think a better way is to simulate 1000s of games with random hands and then figure out the proportion of hands won with any given hold'em cards. Then, use that proportion to determine the relative strength of the hands. This is a Monte Carlo simulation.
    # TODO: Use deck, hole_cards, and n_players to distribute hole_cards to n_players.
    # TODO: Create community cards class that has flop, turn, and river.
    # TODO: Create player_hand class that has hole_cards and community_cards as well as best hand. Best hand is determined by the best 5 cards out of 7. Best hand can be one of the following: straight flush, four of a kind (plus kicker), full house, flush, straight, three of a kind (with 2 kickers), two pair (with 1 kicker), pair (with 3 kickers), high card (with 4 kickers).
    # Straight flush if there are 5 cards in a row of the same suit
    # Four of a kind if there are 4 cards of the same rank
    # Full house is if there are 3 cards of the same rank and 2 cards of the same rank
    # Flush is if there are 5 cards of the same suit
    # Straight is if there are 5 cards in a row
    # Three of a kind is if there are 3 cards of the same rank
    # Two pair is if there are 2 cards of the same rank and 2 cards of the same rank
    # Pair is if there are 2 cards of the same rank
    # High card is if there are no other combinations

    # TODO: (Maybe deprecated) Validate math and corrections implemented by src.scaling_constants and used in the HoleCards class


if __name__ == "__main__":
    main()
