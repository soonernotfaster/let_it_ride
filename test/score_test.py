from hypothesis import given, assume, strategies as st
from score_hand import score, HIGH_CARD_RANKS, CARDS, GameResult, is_straight, is_flush


@st.composite
def low_card_hands(draw) -> list[str]:
    high_cards = list(filter(lambda x: x[0] not in HIGH_CARD_RANKS, CARDS))
    cards = draw(
        st.lists(st.sampled_from(high_cards), min_size=5, max_size=5, unique=True)
    )
    return cards


@given(low_card_hands())
def test_no_win(cards: list[str]):
    assume(not is_straight(cards))
    assume(not is_flush(cards))
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


def test_straight_flush():
    player = ["TC", "9C", "8C"]

    dealer = ["6C", "7C"]

    assert GameResult.StraightFlush == score(dealer, player)


def test_royal_flush():
    player = ["JC", "AC", "KC"]

    dealer = ["TC", "QC"]

    assert GameResult.RoyalFlush == score(dealer, player)
