from src.config import logger
from src.hand import Hand


def main() -> None:
    hand = Hand()
    user_input = input("Guess the pot size: ")
    # TODO: Modify logging to console for user inputs to be color coded and more visible
    if user_input.isdigit() and int(user_input) == hand.pot_size:
        logger.info("Correct!")
    else:
        logger.info(f"WRONG! The pot size is {hand.pot_size}")


if __name__ == "__main__":
    main()
