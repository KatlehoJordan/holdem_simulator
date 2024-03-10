from collections import Counter
from typing import List, Tuple

from src.card import Card
from src.community_cards import CommunityCards
from src.config import logger
from src.deck import Deck
from src.hole_cards import HoleCards


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
        self.name = ""

        try:
            self.name = validate_straight_flush(self)
        except ValueError as e:
            logger.error(e)
            raise

    def __str__(self):
        return f"{self.name}"


def validate_flush(player_hand: PlayerHand) -> Tuple[str, List[Card]]:
    suits = [card.suit.name for card in player_hand.cards]
    suit_counts = Counter(suits)
    most_common_suit = suit_counts.most_common(1)[0][0]
    if suit_counts[most_common_suit] < 5:
        raise ValueError("At least 5 cards must have the same suit.")
    flush_cards = [
        card for card in player_hand.cards if card.suit.name == most_common_suit
    ]
    suit = most_common_suit

    logger.debug(f"Flush suit is {most_common_suit}.")
    logger.debug(f"Flush cards are {', '.join(str(card) for card in flush_cards)}.")

    return suit, flush_cards


def validate_straight(list_of_cards: List[Card]) -> int:
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

    if longest_n_cards_towards_straight < 5:
        raise ValueError("Card ranks must be in ascending order and increase by 1.")

    logger.debug(f"Longest straight is {longest_n_cards_towards_straight} cards long.")
    logger.debug(f"Max card in straight is {rank_of_max_card_in_straight}.")

    return rank_of_max_card_in_straight


def validate_straight_flush(player_hand: PlayerHand) -> str:
    suit, flush_cards = validate_flush(player_hand)
    max_rank = validate_straight(flush_cards)
    name = f"Straight Flush, {max_rank} high in {suit}."
    return name
