from src.bet import Bet
from src.config import logger
from src.small_blind import SmallBlind


class BigBlind(Bet):
    def __init__(self, small_blind: SmallBlind):
        super().__init__(small_blind.amount * 2)
        logger.train("%s\n", self)

    def __str__(self):
        return f"Big blind: {self.amount}"
