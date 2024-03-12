from collections import Counter
from typing import List, Tuple

from attr import validate

from src.card import Card
from src.community_cards import CommunityCards
from src.config import logger
from src.hole_cards import HoleCards
from src.straight_flush import StraightFlush


# TODO: Will want to extend this so that has some way of capturing hand type == straight flush, and that straight_flush will have attributes: 1) hand_type_score == 8 and 2) high card raw rank value. Next hand type would be == four-of-a-kind with attributes 1) hand_type_score == 7, 2) the raw rank value of the four-of-a-kind and 3) the raw rank value of the kicker. Next hand type would be == full house with attributes 1) hand_type_score == 6, 2) the raw rank value of the three-of-a-kind and 3) the raw rank value of the pair. Next hand type would be == flush with attributes 1) hand_type_score == 5 and 2) the raw rank value of the highest card in the flush, 3) the next highest card in the flush, 4) the third highest card in the flush, 5) the fourth highest card in the flush, and 6) the lowest card in the flush. Next hand type would be == straight with attributes 1) hand_type_score == 4 and 2) the raw rank value of the highest card in the straight. Next hand type would be == three-of-a-kind with attributes 1) hand_type_score == 3, 2) the raw rank value of the three-of-a-kind, 3) the raw rank value of the highest kicker, and 4) the raw rank value of the lowest kicker. Next hand type would be == two-pair with attributes 1) hand_type_score == 2, 2) the raw rank value of the highest pair, 3) the raw rank value of the lowest pair, and 4) the raw rank value of the kicker. Next hand type would be == pair with attributes 1) hand_type_score == 1, 2) the raw rank value of the pair, 3) the raw rank value of the highest kicker, 4) the raw rank value of the second highest kicker, and 5) the raw rank value of the lowest kicker. Next hand type would be == high card with attributes 1) hand_type_score == 0, 2) the raw rank value of the high card, 3) the raw rank value of the second highest card, 4) the raw rank value of the third highest card, 5) the raw rank value of the fourth highest card, and 6) the raw rank value of the lowest card.
class PlayerHand:
    def __init__(self, hole_cards: HoleCards, community_cards: CommunityCards):
        if not isinstance(hole_cards, HoleCards):
            raise ValueError(f"hole_cards must be a HoleCards, not {type(hole_cards)}")
        if not isinstance(community_cards, CommunityCards):
            raise ValueError(
                f"community_cards must be a CommunityCards, not {type(community_cards)}"
            )

        self.cards = [hole_cards.hi_card, hole_cards.lo_card] + community_cards.cards

        # TODO: If validate_straight_flush is true, then capture hand type == straight flush, and that straight_flush will have attributes: 1) hand_type_score == 8 and 2) high card raw rank value.
        straight_flush_found, max_rank, name = validate_straight_flush(self)
        if straight_flush_found:
            self.hand_type = StraightFlush(high_card_raw_rank_value=max_rank, name=name)
        else:
            # TODO: populate with next hand type
            self.hand_type = None
            pass

    def __str__(self):
        return f"{self.hand_type}"


def validate_flush(player_hand: PlayerHand) -> Tuple[bool, str, List[Card], str]:
    suits = [card.suit.name for card in player_hand.cards]
    suit_counts = Counter(suits)
    most_common_suit = suit_counts.most_common(1)[0][0]

    flush_cards = [
        card for card in player_hand.cards if card.suit.name == most_common_suit
    ]

    logger.debug(f"Flush suit is {most_common_suit}.")
    logger.debug(f"Flush cards are {', '.join(str(card) for card in flush_cards)}.")

    if suit_counts[most_common_suit] < 5:
        flush_found = False
    else:
        flush_found = True
    sorted_raw_rank_values = sorted(
        card.rank.raw_rank_value for card in player_hand.cards
    )
    name = f"Flush, {sorted_raw_rank_values[-1]}, {sorted_raw_rank_values[-2]}, {sorted_raw_rank_values[-3]}, {sorted_raw_rank_values[-4]}, {sorted_raw_rank_values[-5]}, in {most_common_suit}."

    return flush_found, most_common_suit, flush_cards, name


def validate_straight(list_of_cards: List[Card]) -> Tuple[bool, int, str]:
    sorted_raw_rank_values = sorted(card.rank.raw_rank_value for card in list_of_cards)

    if max(sorted_raw_rank_values) == 14:
        logger.debug("Ace can be high or low, so adding a low ace to the list.")
        sorted_raw_rank_values = [1] + sorted_raw_rank_values

    longest_n_cards_towards_straight = current_n_cards_towards_a_straight = 1
    rank_of_max_card_in_straight = sorted_raw_rank_values[0]
    for i in range(1, len(sorted_raw_rank_values)):
        if sorted_raw_rank_values[i] == sorted_raw_rank_values[i - 1] + 1:
            current_n_cards_towards_a_straight += 1
            if current_n_cards_towards_a_straight > longest_n_cards_towards_straight:
                longest_n_cards_towards_straight = current_n_cards_towards_a_straight
                rank_of_max_card_in_straight = sorted_raw_rank_values[i]
        else:
            current_n_cards_towards_a_straight = 1

    logger.debug(f"Longest straight is {longest_n_cards_towards_straight} cards long.")
    logger.debug(f"Max card in straight is {rank_of_max_card_in_straight}.")

    if longest_n_cards_towards_straight < 5:
        straight_found = False
    else:
        straight_found = True
    name = f"Straight, {rank_of_max_card_in_straight} high."

    return straight_found, rank_of_max_card_in_straight, name


def validate_straight_flush(player_hand: PlayerHand) -> Tuple[bool, int, str]:
    flush_found, suit, flush_cards, _ = validate_flush(player_hand)
    straight_found, rank_of_max_card_in_straight_flush, _ = validate_straight(
        flush_cards
    )

    if flush_found and straight_found:
        straight_flush_found = True
    else:
        straight_flush_found = False

    name = f"Straight Flush, {rank_of_max_card_in_straight_flush} high in {suit}."
    return straight_flush_found, rank_of_max_card_in_straight_flush, name
