from src.community_cards import CommunityCards
from src.deck import Deck
from src.flush import FLUSH_HAND_TYPE_SCORE
from tests.tests_config import CARDS_DICT, hand_type_test_builder

FLUSH_9_HI_SPADES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_SPADES"],
    card2=CARDS_DICT["5_OF_SPADES"],
    card3=CARDS_DICT["7_OF_SPADES"],
    card4=CARDS_DICT["8_OF_SPADES"],
    card5=CARDS_DICT["9_OF_SPADES"],
)

FLUSH_9_HI_DIAMONDS = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["7_OF_DIAMONDS"],
    card4=CARDS_DICT["8_OF_DIAMONDS"],
    card5=CARDS_DICT["9_OF_DIAMONDS"],
)

FLUSH_10_HI_SPADES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_SPADES"],
    card2=CARDS_DICT["5_OF_SPADES"],
    card3=CARDS_DICT["7_OF_SPADES"],
    card4=CARDS_DICT["8_OF_SPADES"],
    card5=CARDS_DICT["10_OF_SPADES"],
)

VALID_FLUSH_CASES_IN_ASCENDING_ORDER = [
    FLUSH_9_HI_SPADES,
    FLUSH_9_HI_DIAMONDS,
    FLUSH_10_HI_SPADES,
]


def test_flush():
    hand_type_test_builder(
        hand_tested="flush",
        valid_cases_in_ascending_strength=VALID_FLUSH_CASES_IN_ASCENDING_ORDER,
        expected_hand_type_score=FLUSH_HAND_TYPE_SCORE,
        valid_tie_case_1=FLUSH_9_HI_SPADES,
        valid_tie_case_2=FLUSH_9_HI_DIAMONDS,
    )
