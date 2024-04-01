
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:
    """
    Class representing a playing card.

    Attributes:
    - suit (str): The suit of the card ('Hearts', 'Diamonds', 'Spades', 'Clubs').
    - rank (str): The rank of the card ('Two', 'Three', ..., 'King', 'Ace').
    - value (int): The value of the card in the game of Blackjack.
    """

    def __init__(self, suit, rank, hidden=False):
        """
        Initializes a playing card with a given suit and rank.
        """
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        self.hidden = hidden

    def __str__(self):
        """
        Returns a string representation of the card.
        """
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        """
        Returns a string representation of the card for debugging purposes.
        """
        return f"Card('{self.suit}', '{self.rank}')"

    def __eq__(self, other):
        """
        Checks if two cards are equal.
        """
        return self.suit == other.suit and self.rank == other.rank

    def __lt__(self, other):
        """
        Checks if this card is less than another card based on their values.
        """
        return values[self.rank] < values[other.rank]

    def __gt__(self, other):
        """
        Checks if this card is greater than another card based on their values.
        """
        return values[self.rank] > values[other.rank]
