import numpy as np

VALUE_OF_POCKET_ACES_BEFORE_SHRINKING = 150
VALUE_OF_WEAKEST_HAND_STILL_IN_TOP_50PCT_OF_HANDS_BEFORE_SHRINKING = 37

MAX_HAND_VALUE_BEFORE_CONVERTING_TO_EXPECTED_VALUE = 200
PRESUMED_PROB_FOR_ACES_TO_WIN_HEADS_UP = 0.85
PRESUMED_PROB_FOR_WEAKEST_HAND_STILL_IN_TOP_50PCT_TO_WIN_HEADS_UP = 0.5

# 100
HAND_VALUE_BONUS_FOR_HEADS_UP_BEFORE_CONVERTING_TO_EXPECTED_VALUE = 50 * 2
# 200 * 0.85 = 170
hand_value_for_aces_before_converting_to_expected_value = (
    MAX_HAND_VALUE_BEFORE_CONVERTING_TO_EXPECTED_VALUE
    * PRESUMED_PROB_FOR_ACES_TO_WIN_HEADS_UP
)

# 200 * 0.5 = 100
hand_value_for_weakest_hand_still_in_top_50pct_before_converting_to_expected_value = (
    MAX_HAND_VALUE_BEFORE_CONVERTING_TO_EXPECTED_VALUE
    * PRESUMED_PROB_FOR_WEAKEST_HAND_STILL_IN_TOP_50PCT_TO_WIN_HEADS_UP
)


# 170 - 100 = 70
adjusted_value_for_aces_before_adding_for_player_count = (
    hand_value_for_aces_before_converting_to_expected_value
    - HAND_VALUE_BONUS_FOR_HEADS_UP_BEFORE_CONVERTING_TO_EXPECTED_VALUE
)

# 100 - 100 = 0
adjusted_value_for_weakest_hand_still_in_top_50pct_before_adding_for_player_count = (
    hand_value_for_weakest_hand_still_in_top_50pct_before_converting_to_expected_value
    - HAND_VALUE_BONUS_FOR_HEADS_UP_BEFORE_CONVERTING_TO_EXPECTED_VALUE
)

# 150 - 37 = 113
range_of_top_50pct_of_hands_before_shrinking = (
    VALUE_OF_POCKET_ACES_BEFORE_SHRINKING
    - VALUE_OF_WEAKEST_HAND_STILL_IN_TOP_50PCT_OF_HANDS_BEFORE_SHRINKING
)

# 70 / 113 = 0.619469
hand_shrink_factor = (
    adjusted_value_for_aces_before_adding_for_player_count
    / range_of_top_50pct_of_hands_before_shrinking
)

# 150 * 0.619469 = 92L
shrunk_value_of_aces = np.floor(
    VALUE_OF_POCKET_ACES_BEFORE_SHRINKING * hand_shrink_factor
)

# 37L * 0.619469 = 22L
shrunk_value_of_weakest_hand_still_in_top_50pct = np.floor(
    VALUE_OF_WEAKEST_HAND_STILL_IN_TOP_50PCT_OF_HANDS_BEFORE_SHRINKING
    * hand_shrink_factor
)

# 92L - 70L = 22L
subtraction_constant_after_shrinking = (
    shrunk_value_of_aces - adjusted_value_for_aces_before_adding_for_player_count
)

# 22L - 0L = 22L
other_subtraction_constant_after_shrinking = (
    shrunk_value_of_weakest_hand_still_in_top_50pct
    - adjusted_value_for_weakest_hand_still_in_top_50pct_before_adding_for_player_count
)
