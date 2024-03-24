from src.community_cards import CommunityCards
from src.deck import Deck
from src.straight import STRAIGHT_HAND_TYPE_SCORE
from tests.tests_config import CARDS_DICT, hand_type_test_builder

STRAIGHT_6_HI = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["6_OF_DIAMONDS"],
    card4=CARDS_DICT["10_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

STRAIGHT_5_HI = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["9_OF_DIAMONDS"],
    card4=CARDS_DICT["10_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

STRAIGHT_5_HI_ALTERNATE = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["9_OF_DIAMONDS"],
    card4=CARDS_DICT["10_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

VALID_STRAIGHT_CASES_IN_ASCENDING_ORDER = [
    STRAIGHT_5_HI,
    STRAIGHT_5_HI_ALTERNATE,
    STRAIGHT_6_HI,
]


def test_straight():
    hand_type_test_builder(
        hand_tested="straight",
        valid_cases_in_ascending_strength=VALID_STRAIGHT_CASES_IN_ASCENDING_ORDER,
        expected_hand_type_score=STRAIGHT_HAND_TYPE_SCORE,
        valid_tie_case_1=STRAIGHT_5_HI,
        valid_tie_case_2=STRAIGHT_5_HI_ALTERNATE,
    )
