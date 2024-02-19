from src.big_blind import BigBlind
from src.players_ahead_of_you import select_random_n_players_ahead_of_you
from src.small_blind import make_random_small_blind


def main() -> None:
    small_blind = make_random_small_blind()
    big_blind = BigBlind(small_blind)
    select_random_n_players_ahead_of_you()


if __name__ == "__main__":
    main()
