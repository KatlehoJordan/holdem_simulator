from src.community_cards import CommunityCards
from src.deck import Deck
from src.straight_flush import STRAIGHT_FLUSH_HAND_TYPE_SCORE
from tests.tests_config import CARDS_DICT, hand_type_test_builder

STRAIGHT_FLUSH_5_HI_SPADES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_SPADES"],
    card2=CARDS_DICT["5_OF_SPADES"],
    card3=CARDS_DICT["9_OF_SPADES"],
    card4=CARDS_DICT["10_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_SPADES"],
    card2=CARDS_DICT["5_OF_SPADES"],
    card3=CARDS_DICT["8_OF_SPADES"],
    card4=CARDS_DICT["9_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

STRAIGHT_FLUSH_7_HI_SPADES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_SPADES"],
    card2=CARDS_DICT["5_OF_SPADES"],
    card3=CARDS_DICT["6_OF_SPADES"],
    card4=CARDS_DICT["7_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

STRAIGHT_FLUSH_9_HI_SPADES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["5_OF_SPADES"],
    card2=CARDS_DICT["6_OF_SPADES"],
    card3=CARDS_DICT["7_OF_SPADES"],
    card4=CARDS_DICT["8_OF_SPADES"],
    card5=CARDS_DICT["9_OF_SPADES"],
)

STRAIGHT_FLUSH_ACE_HI_SPADES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["10_OF_SPADES"],
    card2=CARDS_DICT["JACK_OF_SPADES"],
    card3=CARDS_DICT["QUEEN_OF_SPADES"],
    card4=CARDS_DICT["KING_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

VALID_STRAIGHT_FLUSH_CASES_IN_ASCENDING_STRENGTH = [
    STRAIGHT_FLUSH_5_HI_SPADES,
    STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE,
    STRAIGHT_FLUSH_7_HI_SPADES,
    STRAIGHT_FLUSH_9_HI_SPADES,
    STRAIGHT_FLUSH_ACE_HI_SPADES,
]


def test_straight_flush():
    hand_type_test_builder(
        hand_tested="straight flush",
        valid_cases_in_ascending_strength=VALID_STRAIGHT_FLUSH_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=STRAIGHT_FLUSH_HAND_TYPE_SCORE,
        valid_tie_case_1=STRAIGHT_FLUSH_5_HI_SPADES,
        valid_tie_case_2=STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE,
    )
