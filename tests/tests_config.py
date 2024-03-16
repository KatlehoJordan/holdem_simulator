from src.card import Card
from src.config import VALID_RANKS_DICT, VALID_SUITS
from src.deck import Deck
from src.hole_cards import HoleCards
from src.rank import Rank
from src.suit import Suit

CARDS_DICT = {}

for suit in VALID_SUITS:
    for rank in VALID_RANKS_DICT.keys():
        card_name = f"{rank.upper()}_OF_{suit.upper()}"
        CARDS_DICT[card_name] = Card(Suit(suit), Rank(rank))

HOLE_CARDS_2_3_SPADES = HoleCards(
    deck=Deck(), card1=CARDS_DICT["2_OF_SPADES"], card2=CARDS_DICT["3_OF_SPADES"]
)
