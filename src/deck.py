import random

from src.card import Card
from src.config import VALID_RANKS_DICT, VALID_SUITS, logger
from src.rank import Rank
from src.suit import Suit


class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        for suit in VALID_SUITS:
            for rank in VALID_RANKS_DICT.keys():
                self.cards.append(Card(Suit(suit), Rank(rank)))

    def show(self):
        i = 0
        for card in self.cards:
            i += 1
            print(f"Card {i} is {card}")

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def draw_card(self):
        return self.cards.pop()
