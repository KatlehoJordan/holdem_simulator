from src.community_cards import CommunityCards
from src.config import logger
from src.flush import validate_flush
from src.four_of_a_kind import validate_four_of_a_kind
from src.full_house import validate_full_house
from src.hand_type import HandType
from src.hi_card import validate_hi_card
from src.hole_cards import HoleCards
from src.pair import validate_pair
from src.straight import validate_straight
from src.straight_flush import validate_straight_flush
from src.three_of_a_kind import validate_three_of_a_kind
from src.two_pair import validate_two_pair

FIRST_PLAYER_WINS_STRING = "First player wins."
SECOND_PLAYER_WINS_STRING = "Second player wins."
PLAYERS_TIE_STRING = "Players tie."


class PlayerHand:
    def __init__(self, hole_cards: HoleCards, community_cards: CommunityCards):
        if not isinstance(hole_cards, HoleCards):
            raise ValueError(
                f"hole_cards must be a HoleCards type, not {type(hole_cards)}"
            )
        if not isinstance(community_cards, CommunityCards):
            raise ValueError(
                f"community_cards must be a CommunityCards type, not {type(community_cards)}"
            )

        self.cards = [hole_cards.hi_card, hole_cards.lo_card] + community_cards.cards

        if len(self.cards) != len(set(self.cards)):
            raise ValueError("There are non-unique cards in the hand.")

        if len(self.cards) != 7:
            raise ValueError("There must be 7 cards in the hand.")

        validation_functions = [
            validate_straight_flush,
            validate_four_of_a_kind,
            validate_full_house,
            validate_flush,
            validate_straight,
            validate_three_of_a_kind,
            validate_two_pair,
            validate_pair,
            validate_hi_card,
        ]

        for validate in validation_functions:
            hand_found, hand_type_score, top_ranks, name = validate(self.cards)
            print("hand_found:", hand_found)
            print("hand name:", name)
            if hand_found:
                self.hand_type = HandType(
                    hand_type_score=hand_type_score, top_ranks=top_ranks, name=name
                )
                break

    def __str__(self):
        return f"{self.hand_type}"


def compare_player_hands(
    community_cards: CommunityCards,
    hole_cards_1: HoleCards,
    hole_cards_2: HoleCards,
    first_player_wins_string: str = FIRST_PLAYER_WINS_STRING,
    second_player_wins_string: str = SECOND_PLAYER_WINS_STRING,
    players_tie_string: str = PLAYERS_TIE_STRING,
) -> str:
    player_hand_1 = PlayerHand(hole_cards=hole_cards_1, community_cards=community_cards)
    player_hand_2 = PlayerHand(hole_cards=hole_cards_2, community_cards=community_cards)
    if (
        player_hand_1.hand_type.hand_type_score
        > player_hand_2.hand_type.hand_type_score
    ):
        return first_player_wins_string
    elif (
        player_hand_1.hand_type.hand_type_score
        < player_hand_2.hand_type.hand_type_score
    ):
        return second_player_wins_string
    else:
        for rank_1, rank_2 in zip(
            player_hand_1.hand_type.top_ranks, player_hand_2.hand_type.top_ranks
        ):
            if rank_1 > rank_2:
                return first_player_wins_string
            elif rank_1 < rank_2:
                return second_player_wins_string
        return players_tie_string


def assert_winner_regardless_of_order(
    community_cards: CommunityCards,
    winning_hole_cards: HoleCards,
    losing_hole_cards: HoleCards,
):
    logger.debug(
        "Test that the correct hand is determined as winner regardless of order"
    )
    assert (
        compare_player_hands(
            community_cards=community_cards,
            hole_cards_1=winning_hole_cards,
            hole_cards_2=losing_hole_cards,
        )
        == FIRST_PLAYER_WINS_STRING
    )
    assert (
        compare_player_hands(
            community_cards=community_cards,
            hole_cards_1=losing_hole_cards,
            hole_cards_2=winning_hole_cards,
        )
        == SECOND_PLAYER_WINS_STRING
    )


def assert_tie_regardless_of_order(
    community_cards: CommunityCards,
    hole_cards_1: HoleCards,
    hole_cards_2: HoleCards,
):
    logger.debug("Test that ties are determined as a tie regardless of order")
    assert (
        compare_player_hands(
            community_cards=community_cards,
            hole_cards_1=hole_cards_1,
            hole_cards_2=hole_cards_2,
        )
        == PLAYERS_TIE_STRING
    )
    assert (
        compare_player_hands(
            community_cards=community_cards,
            hole_cards_1=hole_cards_2,
            hole_cards_2=hole_cards_1,
        )
        == PLAYERS_TIE_STRING
    )
