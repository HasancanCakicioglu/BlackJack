from hand import Hand


class Seat:
    """
    Class representing a seat at the blackjack table.

    Attributes:
    - hands (list): A list of Hand objects representing the hands at the seat.
    """

    def __init__(self):
        """
        Initializes a seat with no hands.
        """
        self.hands: list[Hand] = []

    def add_hand(self, hand):
        """
        Adds a hand to the seat.

        Args:
        - hand (Hand): The Hand object to add to the seat.
        """
        if len(self.hands) < 2:
            self.hands.append(hand)
        else:
            print("You cannot have more than 2 hands at a seat.")

    def split_hand(self):
        """
        Splits a hand at the specified index.

        Args:
        - hand_index (int): The index of the hand to split.
        """
        if len(self.hands) != 1 and len(self.hands[0].cards) != 2:
            print("You need 1 hands to split.")
            print("You need 2 cards to split.")
            return

        hand_one = Hand(chip=self.hands[0].chip)
        hand_one.add_card(self.hands[0].cards[0])
        hand_two = Hand(chip=self.hands[0].chip)
        hand_two.add_card(self.hands[0].cards[1])
        self.hands = [hand_one, hand_two]

    def __str__(self):
        """
        Returns a string representation of the seat (list of hand strings).
        """
        seat_info = f"Seat Object: Contains {len(self.hands)} hands\n"
        hand_info = ""
        for idx, hand in enumerate(self.hands, start=1):
            hand_info += f"   - Hand {idx}: {str(hand)}\n"  # İkinci düzey girinti ekleniyor
        return seat_info + hand_info

    def __repr__(self):
        """
        Returns a string representation of the seat for debugging purposes.
        """
        return f"Seat(hands={self.hands})"

