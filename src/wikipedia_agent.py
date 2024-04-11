from src.hand import Hand


"""
Wikipedia Blackjack Strategy

This code creates a blackjack agent based on the strategy outlined in Wikipedia's "Blackjack" article. 
The agent determines the recommended action for the player (Hit, Stand, Double, Split, Surrender) 
depending on the current state of the hands.

Source: https://en.wikipedia.org/wiki/Blackjack
"""


class Actions:
    """
    Class representing the possible actions in the game of Blackjack.

    Attributes:
    - STAND (int): The player stands.
    - HIT (int): The player hits.
    - DOUBLE (int): The player doubles down.
    - SPLIT (int): The player splits the hand.
    - SURRENDER (int): The player surrenders.
    """

    STAND = 0
    HIT = 1
    DOUBLE = 2
    SPLIT = 3
    SURRENDER = 4

class WikipediaAgent:
    def __init__(self,surrender=False,double_down=True):
        """
        Initializes a WikipediaAgent instance with optional surrender and double down abilities.

        Args:
        - surrender (bool): Whether the agent can surrender (default is False).
        - double_down (bool): Whether the agent can double down (default is True).
        """

        # Allowes the agent to surrender
        self.surrender = surrender

        # Allowes the agent to double down
        self.double_down = double_down

    def get_action(self, dealer_hand:Hand, player_hand:Hand):
        """
        Returns the recommended action for the player given the current hands.

        Args:
        - dealer_hand (Hand): The dealer's hand.
        - player_hand (Hand): The player's hand.

        Returns:
        - int: The recommended action (Actions.STAND, Actions.HIT, Actions.DOUBLE, Actions.SPLIT, Actions.SURRENDER).
        """
        player_value = player_hand.get_value()

        # Dealer's upcard
        dealerCard = dealer_hand.cards[0]

        # Pairs strategy
        if player_hand.can_split():
            card = player_hand.cards[0]
            if card.rank == 'Ace':
                return Actions.SPLIT
            elif card.value == 10:
                return Actions.STAND
            elif card.value == 9:
                if dealerCard.rank in ['Seven', 'Ten','Jack','Queen','King', 'Ace']:
                    return Actions.STAND
                return Actions.SPLIT
            elif card.value == 8:
                if dealerCard.rank in ['Ace'] and self.surrender:
                    return Actions.SURRENDER
                else:
                    return Actions.SPLIT
            elif card.value == 7:
                if dealerCard.rank in ['Eight', 'Nine', 'Ten','Jack','Queen','King', 'Ace']:
                    return Actions.HIT
                return Actions.SPLIT
            elif card.value == 6:
                if dealerCard.rank in ['Seven', 'Eight', 'Nine', 'Ten','Jack','Queen','King', 'Ace']:
                    return Actions.HIT
                return Actions.SPLIT
            elif card.value == 5:
                if dealerCard.rank in ['Ten','Jack','Queen','King', 'Ace']:
                    return Actions.HIT
                elif self.double_down:
                    return Actions.DOUBLE
                else:
                    return Actions.HIT
            elif card.value == 4:
                if dealerCard.rank in ['Five', 'Six']:
                    return Actions.SPLIT
                return Actions.HIT
            elif card.value == 3 or card.value == 2:
                if dealerCard.rank in ['Eight', 'Nine', 'Ten','Jack','Queen','King', 'Ace']:
                    return Actions.HIT
                return Actions.SPLIT


        # Soft hands strategy
        elif player_hand.is_soft_hand():
            if player_value == 21:
                return Actions.STAND
            elif player_value == 20:
                return Actions.STAND
            elif player_value == 19:
                if dealerCard.rank in ['Six']:
                    if player_hand.can_double() and self.double_down:
                        return Actions.DOUBLE
                return Actions.STAND
            elif player_value == 18:
                if dealerCard.rank in ['Two', 'Three', 'Four', 'Five', 'Six']:
                    if player_hand.can_double() and self.double_down:
                        return Actions.DOUBLE
                    else:
                        return Actions.STAND
                if dealerCard.rank in ['Seven', 'Eight']:
                    return Actions.STAND
                return Actions.HIT
            elif player_value == 17:
                if dealerCard.rank in ['Three', 'Four', 'Five', 'Six']:
                    if player_hand.can_double() and self.double_down:
                        return Actions.DOUBLE
                    else:
                        return Actions.HIT
                else:
                    return Actions.HIT
            elif player_value == 16 or player_value == 15:
                if dealerCard.rank in ['Four', 'Five', 'Six']:
                    if player_hand.can_double() and self.double_down:
                        return Actions.DOUBLE
                    else:
                        return Actions.HIT
                else:
                    return Actions.HIT
            elif player_value == 14 or player_value == 13:
                if dealerCard.rank in ['Five', 'Six']:
                    if player_hand.can_double() and self.double_down:
                        return Actions.DOUBLE
                    else:
                        return Actions.HIT
                else:
                    return Actions.HIT
            elif player_value == 12 and len(player_hand.cards)==2:
                if dealerCard.rank in ['Six']:
                    if player_hand.can_double() and self.double_down:
                        return Actions.DOUBLE
                    else:
                        return Actions.HIT
                else:
                    return Actions.HIT



        # Hard hands strategy
        elif player_value >= 17:
            if dealerCard.rank == 'Ace' and player_value == 17:
                if self.surrender:
                    return Actions.SURRENDER
            return Actions.STAND
        elif player_value == 16:
            if dealerCard.rank in ['Nine', 'Ten','Jack','Queen','King', 'Ace']:
                if self.surrender:
                    return Actions.SURRENDER
                else:
                    return Actions.HIT
            elif dealerCard.rank in ['Seven', 'Eight']:
                return Actions.HIT
            else:
                return Actions.STAND
        elif player_value == 15:
            if dealerCard.rank in ['Ten','Jack','Queen','King', 'Ace']:
                if self.surrender:
                    return Actions.SURRENDER
                else:
                    return Actions.HIT
            elif dealerCard.rank in ['Seven', 'Eight', 'Nine']:
                return Actions.HIT
            else:
                return Actions.STAND
        elif player_value == 14 or player_value == 13:
            if dealerCard.rank in ['Seven', 'Eight', 'Nine', 'Ten','Jack','Queen','King', 'Ace']:
                return Actions.HIT
            else:
                return Actions.STAND
        elif player_value == 12:
            if dealerCard.rank in ['Four', 'Five', 'Six']:
                return Actions.STAND
            else:
                return Actions.HIT
        elif player_value == 11:
            if player_hand.can_double() and self.double_down:
                return Actions.DOUBLE
            else:
                return Actions.HIT
        elif player_value == 10:
            if dealerCard.rank in ['Ten','Jack','Queen','King', 'Ace']:
                return Actions.HIT
            elif player_hand.can_double() and self.double_down:
                return Actions.DOUBLE
            else:
                return Actions.HIT
        elif player_value == 9:
            if dealerCard.rank in ['Three', 'Four', 'Five', 'Six']:
                if player_hand.can_double() and self.double_down:
                    return Actions.DOUBLE
                else:
                    return Actions.HIT
            else:
                return Actions.HIT
        elif player_value <= 8:
            return Actions.HIT



