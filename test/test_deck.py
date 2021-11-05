import unittest
from src.deck import *


class TestDeck(unittest.TestCase):
    def test_card_black(self):
        card = Card(5, Suit.club)
        self.assertTrue(card.is_black)
        card = Card(13, Suit.spade)
        self.assertTrue(card.is_black)

    def test_card_red(self):
        card = Card(5, Suit.diamond)
        self.assertTrue(card.is_red)
        card = Card(13, Suit.heart)
        self.assertTrue(card.is_red)

    def test_card_face(self):
        card = Card(5, Suit.diamond)
        self.assertFalse(card.is_face_card)
        card = Card(13, Suit.heart)
        self.assertTrue(card.is_face_card)

    def test_deck_init(self):
        deck = Deck()
        cards = set()

        for card in deck:
            self.assertFalse(card in cards)
            cards.add(card)

        self.assertEquals(len(cards), 52)

    def test_shuffle(self):
        unshuffled_deck = [Card(val, suit) for suit in Suit for val in range(1, 14)]
        shuffled_deck = Deck().cards

        different_order = False

        for i in range(52):
            if unshuffled_deck[i] != shuffled_deck[i]:
                different_order = True
                break

        self.assertTrue(different_order)

    def test_pull_card(self):
        deck = Deck()
        cards = set()

        for _ in range(52):
            card = deck.pull_card()
            self.assertFalse(card in cards)
            cards.add(card)

        self.assertEquals(len(cards), 52)
        self.assertEquals(len(deck.cards), 0)

    def test_decks_init(self):
        cards = Decks(2)
        num_cards = len(cards.cards)

        cards_found = {}

        for _ in range(num_cards):
            card = cards.pull_card()

            if card not in cards_found:
                cards_found[card] = 0

            cards_found[card] += 1

        self.assertEquals(len(cards_found), 52)

        for card, times_seen in cards_found.items():
            self.assertEquals(times_seen, 2)
