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
from hypothesis import given, assume, strategies as st
from collections import Counter
from enum import StrEnum

HIGH_CARD_RANKS = {"T", "J", "Q", "K", "A"}
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
SUITS = ["C", "D", "H", "S"]


class GameResult(StrEnum):
    NoPayout = "no-payout"
    Pair = "1-pair"
    TwoPair = "2-pair"
    ThreeOfAKind = "3-of-a-kind"
    FourOfAKind = "4-of-a-kind"
    FullHouse = "full-house"
    Straight = "straight"
    Flush = "flush"


@st.composite
def low_card_hands(draw) -> list[str]:
    high_cards = list(filter(lambda x: x[0] not in HIGH_CARD_RANKS, CARDS))
    cards = draw(
        st.lists(st.sampled_from(high_cards), min_size=5, max_size=5, unique=True)
    )
    return cards


@given(low_card_hands())
def test_no_win(cards: list[str]):
    assume(not _is_straight(cards))
    assume(not _is_flush(cards))
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


def test_full_house():
    player = ["AD", "AC", "AS"]

    dealer = ["TH", "TS"]

    assert GameResult.FullHouse == score(dealer, player)


def test_full_house():
    player = ["AD", "AC", "TH"]

    dealer = ["AS", "TS"]

    assert GameResult.FullHouse == score(dealer, player)


def test_straight():
    player = ["2C", "3D", "4H"]

    dealer = ["5S", "6D"]

    assert GameResult.Straight == score(dealer, player)


def test_flush():
    player = ["6C", "TC", "AC"]

    dealer = ["JC", "2C"]

    assert GameResult.Flush == score(dealer, player)


RANK_INDEX = 0

RANK_TO_VALUE = {
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6,
    "9": 7,
    "T": 8,
    "J": 9,
    "Q": 10,
    "K": 11,
    "A": 12,
}


def _is_straight(hand: list[str]) -> bool:
    ranks = sorted([RANK_TO_VALUE[c[0]] for c in hand])

    for i in range(4):
        if ranks[i] + 1 != ranks[i + 1]:
            return False

    return True


def _is_flush(hand: list[str]) -> bool:
    suits = [c[1] for c in hand]
    print(suits)
    suit_frequencies = Counter(suits)

    suit_frequency_dist = Counter(suit_frequencies.values())
    print(suit_frequency_dist)

    if 5 in suit_frequency_dist:
        return True
    return False


def score(dealer: list[str], player: list[str]) -> str:
    def by_rank(card: str) -> None:
        return card[0]

    full_hand = sorted(dealer + player, key=by_rank)
    ranks = [c[RANK_INDEX] for c in full_hand if c[RANK_INDEX] in HIGH_CARD_RANKS]
    count_by_ranks = Counter(ranks)
    rank_frequency_dist = Counter(count_by_ranks.values())

    if _is_flush(full_hand):
        return GameResult.Flush
    if _is_straight(full_hand):
        return GameResult.Straight
    if 3 in rank_frequency_dist and 2 in rank_frequency_dist:
        return GameResult.FullHouse
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
