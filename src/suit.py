VALID_SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]

class Suit:
    def __init__(self, suit: str):
        if suit not in VALID_SUITS:
            raise ValueError(f"Suit must be one of {VALID_SUITS}")
        self.suit = suit

    def __str__(self):
        return self.suit
