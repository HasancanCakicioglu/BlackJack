from typing import SupportsFloat, Any, Optional, Union
import gymnasium as gym
from gymnasium.core import ActType, ObsType, RenderFrame
from gymnasium.vector.utils import spaces
from deck import Deck
from table import Table
from seat import Seat
from hand import Hand
from chip import Chip


class BlackJackEnv(gym.Env):
    def __init__(self):
        self.deck = Deck()
        self.table = Table()

        self.table = self.create_objects(self.table,1,[100])

        self.dealer_hand = []
        self.player_hand = []

        self.action_space = spaces.Discrete(5)  # 0: stand, 1: hit, 2: double, 3: split, 4: surrender
        self.observation_space = spaces.Tuple(
            [
                spaces.Discrete(32),  # player sum
                spaces.Discrete(11),  # dealer card
                spaces.Discrete(2),  # usable ace
            ]
        )
        self.state = ()
        print(self.dealer_hand)
    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        pass

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict[str, Any]] = None,
    ) -> tuple[ObsType, dict[str, Any]]:
        pass

    def render(self) -> Union[RenderFrame, list[RenderFrame], None]:
        pass

    def close(self):
        pass

    def get_obs(self):
        pass

    def distribute_cards(self):
        for _ in range(2):
            for i in self.table.seats:
                i.hands[0].add_card(self.deck.hit())
            self.dealer_hand.append(self.deck.hit())

    def create_objects(self,table,seats_count,chip_amounts):
        assert seats_count == len(chip_amounts)

        for i in range(seats_count):
            seat = Seat()
            hand = Hand(chip=Chip(chip_amounts[i]))
            seat.add_hand(hand)
            table.add_seat(seat)
        return table



b = BlackJackEnv()
b.deck.shuffle()
b.distribute_cards()
print(b.table)
print(b.dealer_hand)