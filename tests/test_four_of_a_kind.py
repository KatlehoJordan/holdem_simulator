from src.community_cards import CommunityCards
from src.deck import Deck
from src.four_of_a_kind import FOUR_OF_A_KIND_HAND_TYPE_SCORE
from src.player_hand import PlayerHand
from tests.tests_config import CARDS_DICT, HOLE_CARDS_2_3_SPADES

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


def test_validate_four_of_a_kind(
    four_of_a_kind_hand_type_score: int = FOUR_OF_A_KIND_HAND_TYPE_SCORE,
):
    valid_cases = [
        FOUR_OF_A_KIND_2S,
        FOUR_OF_A_KIND_2S_ALTERNATE,
        FOUR_OF_A_KIND_2S_WEAK_KICKERS,
        FOUR_OF_A_KIND_3S,
        FOUR_OF_A_KIND_4S,
        FOUR_OF_A_KIND_ACES,
    ]

    for community_cards in valid_cases:
        assert (
            PlayerHand(
                hole_cards=HOLE_CARDS_2_3_SPADES,
                community_cards=community_cards,
                # TODO: Remove type ignoring after finished implementing player_hand with all paths
            ).hand_type.hand_type_score  # type: ignore
            == four_of_a_kind_hand_type_score
        )


def test_four_of_a_kind_tie_breakers():
    community_cards_list = [
        FOUR_OF_A_KIND_2S_WEAK_KICKERS,
        FOUR_OF_A_KIND_2S,
        FOUR_OF_A_KIND_2S_ALTERNATE,
        FOUR_OF_A_KIND_3S,
        FOUR_OF_A_KIND_4S,
        FOUR_OF_A_KIND_ACES,
    ]

    hand_types = [
        PlayerHand(
            hole_cards=HOLE_CARDS_2_3_SPADES, community_cards=community_cards
        ).hand_type
        for community_cards in community_cards_list
    ]

    hand_type_scores = [hand_type.hand_type_score for hand_type in hand_types]  
    top_ranks = [hand_type.top_ranks[0] for hand_type in hand_types]

    assert all(score == hand_type_scores[0] for score in hand_type_scores)
    assert top_ranks == sorted(top_ranks)

    assert (
        hand_types[community_cards_list.index(FOUR_OF_A_KIND_2S)].top_ranks
        == hand_types[
            community_cards_list.index(FOUR_OF_A_KIND_2S_ALTERNATE)
        ].top_ranks
    )
