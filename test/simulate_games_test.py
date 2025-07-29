import pandas as pd
import numpy as np
from score_hand import CARDS


def simulate_games(sims: int) -> pd.DataFrame:
    plays = []

    for _i in range(sims):
        player_hand = np.random.choice(CARDS, 3)
        plays.append({"player_1": player_hand, "dealer": "b", "player_1_result": "c"})

    return pd.DataFrame.from_records(plays)


def test_play_game():
    num_sims = 10
    expected_columns = ["player_1", "dealer", "player_1_result"]
    result = simulate_games(num_sims)

    assert len(result) == num_sims
    assert expected_columns == result.columns.to_list()
    assert all([len(hand) == 3 for hand in result.player_1]), "All hands are size 3"
