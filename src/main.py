import pandas as pd
from score_hand import score, CARDS
from numpy import random


def generate_games() -> None:
    random.seed(42)
    sims = 100_000

    observations = []

    for i in range(sims):
        cards = random.choice(CARDS, size=5, replace=False)
        player = cards[:3].tolist()
        dealer = cards[3:].tolist()
        observations.append(
            {"player": player, "dealer": dealer, "result": score(dealer, player)}
        )

    return observations


def main() -> None:
    games = generate_games()

    df = pd.DataFrame.from_dict(games)
    df.to_csv("data/one_player.csv")


if __name__ == "__main__":
    main()
