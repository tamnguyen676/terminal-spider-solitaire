from enum import Enum
import random


class Suit(Enum):
    club = 1
    spade = 2
    diamond = 3
    heart = 4


suits = {
    Suit.club: '♣',
    Suit.spade: '♠',
    Suit.diamond: '♦',
    Suit.heart: '♥'
}
A, J, Q, K, = 1, 11, 12, 13


class Card:
    def __init__(self, value, suit, revealed=False, holding=False, show_suit=False):
        self.value = value
        self.suit = suit
        self.revealed = revealed
        self.holding = holding
        self.symbol = self._to_symbol(show_suit)

        self.is_face_card = value in [A, J, Q, K]
        self.is_red = suit in [Suit.heart, Suit.diamond]
        self.is_black = not self.is_red

    def equals(self, other, suits, offset=0):
        if other.value + offset != self.value:
            return False
        if suits == 1:
            return True
        elif suits == 2:
            return other.is_red == self.is_red
        else:
            return other.suit == self.suit

    def _to_symbol(self, show_suit):

        if 2 <= self.value <= 10:
            symbol = str(self.value)
        elif self.value == 1:
            symbol = 'A'
        elif self.value == 11:
            symbol = 'J'
        elif self.value == 12:
            symbol = 'Q'
        else:
            symbol = 'K'

        if show_suit:
            symbol += suits[self.suit]

        return symbol

    def __hash__(self):
        return hash((self.value, self.suit))

    def __eq__(self, other):
        return other.value == self.value and other.suit == self.suit


class Cards:
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = cards

    def __iter__(self):
        return self.cards.__iter__()

    def __len__(self):
        return len(self.cards)

    def __delitem__(self, key):
        self.cards.__delitem__(key)

    def __getitem__(self, key):
        return self.cards.__getitem__(key)

    def __setitem__(self, key, value):
        self.cards.__setitem__(key, value)

    def shuffle(self):
        random.shuffle(self.cards)

    def pull_card(self):
        return self.cards.pop()

    def add_card(self, card):
        self.cards.append(card)

    def add_cards(self, cards):
        self.cards.extend(cards)


class Deck(Cards):
    def __init__(self, show_suit=False):
        cards = [Card(val, suit, show_suit=show_suit) for suit in Suit for val in range(1, 14)]
        super().__init__(cards)
        self.shuffle()


class Decks(Cards):
    def __init__(self, num_decks, show_suit=False):
        self.num_decks = num_decks
        cards = [card for _ in range(self.num_decks) for card in Deck(show_suit)]
        super().__init__(cards)
        self.shuffle()
