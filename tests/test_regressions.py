from src.config import logger
from src.player_hand import PlayerHand
from tests.tests_config import (
    make_community_cards_for_testing,
    make_hole_cards_for_testing,
)

CASE_378_COMMUNITY_SPADES_FLUSH_10_HI = make_community_cards_for_testing(
    ["6_OF_SPADES", "2_OF_SPADES", "9_OF_SPADES", "10_OF_SPADES", "7_OF_SPADES"]
)

CASE_378_YOUR_HOLE_CARDS = make_hole_cards_for_testing(
    ["ACE_OF_DIAMONDS", "JACK_OF_SPADES"]
)


def test_case_378():
    logger.debug(
        "Previously, the the winning hand was identified as a 10-high flush, but this is a Jack-high flush."
    )
    player_hand = PlayerHand(
        hole_cards=CASE_378_YOUR_HOLE_CARDS,
        community_cards=CASE_378_COMMUNITY_SPADES_FLUSH_10_HI,
    )
    assert player_hand.hand_type.name == "Flush: Jack, 10, 9, 7, 6, in Spades."
