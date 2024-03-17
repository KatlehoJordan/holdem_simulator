from src.community_cards import CommunityCards
from src.deck import Deck
from src.player_hand import PlayerHand
from src.straight_flush import STRAIGHT_FLUSH_HAND_TYPE_SCORE
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

# TODO: pull out the test cases written for the test_straight_flush file, and put them with the more appropriate file.
# FLUSH_9_HI_SPADES = CommunityCards(
#     deck=Deck(),
#     card1=CARDS_DICT["4_OF_SPADES"],
#     card2=CARDS_DICT["5_OF_SPADES"],
#     card3=CARDS_DICT["7_OF_SPADES"],
#     card4=CARDS_DICT["8_OF_SPADES"],
#     card5=CARDS_DICT["9_OF_SPADES"],
# )

# STRAIGHT_5_HI = CommunityCards(
#     deck=Deck(),
#     card1=CARDS_DICT["4_OF_SPADES"],
#     card2=CARDS_DICT["5_OF_DIAMONDS"],
#     card3=CARDS_DICT["9_OF_SPADES"],
#     card4=CARDS_DICT["10_OF_SPADES"],
#     card5=CARDS_DICT["ACE_OF_SPADES"],
# )

# HI_CARD_9 = CommunityCards(
#     deck=Deck(),
#     card1=CARDS_DICT["4_OF_DIAMONDS"],
#     card2=CARDS_DICT["5_OF_DIAMONDS"],
#     card3=CARDS_DICT["7_OF_CLUBS"],
#     card4=CARDS_DICT["8_OF_SPADES"],
#     card5=CARDS_DICT["9_OF_SPADES"],
# )


# TODO: See if can refactor this test function and the one used in test_four_of_a_kind.py to be more DRY. Will try to do this after having pulled out the flush, straight, and high card test cases into their own files.
def test_straight_flush_hand_type_score(
    straight_flush_hand_type_score: int = STRAIGHT_FLUSH_HAND_TYPE_SCORE,
):
    valid_cases = [
        STRAIGHT_FLUSH_5_HI_SPADES,
        STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE,
        STRAIGHT_FLUSH_7_HI_SPADES,
        STRAIGHT_FLUSH_9_HI_SPADES,
        STRAIGHT_FLUSH_ACE_HI_SPADES,
    ]

    for community_cards in valid_cases:
        assert (
            PlayerHand(
                hole_cards=HOLE_CARDS_2_3_SPADES,
                community_cards=community_cards,
                # TODO: Remove type ignoring after finished implementing player_hand with all paths
            ).hand_type.hand_type_score  # type: ignore
            == straight_flush_hand_type_score
        )

    # TODO: implement this here, or as a separate test, with specific expected values instead of not equal logic, and only implement after all other hand types are implemented
    # invalid_cases = [
    #     FLUSH_9_HI_SPADES,
    #     STRAIGHT_5_HI,
    #     HI_CARD_9,
    # ]

    # for community_cards in invalid_cases:
    #     assert (
    #         PlayerHand(
    #             hole_cards=HOLE_CARDS_2_3_SPADES, community_cards=community_cards
    #         ).hand_type.hand_type_score
    #         != straight_flush_hand_type_score
    #     )


def test_straight_flush_tie_breakers():
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
    top_ranks = [hand_type.top_ranks[0] for hand_type in hand_types]  # type: ignore

    assert all(score == hand_type_scores[0] for score in hand_type_scores)
    assert top_ranks == sorted(top_ranks)

    assert (
        hand_types[community_cards_list.index(STRAIGHT_FLUSH_5_HI_SPADES)].top_ranks  # type: ignore
        == hand_types[
            community_cards_list.index(STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE)
        ].top_ranks  # type: ignore
    )
