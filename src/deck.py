from card import Card, suits, ranks
import random


class Deck:
    """
    Class representing a deck of playing cards.

    Attributes:
    - cards (list): A list of Card objects representing the deck of cards.
    - num_decks (int) : Number of Deck, Each deck has 52 card
    """

    def __init__(self, num_decks=8):
        """
        Initializes a deck of playing cards with the specified number of decks.
        """
        self.cards = []
        self.num_decks = num_decks
        self.populate_deck()
        assert len(self.cards) == 52 * num_decks, f"Deck must contain {52 * num_decks} cards upon initialization"

    def populate_deck(self):
        """
        Populates the deck with playing cards from multiple decks.
        """
        self.cards.clear()
        for _ in range(self.num_decks):
            for suit in suits:
                for rank in ranks:
                    self.cards.append(Card(suit, rank))

    def shuffle(self):
        """
        Shuffles the deck of cards.
        """
        random.shuffle(self.cards)

    def hit(self):
        """
        Draws a card from the deck (removes and returns the last card in the list).
        """
        if len(self.cards) == 0:
            raise ValueError("Deck is empty, cannot draw a card")
        return self.cards.pop()

    def needs_shuffle(self):
        """
        Checks if the deck needs to be shuffled.

        Returns:
        - True if less than 30% of the cards remain in the deck, False otherwise.
        """
        return len(self.cards) / (52 * self.num_decks) < 0.3

    def __str__(self):
        """
        Returns a string representation of the deck (list of card strings).
        """
        return '\n'.join(str(card) for card in self.cards)

    def __repr__(self):
        """
        Returns a string representation of the deck for debugging purposes.
        """
        return f"Deck(num_decks={self.num_decks}, cards={self.cards})"
