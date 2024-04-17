from typing import List

from src.card import VALID_CARDS_DICT
from src.community_cards import CommunityCards
from src.config import logger
from src.deck import Deck
from src.hole_cards import HoleCards
from src.player_hand import PlayerHand

HOLE_CARDS_2_3_SPADES = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["2_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["3_OF_SPADES"],
)


def hand_type_test_builder(
    hand_tested: str,
    valid_cases_in_ascending_strength: list,
    expected_hand_type_score: int,
    valid_tie_case_1: CommunityCards,
    valid_tie_case_2: CommunityCards,
    hole_cards: HoleCards = HOLE_CARDS_2_3_SPADES,
):
    logger.debug(
        "Test that every %s tested has the correct hand type score", hand_tested
    )
    for community_cards in valid_cases_in_ascending_strength:
        assert (
            PlayerHand(
                hole_cards=hole_cards,
                community_cards=community_cards,
            ).hand_type.hand_type_score
            == expected_hand_type_score
        )

    logger.debug(
        "Test that every %s is ranked in correct order based on top rank", hand_tested
    )
    hand_types = [
        PlayerHand(hole_cards=hole_cards, community_cards=community_cards).hand_type
        for community_cards in valid_cases_in_ascending_strength
    ]
    top_ranks = [hand_type.top_ranks for hand_type in hand_types]
    assert top_ranks == sorted(top_ranks)

    logger.debug("Test that %s ties are detected", hand_tested)
    assert (
        PlayerHand(
            hole_cards=hole_cards, community_cards=valid_tie_case_1
        ).hand_type.top_ranks
        == PlayerHand(
            hole_cards=hole_cards, community_cards=valid_tie_case_2
        ).hand_type.top_ranks
    )


def make_community_cards_for_testing(list_of_5_cards: List[str]) -> CommunityCards:
    cards = [VALID_CARDS_DICT[card] for card in list_of_5_cards]
    return CommunityCards(
        deck=Deck(),
        community_card_1=cards[0],
        community_card_2=cards[1],
        community_card_3=cards[2],
        community_card_4=cards[3],
        community_card_5=cards[4],
    )


def make_hole_cards_for_testing(list_of_2_cards: List[str]) -> HoleCards:
    cards = [VALID_CARDS_DICT[card] for card in list_of_2_cards]
    return HoleCards(deck=Deck(), hole_card_1=cards[0], hole_card_2=cards[1])
