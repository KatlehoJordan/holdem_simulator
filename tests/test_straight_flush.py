from src.community_cards import CommunityCards
from src.deck import Deck
from src.hole_cards import HoleCards
from src.player_hand import PlayerHand
from src.straight_flush import StraightFlush
from tests.tests_config import CARDS_DICT, HOLE_CARDS_2_3_SPADES

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

STRAIGHT_5_HI = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_SPADES"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["9_OF_SPADES"],
    card4=CARDS_DICT["10_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

FLUSH_9_HI_SPADES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_SPADES"],
    card2=CARDS_DICT["5_OF_SPADES"],
    card3=CARDS_DICT["7_OF_SPADES"],
    card4=CARDS_DICT["8_OF_SPADES"],
    card5=CARDS_DICT["9_OF_SPADES"],
)

HI_CARD_9 = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["7_OF_CLUBS"],
    card4=CARDS_DICT["8_OF_SPADES"],
    card5=CARDS_DICT["9_OF_SPADES"],
)


def test_validate_straight_flush():
    test_cases = [
        (STRAIGHT_FLUSH_5_HI_SPADES, True),
        (STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE, True),
        (STRAIGHT_FLUSH_7_HI_SPADES, True),
        (STRAIGHT_FLUSH_9_HI_SPADES, True),
        (STRAIGHT_FLUSH_ACE_HI_SPADES, True),
        (STRAIGHT_5_HI, False),
        (FLUSH_9_HI_SPADES, False),
        (HI_CARD_9, False),
    ]

    for community_cards, expected in test_cases:
        assert (
            isinstance(
                PlayerHand(
                    hole_cards=HOLE_CARDS_2_3_SPADES, community_cards=community_cards
                ).hand_type,
                StraightFlush,
            )
            is expected
        )


def test_straight_flush_winners():
    community_cards_list = [
        STRAIGHT_FLUSH_5_HI_SPADES,
        STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE,
        STRAIGHT_FLUSH_7_HI_SPADES,
        STRAIGHT_FLUSH_9_HI_SPADES,
        STRAIGHT_FLUSH_ACE_HI_SPADES,
    ]

    hand_types = [
        PlayerHand(
            hole_cards=HOLE_CARDS_2_3_SPADES, community_cards=community_cards
        ).hand_type
        for community_cards in community_cards_list
    ]

    # TODO: Remove type ignoring after finished implementing player_hand with all paths
    hand_type_scores = [hand_type.hand_type_score for hand_type in hand_types]  # type: ignore
    top_ranks = [hand_type.top_ranks[~0] for hand_type in hand_types]  # type: ignore

    assert all(score == hand_type_scores[0] for score in hand_type_scores)
    assert top_ranks == sorted(top_ranks)

    assert (
        hand_types[community_cards_list.index(STRAIGHT_FLUSH_5_HI_SPADES)].top_ranks  # type: ignore
        == hand_types[
            community_cards_list.index(STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE)
        ].top_ranks  # type: ignore
    )
