from collections import Counter
from typing import List, Tuple

from src.card import Card
from src.config import logger


# TODO: Modify the implementation of this so that it is a list of cards that includes HoleCards and CommunityCards
class PlayerHand:
    def __init__(self, cards: List[Card]):
        if len(cards) != 7:
            raise ValueError("A PlayerHand must have exactly 7 cards.")
        self.cards = cards
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
