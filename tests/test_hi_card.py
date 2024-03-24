from src.community_cards import CommunityCards
from src.deck import Deck
from src.hi_card import HI_CARD_HAND_TYPE_SCORE
from tests.tests_config import CARDS_DICT, hand_type_test_builder

HI_CARD_9 = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["7_OF_DIAMONDS"],
    card4=CARDS_DICT["8_OF_SPADES"],
    card5=CARDS_DICT["9_OF_SPADES"],
)

HI_CARD_10_9 = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["7_OF_DIAMONDS"],
    card4=CARDS_DICT["9_OF_SPADES"],
    card5=CARDS_DICT["10_OF_SPADES"],
)

HI_CARD_10_8 = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["7_OF_DIAMONDS"],
    card4=CARDS_DICT["8_OF_SPADES"],
    card5=CARDS_DICT["10_OF_SPADES"],
)

HI_CARD_10_8_ALTERNATE = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["7_OF_DIAMONDS"],
    card4=CARDS_DICT["8_OF_DIAMONDS"],
    card5=CARDS_DICT["10_OF_SPADES"],
)

VALID_HI_CARD_CASES_IN_ASCENDING_ORDER = [
    HI_CARD_9,
    HI_CARD_10_9,
    HI_CARD_10_8,
    HI_CARD_10_8_ALTERNATE,
]


def test_hi_card():
    hand_type_test_builder(
        hand_tested="hi card",
        valid_cases_in_ascending_strength=VALID_HI_CARD_CASES_IN_ASCENDING_ORDER,
        expected_hand_type_score=HI_CARD_HAND_TYPE_SCORE,
        valid_tie_case_1=HI_CARD_10_8,
        valid_tie_case_2=HI_CARD_10_8_ALTERNATE,
    )
