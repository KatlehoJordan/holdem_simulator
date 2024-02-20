from src.guess_functions import guess_pot_odds, guess_pot_size
from src.hand import Hand
from src.players_ahead_of_you import simulate_and_plot


def main() -> None:
    hand = Hand()

    guess_pot_size(hand)
    guess_pot_odds(hand)
    # TODO: Start implementing classes for suits, ranks, cards, and your_hand


if __name__ == "__main__":
    main()
