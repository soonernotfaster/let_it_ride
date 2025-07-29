import pandas as pd
import numpy as np
from score_hand import CARDS


def simulate_games(sims: int) -> pd.DataFrame:
    plays = []

    for _i in range(sims):
        hand = np.random.choice(CARDS, 5)
        player_hand = hand[:3]
        dealer_hand = hand[3:]
        plays.append(
            {
                "player_1": player_hand,
                "dealer_hand": dealer_hand,
                "player_1_result": "c",
            }
        )

    return pd.DataFrame.from_records(plays)


def test_play_game():
    num_sims = 10
    expected_columns = ["player_1", "dealer_hand", "player_1_result"]
    result = simulate_games(num_sims)

    assert len(result) == num_sims
    assert expected_columns == result.columns.to_list()
    assert all([len(hand) == 3 for hand in result.player_1]), "Player hands are size 3"
    assert all(
        [len(hand) == 2 for hand in result.dealer_hand]
    ), "Dealer hands are size 2"
