from typing import SupportsFloat, Any, Optional, Union
import gymnasium as gym
from gymnasium.core import ActType, ObsType, RenderFrame
from gymnasium.vector.utils import spaces
from deck import Deck
from table import Table
from seat import Seat
from hand import Hand, Outcome
from chip import Chip


class BlackJackEnv(gym.Env):
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.table = Table()

        self.table = self.create_objects(self.table, 1, [100])

        self.dealer_hand = Hand(chip=Chip(0))
        self.playingHand = None

        self.distribute_cards()

        self.action_space = spaces.Discrete(5)  # 0: stand, 1: hit, 2: double, 3: split
        self.observation_space = spaces.Tuple(
            [
                spaces.Discrete(32),  # player sum
                spaces.Discrete(11),  # dealer card
                spaces.Discrete(2),  # usable ace
            ]
        )
        self.state = ()
    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:

        hand, seat = self.get_next_hand()

        if action == 0:
            hand.done = True
        elif action == 1:
            hand.add_card(self.deck.hit())
            hand.is_busted()
        elif action == 2:
            hand.add_card(self.deck.hit())
            hand.chip.double()
            hand.done = True
        elif action == 3:
            seat.split_hand()

        self.playingHand = hand
        hand = self.get_next_hand()
        if hand == None:
            self.dealer_play()
            reward = self.results()

            return self.get_obs(), reward, True, True, {}

        return self.get_obs(), 0, False, False, {}



    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict[str, Any]] = None,
    ) -> tuple[ObsType, dict[str, Any]]:

        if self.deck.needs_shuffle():
            self.deck = Deck()
            self.deck.shuffle()

        self.table = Table()

        self.table = self.create_objects(self.table, 1, [100])

        self.dealer_hand = Hand(chip=Chip(0))
        self.playingHand = self.get_next_hand()[0]
        self.distribute_cards()
        return self.get_obs(), {}

    def render(self) -> Union[RenderFrame, list[RenderFrame], None]:
        pass

    def close(self):
        pass

    def get_obs(self):
        return [
            self.dealer_hand,
            self.playingHand
        ]

    def distribute_cards(self):
        for k in range(2):
            for i in self.table.seats:
                i.hands[0].add_card(self.deck.hit())

            card = self.deck.hit()
            if k == 1:
                card.hidden = True
            self.dealer_hand.add_card(card)

    def create_objects(self,table,seats_count,chip_amounts):
        assert seats_count == len(chip_amounts)

        for i in range(seats_count):
            seat = Seat()
            hand = Hand(chip=Chip(chip_amounts[i]))
            seat.add_hand(hand)
            table.add_seat(seat)
        return table

    def dealer_play(self):

        self.dealer_hand.cards[1].hidden = False

        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.hit())


    def results(self):
        win_chip = 0
        loss_chip = 0
        for seat in self.table.seats:
            for hand in seat.hands:
                outcome = hand.is_win(self.dealer_hand)
                if outcome == Outcome.WIN:
                    win_chip += hand.chip.value
                elif outcome == Outcome.LOSS:
                    loss_chip += hand.chip.value
        return win_chip - loss_chip




    def get_next_hand(self):
        for seat in self.table.seats:
            for hand in seat.hands:
                if hand.done == False:
                    return hand , seat
        return None


