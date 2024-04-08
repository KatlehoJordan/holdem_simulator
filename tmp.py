# TODO: Remove this file after you've fixed the bug that is not saving the correct player_1_wins_as_float value when there are ties.
import pandas as pd

my_df = pd.read_csv("simulations/unaggregated/unaggregated data for 2 players.csv")

# When "you_win_as_float" == 0.5, update "player_1_wins_as_float" to 0.5
my_df.loc[my_df["you_win_as_float"] == 0.5, "player_1_wins_as_float"] = 0.5

my_df.loc[my_df["winning_type"] == "Tie", "player_1_wins"] = True

# Save the updated DataFrame to a new CSV file

my_df.to_csv(
    "simulations/unaggregated/unaggregated data for 2 players fixed.csv", index=False
)
