from random import choice

from src.wikipedia_agent import WikipediaAgent


class AgentType:
    """
    Class representing the possible agent types.

    Attributes:
    - RANDOM (str): The agent takes random actions.
    - WIKIPEDIA (str): The agent follows the Wikipedia strategy.
    - ME (str): The agent takes input from the user.
    """
    RANDOM = 'random'
    WIKIPEDIA = 'wikipedia'
    ME = 'me'

class Agent:
    def __init__(self, strategy=AgentType.RANDOM,action_space=None):
        """
        Initializes the Agent with a specified strategy.

        Args:
        - strategy (str): The strategy to use for the agent.
        - action_space (list): The list of possible actions for the agent.

        """
        self.strategy = strategy
        self.action_space = action_space
        self.wikipedia = WikipediaAgent()


    def act(self, dealer_hand, player_hand):
        """
        Returns the recommended action for the player given the current hands.

        Args:
        - dealer_hand (Hand): The dealer's hand.
        - player_hand (Hand): The player's hand.

        Returns:
        - Actions: The recommended action.
        """
        if self.strategy == AgentType.RANDOM:
            return self.action_space.sample()
        elif self.strategy == AgentType.ME:
            return int(input("Please enter the corresponding number for an option (0-3): "))
        elif self.strategy == AgentType.WIKIPEDIA:
            return self.wikipedia.get_action(dealer_hand, player_hand)
