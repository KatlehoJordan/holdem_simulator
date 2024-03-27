from typing import Union

from src.card import Card
from src.config import logger
from src.deck import Deck

N_CARDS_IN_COMMUNITY_CARDS = 5


class CommunityCards:
    def __init__(
        self,
        deck: Deck,
        card1: Union[Card, None] = None,
        card2: Union[Card, None] = None,
        card3: Union[Card, None] = None,
        card4: Union[Card, None] = None,
        card5: Union[Card, None] = None,
    ):
        self.cards = [
            card if isinstance(card, Card) else deck.draw_card()
            for card in [card1, card2, card3, card4, card5]
        ]

        card_names = [card.name for card in self.cards]
        for ith_card, card in enumerate(self.cards):
            while card_names.count(card.name) > 1:
                new_card = deck.draw_card()
                self.cards[ith_card] = new_card
                card_names[ith_card] = new_card.name

        for ith_card, card in enumerate(self.cards, start=1):
            if not isinstance(card, Card):
                raise ValueError(f"card{ith_card} must be a Card, not {type(card)}")

        self.name = "\n".join(card.name for card in self.cards)
        logger.info("%s\n", self)

    def __str__(self):
        return f"\nThe community cards are:\n{self.name}"
