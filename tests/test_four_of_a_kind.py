from src.community_cards import CommunityCards
from src.deck import Deck
from src.four_of_a_kind import FOUR_OF_A_KIND_HAND_TYPE_SCORE
from tests.tests_config import CARDS_DICT, hand_type_test_builder

FOUR_OF_A_KIND_2S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["2_OF_HEARTS"],
    card3=CARDS_DICT["2_OF_CLUBS"],
    card4=CARDS_DICT["4_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

FOUR_OF_A_KIND_2S_ALTERNATE = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["2_OF_HEARTS"],
    card3=CARDS_DICT["2_OF_CLUBS"],
    card4=CARDS_DICT["5_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_DIAMONDS"],
)

FOUR_OF_A_KIND_2S_WEAK_KICKERS = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["2_OF_HEARTS"],
    card3=CARDS_DICT["2_OF_CLUBS"],
    card4=CARDS_DICT["4_OF_SPADES"],
    card5=CARDS_DICT["4_OF_DIAMONDS"],
)

FOUR_OF_A_KIND_3S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["3_OF_DIAMONDS"],
    card2=CARDS_DICT["3_OF_HEARTS"],
    card3=CARDS_DICT["3_OF_CLUBS"],
    card4=CARDS_DICT["4_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

FOUR_OF_A_KIND_4S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["4_OF_HEARTS"],
    card3=CARDS_DICT["4_OF_CLUBS"],
    card4=CARDS_DICT["4_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

FOUR_OF_A_KIND_ACES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["ACE_OF_DIAMONDS"],
    card2=CARDS_DICT["ACE_OF_HEARTS"],
    card3=CARDS_DICT["ACE_OF_CLUBS"],
    card4=CARDS_DICT["ACE_OF_SPADES"],
    card5=CARDS_DICT["4_OF_SPADES"],
)

VALID_FOUR_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH = [
    FOUR_OF_A_KIND_2S,
    FOUR_OF_A_KIND_2S_ALTERNATE,
    FOUR_OF_A_KIND_2S_WEAK_KICKERS,
    FOUR_OF_A_KIND_3S,
    FOUR_OF_A_KIND_4S,
    FOUR_OF_A_KIND_ACES,
]


def test_four_of_a_kind():
    hand_type_test_builder(
        hand_tested="flush",
        valid_cases_in_ascending_strength=VALID_FOUR_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=FOUR_OF_A_KIND_HAND_TYPE_SCORE,
        valid_tie_case_1=FOUR_OF_A_KIND_2S,
        valid_tie_case_2=FOUR_OF_A_KIND_2S_ALTERNATE,
    )
