from src.guess_functions import guess_pot_odds, guess_pot_size
from src.hand import Hand
from src.rank import VALID_RANKS_DICT, Rank


def main() -> None:
    hand = Hand()

    guess_pot_size(hand)
    guess_pot_odds(hand)
    # TODO: Use the HoleCards class to rebuild the interactive game I previously made in R
    # TODO: Implement tests that ensure known hands have expected relative ranks, as previously implemented in R
    # TODO: Figure out why players ahead of you is being called just because importing guess_pot_odds or guess_pot_size, but not called twice when importing both
    # TODO: Remove the next for block when done since just used for testing
    # TODO: Validate math and corrections implemented by src.scaling_constants and used in the HoleCards class
    for rank in VALID_RANKS_DICT.keys():
        this_rank = Rank(rank)
        print(this_rank)


if __name__ == "__main__":
    main()
