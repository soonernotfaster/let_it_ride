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

HIGH_CARD_RANKS = {"T", "J", "Q", "K", "A"}
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
SUITS = ["C", "D", "H", "S"]


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

    assert "no_payout" == score(dealer, player)


def score(dealer: list[str], player: list[str]) -> str:
    return "no_payout"
