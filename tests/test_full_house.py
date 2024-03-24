from src.community_cards import CommunityCards
from src.deck import Deck
from src.full_house import FULL_HOUSE_HAND_TYPE_SCORE
from tests.tests_config import CARDS_DICT, hand_type_test_builder

FULL_HOUSE_2S_OVER_3S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["2_OF_HEARTS"],
    card3=CARDS_DICT["3_OF_CLUBS"],
    card4=CARDS_DICT["4_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

FULL_HOUSE_2S_OVER_3S_ALTERNATE = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["2_OF_HEARTS"],
    card3=CARDS_DICT["3_OF_DIAMONDS"],
    card4=CARDS_DICT["5_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_DIAMONDS"],
)

FULL_HOUSE_3S_OVER_2S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["3_OF_HEARTS"],
    card3=CARDS_DICT["3_OF_CLUBS"],
    card4=CARDS_DICT["4_OF_SPADES"],
    card5=CARDS_DICT["5_OF_DIAMONDS"],
)

FOUR_OF_A_KIND_4S_OVER_5S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["4_OF_HEARTS"],
    card3=CARDS_DICT["4_OF_CLUBS"],
    card4=CARDS_DICT["5_OF_SPADES"],
    card5=CARDS_DICT["5_OF_DIAMONDS"],
)

FOUR_OF_A_KIND_ACES_OVER_KINGS = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["ACE_OF_DIAMONDS"],
    card2=CARDS_DICT["ACE_OF_HEARTS"],
    card3=CARDS_DICT["ACE_OF_CLUBS"],
    card4=CARDS_DICT["KING_OF_SPADES"],
    card5=CARDS_DICT["KING_OF_DIAMONDS"],
)

VALID_FOUR_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH = [
    FULL_HOUSE_2S_OVER_3S,
    FULL_HOUSE_2S_OVER_3S_ALTERNATE,
    FULL_HOUSE_3S_OVER_2S,
    FOUR_OF_A_KIND_4S_OVER_5S,
    FOUR_OF_A_KIND_ACES_OVER_KINGS,
]


def test_full_house():
    hand_type_test_builder(
        hand_tested="full house",
        valid_cases_in_ascending_strength=VALID_FOUR_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=FULL_HOUSE_HAND_TYPE_SCORE,
        valid_tie_case_1=FULL_HOUSE_2S_OVER_3S,
        valid_tie_case_2=FULL_HOUSE_2S_OVER_3S_ALTERNATE,
    )
