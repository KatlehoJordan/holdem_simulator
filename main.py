from src.config import logger
from src.hand import Hand


def main() -> None:
    hand = Hand()
    logger.info(f"Pot size = {hand.pot_size}")


if __name__ == "__main__":
    main()
