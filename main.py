from src.config import logger
from src.hand import Hand


def main() -> None:
    hand = Hand()
    user_input = input("Guess the pot size: ")
    # TODO: Modify logging to console for user inputs to be color coded and more visible
    if user_input.isdigit() and int(user_input) == hand.pot_size:
        logger.info("Correct!")
    else:
        logger.info(f"WRONG!")
    hand.show_pot_size()
    user_input = input("Guess the pot odds: ")
    if user_input == hand.pot_odds:
        logger.info("Correct!")
    else:
        logger.info(f"WRONG!")
    hand.show_pot_odds()


if __name__ == "__main__":
    main()
