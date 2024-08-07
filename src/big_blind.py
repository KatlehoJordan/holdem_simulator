from src.bet import Bet
from src.config import logger
from src.small_blind import SmallBlind


class BigBlind(Bet):
    def __init__(self, small_blind: SmallBlind):
        # TODO: Modify this and small blind in order to train/simulate 25/50 games, as they exist at Casino Cosmopol
        # super().__init__(small_blind.amount * 2)
        super().__init__(small_blind.amount)
        logger.info("%s\n", self)

    def __str__(self):
        return f"Big blind: {self.amount}"
