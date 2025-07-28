# Cards
CARDS = [
    "AC",
    "2C",
    "3C",
    "4C",
    "5C",
    "6C",
    "7C",
    "8C",
    "9C",
    "TC",
    "JC",
    "QC",
    "KC",
    "AD",
    "2D",
    "3D",
    "4D",
    "5D",
    "6D",
    "7D",
    "8D",
    "9D",
    "TD",
    "JD",
    "QD",
    "KD",
    "AH",
    "2H",
    "3H",
    "4H",
    "5H",
    "6H",
    "7H",
    "8H",
    "9H",
    "TH",
    "JH",
    "QH",
    "KH",
    "AS",
    "2S",
    "3S",
    "4S",
    "5S",
    "6S",
    "7S",
    "8S",
    "9S",
    "TS",
    "JS",
    "QS",
    "KS",
]
from hypothesis import given, strategies as st
from collections import Counter
from enum import StrEnum

HIGH_CARD_RANKS = {"T", "J", "Q", "K", "A"}
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
SUITS = ["C", "D", "H", "S"]


class GameResult(StrEnum):
    NoPayout = "no_payout"
    Pair = "1-pair"
    TwoPair = "2-pair"
    ThreeOfAKind = "3-of-a-kind"
    FourOfAKind = "4-of-a-kind"


@st.composite
def low_card_hands(draw) -> list[str]:
    high_cards = list(filter(lambda x: x[0] not in HIGH_CARD_RANKS, CARDS))
    cards = draw(
        st.lists(st.sampled_from(high_cards), min_size=5, max_size=5, unique=True)
    )
    return cards


@given(low_card_hands())
def test_no_win(cards: list[str]):
    player = cards[:3]
    dealer = cards[3:]

    assert GameResult.NoPayout == score(dealer, player)


def test_pair_when_dealer_and_player_have_one_card_in_pair():
    player = ["2H", "3S", "JD"]
    dealer = ["4C", "JH"]

    assert GameResult.Pair == score(dealer, player)


def test_pair_when_all_cards_are_in_player_hand():
    player = ["2H", "JH", "JD"]
    dealer = ["4C", "3S"]

    assert GameResult.Pair == score(dealer, player)


def test_pair_when_all_cards_are_in_dealer_hand():
    player = ["2H", "3S", "4C"]
    dealer = ["JD", "JH"]

    assert GameResult.Pair == score(dealer, player)


def test_two_pair_when_dealer_and_player_have_one_of_each_rank():
    player = ["JH", "TD", "4C"]
    dealer = ["JD", "TH"]

    assert GameResult.TwoPair == score(dealer, player)


def test_two_pair_when_dealer_and_player_each_have_a_pair():
    player = ["TH", "TD", "4C"]
    dealer = ["JD", "JH"]

    assert GameResult.TwoPair == score(dealer, player)


def test_two_pair_when_player_has_a_pair_and_dealer_has_remaining_card():
    player = ["TH", "TD", "JH"]
    dealer = ["JD", "4C"]

    assert GameResult.TwoPair == score(dealer, player)


def test_three_of_a_kind_when_player_has_all_three_cards():
    player = ["JD", "JC", "JH"]
    dealer = ["2D", "4C"]

    assert GameResult.ThreeOfAKind == score(dealer, player)


def test_three_of_a_kind_when_player_and_dealer_have_pair():
    player = ["JD", "JC", "4H"]
    dealer = ["JS", "4C"]

    assert GameResult.ThreeOfAKind == score(dealer, player)


def test_four_of_a_kind_when_player_has_three_of_a_kind():
    player = ["JD", "JC", "JS"]

    dealer = ["JH", "4C"]

    assert GameResult.FourOfAKind == score(dealer, player)


def test_four_of_a_kind_when_player_and_dealer_have_pairs():
    player = ["JD", "JC", "4C"]

    dealer = ["JH", "JS"]

    assert GameResult.FourOfAKind == score(dealer, player)


RANK_INDEX = 0


def score(dealer: list[str], player: list[str]) -> str:
    full_hand = dealer + player
    ranks = [c[RANK_INDEX] for c in full_hand if c[RANK_INDEX] in HIGH_CARD_RANKS]
    count_by_ranks = Counter(ranks)
    rank_frequency_dist = Counter(count_by_ranks.values())

    if 2 in rank_frequency_dist:
        if rank_frequency_dist[2] == 2:
            return GameResult.TwoPair
        if rank_frequency_dist[2] == 1:
            return GameResult.Pair
    if 3 in rank_frequency_dist:
        return GameResult.ThreeOfAKind
    if 4 in rank_frequency_dist:
        return GameResult.FourOfAKind

    return GameResult.NoPayout
