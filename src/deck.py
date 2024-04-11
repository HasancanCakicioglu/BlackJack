from card import Card, suits, ranks, values
import random


class Deck:
    """
    Class representing a deck of playing cards.

    Attributes:
    - cards (list): A list of Card objects representing the deck of cards.
    - num_decks (int) : Number of Deck, Each deck has 52 card
    - cards_drawn_from_each (list): A list of integers representing the number of cards drawn from each rank.
    """

    def __init__(self, num_decks=8):
        """
        Initializes a deck of playing cards with the specified number of decks.
        """
        self.cards = []
        self.num_decks = num_decks
        self.populate_deck()
        self.cards_drawn_from_each = [0 for _ in range(10)]  # 2, 3, 4, 5, 6, 7, 8, 9, 10, A
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
        card = self.cards.pop()
        self.cards_drawn_from_each[card.value-2] += 1
        return card

    def needs_shuffle(self):
        """
        Checks if the deck needs to be shuffled.

        Returns:
        - True if less than 30% of the cards remain in the deck, False otherwise.
        """
        return len(self.cards) / (52 * self.num_decks) < 0.3

    def reset(self, num_decks=8):
        """
        Resets the deck by repopulating and shuffling the cards.
        """
        self.cards = []
        self.num_decks = num_decks
        self.populate_deck()
        self.cards_drawn_from_each = [0 for _ in range(10)]  # 2, 3, 4, 5, 6, 7, 8, 9, 10, A

        assert len(self.cards) == 52 * num_decks, f"Deck must contain {52 * num_decks} cards upon initialization"

    def probability_of_cards(self):
        """
        Returns the probability of drawing each card from the deck.
        """
        remaining_cards = (self.num_decks * 52) - sum(self.cards_drawn_from_each)
        probabilities = [(((self.num_decks * (16 if index == 8 else 4))-count)/remaining_cards) for index,count in enumerate(self.cards_drawn_from_each)]
        return probabilities


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
