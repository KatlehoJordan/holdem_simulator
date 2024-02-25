from src.guess_functions import guess_pot_odds, guess_pot_size
from src.hand import Hand
from src.rank import VALID_RANKS_DICT, Rank


def main() -> None:
    hand = Hand()

    guess_pot_size(hand)
    guess_pot_odds(hand)
    # TODO: Start implementing classes cards, and your_hand
    # TODO: Figure out why players ahead of you is being called just because importing guess_pot_odds or guess_pot_size, but not called twice when importing both
    # TODO: Remove the next for block when done since just used for testing
    for rank in VALID_RANKS_DICT.keys():
        this_rank = Rank(rank)
        print(this_rank.rank)
        print("Final rank value is:")
        print(this_rank.final_rank_value)
        print("\n\n\n")


if __name__ == "__main__":
    main()
