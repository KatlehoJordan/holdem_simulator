import random

VALID_SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]


class Suit:
    def __init__(self, suit: str, valid_suits: list = VALID_SUITS):
        if suit not in valid_suits:
            raise ValueError(f"Suit must be one of {valid_suits}")
        self.name = suit

    def __str__(self):
        return self.name

    @classmethod
    def select_random_suit(cls, valid_suits: list = VALID_SUITS) -> "Suit":
        return cls(random.choice(valid_suits))
