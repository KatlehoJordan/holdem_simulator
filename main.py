from src.aggregate_simulations import aggregate_simulations
from src.config import logger
from src.deck import Deck
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
from src.simulate_hands import simulate_hands

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


# TODO: increase n_simulations sufficiently to get below thresholds specified in aggregate_simulations. May want to disable logging to make simulations faster.
# TODO: Run simulations for all player counts between 2 and 10.
# TODO: After getting all simulations and aggregations working, build a way to graph the results
N_SIMS = 100000  # >210 000 is likely needed to get over 1000 appearances for each hole_cards_flavor
N_PLAYERS_TO_SIM_OR_AGGREGATE = 2
ERRORS_FOR_LOW_SAMPLE_SIZE = False


# TODO: Resolve TODOs in other files
def main(
    starting_prompt: str = STARTING_PROMPT,
    continuation_prompt: str = CONTINUATION_PROMPT,
    purpose: str = "Training",
) -> None:
    clear_console()
    if purpose == "Simulating":
        logger.setLevel("WARNING")
        simulate_hands(
            n_simulations=N_SIMS, n_players_per_simulation=N_PLAYERS_TO_SIM_OR_AGGREGATE
        )
        exit()
    if purpose == "Aggregating":
        logger.setLevel("WARNING")
        aggregate_simulations(
            n_players_simulated_to_aggregate=N_PLAYERS_TO_SIM_OR_AGGREGATE,
            errors_for_low_sample_size=ERRORS_FOR_LOW_SAMPLE_SIZE,
        )
        exit()
    if purpose == "Training":
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
                deck = Deck()
                hole_cards = HoleCards(deck=deck)
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
        # TODO: (Maybe deprecated) Validate math and corrections implemented by src.scaling_constants and used in the HoleCards class
        # TODO: Get python debugger launch.json configuration working for a given file so that do not have to always bake logic into main.py


if __name__ == "__main__":
    main(purpose="Simulating")
