from collections import Counter
from enum import StrEnum

HIGH_CARD_RANKS = {"T", "J", "Q", "K", "A"}
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
SUITS = ["C", "D", "H", "S"]
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


class GameResult(StrEnum):
    NoPayout = "no-payout"
    Pair = "1-pair"
    TwoPair = "2-pair"
    ThreeOfAKind = "3-of-a-kind"
    FourOfAKind = "4-of-a-kind"
    FullHouse = "full-house"
    Straight = "straight"
    Flush = "flush"
    StraightFlush = "straight-flush"
    RoyalFlush = "royal-flush"


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


def is_straight(hand: list[str]) -> bool:
    ranks = sorted([RANK_TO_VALUE[c[0]] for c in hand])

    for i in range(4):
        if ranks[i] + 1 != ranks[i + 1]:
            return False

    return True


def is_flush(hand: list[str]) -> bool:
    suits = [c[1] for c in hand]
    suit_frequencies = Counter(suits)
    suit_frequency_dist = Counter(suit_frequencies.values())

    if 5 in suit_frequency_dist:
        return True
    return False


def score(dealer: list[str], player: list[str]) -> str:
    hand = dealer + player

    return _check_made_hands(hand) or _check_pair_hands(hand) or GameResult.NoPayout


def _check_made_hands(hand: list[str]) -> GameResult:
    if is_flush(hand) and _all_high_cards(hand):
        return GameResult.RoyalFlush
    if is_flush(hand) and is_straight(hand):
        return GameResult.StraightFlush
    if is_flush(hand):
        return GameResult.Flush
    if is_straight(hand):
        return GameResult.Straight

    return None


def _all_high_cards(hand: list[str]) -> bool:
    return all([c[0] in HIGH_CARD_RANKS for c in hand])


def _check_pair_hands(hand: list[str]) -> GameResult:
    ranks = [c[RANK_INDEX] for c in hand if c[RANK_INDEX] in HIGH_CARD_RANKS]
    count_by_ranks = Counter(ranks)
    rank_frequency_dist = Counter(count_by_ranks.values())

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

    return None
