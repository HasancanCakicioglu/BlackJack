from card import Card
from chip import Chip
from enum import Enum


class Outcome(Enum):
    WIN = "Win"
    LOSS = "Loss"
    DRAW = "Draw"
    UNCLEAR = "unclear"

class Hand:
    """
    Class representing a hand of playing cards.

    Attributes:
    - cards (List[Card]): A list of Card objects representing the cards in the hand.
    - chip (Chip): The chip object representing the bet placed on the hand.
    """

    def __init__(self, chip: Chip):
        """
        Initializes an empty hand.
        """
        self.cards: list[Card] = []  # This list will contain instances of the Card class
        self.chip = chip
        self.done = False
        self.case = Outcome.UNCLEAR

    def add_card(self, card: Card):
        """
        Adds a card to the hand.

        Args:
        - card (Card): The Card object to add to the hand.
        """
        self.cards.append(card)

    def get_value(self):
        """
        Calculates the value of the hand.

        Returns:
        - int: The total value of the hand.
        """

        cards = [card for card in self.cards if not card.hidden]

        total_value = sum(card.value for card in cards)
        # Check for aces and adjust their value if needed
        num_aces = sum(1 for card in cards if card.rank == 'Ace')
        while total_value > 21 and num_aces:
            total_value -= 10
            num_aces -= 1
        return total_value

    def is_busted(self):
        """
        Checks if the hand is busted (total value exceeds 21).

        Returns:
        - bool: True if the hand is busted, False otherwise.
        """
        if self.get_value() > 21:

            self.done = True
            return self.done
        return False

    def is_win(self,dealer_hand):
        """
        Checks if the hand is win (total value exceeds 21).

        Returns:
        - bool: True if the hand is win, False otherwise.
        """
        if self.get_value() > 21:
            return Outcome.LOSS
        elif dealer_hand.get_value() > 21:
            return Outcome.WIN
        elif self.get_value() > dealer_hand.get_value():
            return Outcome.WIN
        elif self.get_value() == dealer_hand.get_value():
            return Outcome.DRAW
        return Outcome.LOSS


    def __str__(self):
        """
        Returns a string representation of the hand (list of card strings).
        """
        num_cards = len(self.cards)
        card_strings = ', '.join('*******' if card.hidden else str(card) for card in self.cards)

        return f"Hand Object: Contains {num_cards} cards - Cards: [{card_strings}] - Hand Value: {self.get_value()}"

    def __repr__(self):
        """
        Returns a string representation of the hand for debugging purposes.
        """
        return f"Hand(cards={self.cards})"

