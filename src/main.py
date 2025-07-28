import pandas as pd
from score_hand import score, CARDS
from numpy import random


def generate_games() -> None:
    random.seed(42)
    sims = 100_000

    observations = []

    for i in range(sims):
        cards = random.choice(CARDS, size=8, replace=False)
        player_1 = cards[:3].tolist()
        player_2 = cards[3:6].tolist()
        dealer = cards[6:].tolist()
        observations.append(
            {
                "player_1": player_1,
                "player_2": player_2,
                "dealer": dealer,
                "player_1_result": score(dealer, player_1),
                "player_2_result": score(dealer, player_2),
            }
        )

    return observations


def main() -> None:
    games = generate_games()

    df = pd.DataFrame.from_dict(games)
    df.to_csv("data/two_player.csv")


if __name__ == "__main__":
    main()
