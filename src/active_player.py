from src.bet import Bet
from src.config import logger


class ActivePlayer:
    def __init__(self, bet: Bet):
        self.bet = bet
        logger.info(f"Player's bet: {self.bet}")
