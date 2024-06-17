from typing import SupportsFloat, Any, Optional
import gymnasium as gym
import numpy as np
import pygame
from gymnasium.core import ActType, ObsType
from gymnasium.vector.utils import spaces
from src.deck import Deck
from src.table import Table
from src.seat import Seat
from src.hand import Hand, Outcome
from src.chip import Chip


class BlackJackEnv(gym.Env):
    """
    A Blackjack environment.

    Attributes:
        - screen: The Pygame screen for rendering the game.
        - clock: The Pygame clock for managing time.
        - seats_count: The number of seats at the table.
        - chip_amounts: The list of chip amounts for each seat.
         - win: The number of wins.
        - loss: The number of losses.
        - draw: The number of draws.
        - played_hands: The number of hands played.
        - deck: The deck of cards.
        - table: The table containing seats and hands.
        - dealer_hand: The dealer's hand.
        - playingHand: The current playing hand.
        - done: Flag indicating if the game is done.
        - reward: The reward for the current action.
        - action_space: The action space for the environment.
        - observation_space: The observation space for the environment.

    """

    metadata = {"render_modes": ["human", "cmd"], "render_fps": 1}
    def __init__(self, seats_count=1, chip_amounts= [100],render_mode="cmd",fps=1,envV = 1,*args, **kwargs):
        super().__init__()
        """
        Initializes a Blackjack environment.

        Args:
        - seats_count (int): The number of seats at the table.
        - chip_amounts (list): A list of chip amounts for each seat.

        """
        self.envV = envV

        self.screen = None
        self.clock = None

        self.seats_count = seats_count
        self.chip_amounts = chip_amounts
        self.render_mode = render_mode
        self.fps = fps

        self.win = 0
        self.loss = 0
        self.draw = 0
        self.played_hands = 0
        self.illegal_moves = 0
        self.money = 0
        self.all_money = 0
        self.earn_money_rate = 0
        self.loss_money_rate = 0

        self.deck = Deck()
        self.deck.shuffle()
        self.table = Table()
        self.table = self.create_objects(self.table,self.seats_count, self.chip_amounts)
        self.dealer_hand = Hand(chip=Chip(0))
        self.playingHand = None
        self.done = False
        self.distribute_cards()
        self.reward = 0

        if envV ==1:
            self.action_space = spaces.Discrete(4)  # 0: stand, 1: hit, 2: double, 3: split

            self.observation_space = spaces.Dict({
                "player_sum": spaces.Discrete(32),
                "dealer_card": spaces.Discrete(12),
                "usable_ace": spaces.Discrete(2),
                "can_split": spaces.Discrete(2),
                "can_double": spaces.Discrete(2),

            })

        if envV == 2:
            self.action_space = spaces.Discrete(4)  # 0: stand, 1: hit, 2: double, 3: split

            self.observation_space = spaces.Dict({
                "player_sum": spaces.Discrete(32),
                "dealer_card": spaces.Discrete(12),
                "usable_ace": spaces.Discrete(2),
                "can_split": spaces.Discrete(2),
                "can_double": spaces.Discrete(2),

                "two": spaces.Discrete(100),
                "three": spaces.Discrete(100),
                "four": spaces.Discrete(100),
                "five": spaces.Discrete(100),
                "six": spaces.Discrete(100),
                "seven": spaces.Discrete(100),
                "eight": spaces.Discrete(100),
                "nine": spaces.Discrete(100),
                "ten": spaces.Discrete(100),
                "ace": spaces.Discrete(100),
                "last_card": spaces.Discrete(12),

            })
        if envV == 3:
            self.action_space = spaces.Discrete(4)  # 0: stand, 1: hit, 2: double, 3: split

            self.observation_space = spaces.Dict({
                "player_sum": spaces.Discrete(32),
                "dealer_card": spaces.Discrete(12),
                "usable_ace": spaces.Discrete(2),
                "can_split": spaces.Discrete(2),
                "can_double": spaces.Discrete(2),

                "prob":spaces.Box(low=0, high=100, shape=(10,), dtype=np.float16),
                "last_card":spaces.Discrete(12),
                "last_second_card":spaces.Discrete(12),
                "last_third_card":spaces.Discrete(12),


            })

        #self.observation_space = spaces.MultiDiscrete([17, 10, 2])


    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        """
        Perform a step in the environment.

        Args:
        - action (ActType): The action to take.

        Returns:
        - tuple: Tuple containing the next observation, reward, done flag, info dictionary.
        """
        hand, seat = self.get_next_hand()

        if action == 0:
            hand.done = True
        elif action == 1:
            hand.add_card(self.deck.hit())
            hand.is_busted()
        elif action == 2:
            if not hand.double_down(self.deck):
                self.illegal_moves += 1
                return self.get_obs(), self.table.len_hands() * -100, True, True, {}
                pass

        elif action == 3:
            if not seat.split_hand():
                self.illegal_moves += 1
                return self.get_obs(), self.table.len_hands() * -100, True, True, {}
                pass
            else:
                seat.hands[0].add_card(self.deck.hit())
                seat.hands[1].add_card(self.deck.hit())

        self.playingHand = hand
        hand = self.get_next_hand()

        if hand is None:

            self.dealer_play()
            self.reward = self.results()
            self.money = self.money + self.reward
            self.done = True
            self.sum_all_chips()
            self.deck.add_last_secret_to_prob()
            return self.get_obs(), self.reward, True, True, {}
        else:
            self.playingHand = hand[0]

        return self.get_obs(), 0, False, False, {}

    def reset(
        self,
        seed: Optional[int] = None,
        full_reset: bool = True
    ):
        """
        Reset the environment.

        Args:
        - seed (int): Optional seed for random number generation.
        - options (dict): Optional dictionary of environment options.
        - full_reset (bool): Whether to fully reset the environment or not.

        Returns:
        - ObsType: The initial observation after reset.
        """

        if full_reset:
            self.deck = Deck()
            self.deck.shuffle()
        else:
            if self.deck.needs_shuffle():
                self.deck = Deck()
                self.deck.shuffle()

        self.table = Table()

        self.table = self.create_objects(self.table,self.seats_count , self.chip_amounts)
        self.done = False
        self.dealer_hand = Hand(chip=Chip(0))
        self.playingHand = self.get_next_hand()[0]
        self.distribute_cards()
        return self.get_obs(),{}

    def render(self):
        """
         Render the environment.

         Args:
         - mode (str): The rendering mode. Options are 'human' or 'cmd'.
         """

        if self.render_mode == 'human':

            def draw_circle(window, value, x, y, color= (0, 0, 0)):
                circle_radius = 12
                circle_color = color
                font = pygame.font.SysFont(None, 24)
                text_color = (255, 255, 255)  # Beyaz renk

                pygame.draw.circle(window, circle_color, (int(x), int(y)), circle_radius)

                text_surface = font.render(str(value), True, text_color)
                text_rect = text_surface.get_rect()
                text_rect.center = (int(x), int(y))

                window.blit(text_surface, text_rect)

            if self.screen is None:

                pygame.init()
                pygame.display.set_caption("BlackJack")
                self.screen = pygame.display.set_mode((800, 600))
                self.clock = pygame.time.Clock()

                self.screenWidth , self.screenHeight = pygame.display.get_surface().get_size()
                self.cardWidth = 50
                self.cardHeight = 80

            self.screen.fill((0, 128, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.clock.tick(self.fps)

            for indexCard,card in enumerate(self.dealer_hand.cards):
                if card.hidden:
                    image = pygame.transform.scale(pygame.image.load("../assets/cardback.png"), (self.cardWidth, self.cardHeight))
                    self.screen.blit(image, ((self.screenWidth/2)+(indexCard*10)-(self.cardWidth/2),(70)-(indexCard*10)))
                else:
                    image = pygame.transform.scale(pygame.image.load(card.get_asset_path()), (self.cardWidth, self.cardHeight))
                    self.screen.blit(image, ((self.screenWidth/2)+(indexCard*10)-(self.cardWidth/2),(70)-(indexCard*10)))
                draw_circle(self.screen, self.dealer_hand.get_value(), self.screenWidth/2, 170)

            num_seats = len(self.table.seats)
            seat_space = self.screenWidth / num_seats
            order = True
            for indexSeat,seat in enumerate(self.table.seats):
                splited_hand = len(seat.hands)==2
                for indexHand,hand in enumerate(seat.hands):
                    for indexCard,card in enumerate(hand.cards):
                        image = pygame.transform.scale(pygame.image.load(card.get_asset_path()), (self.cardWidth, self.cardHeight))
                        main_space = (self.screenWidth-((indexSeat+1)*seat_space-(seat_space/2)))
                        if splited_hand:
                            if indexHand == 0:
                                main_space = main_space + (seat_space/4)
                            else:
                                main_space = main_space - (seat_space/4)
                        self.screen.blit(image, (main_space+(indexCard*10)-(self.cardWidth/2),(self.screenHeight-150)-(indexCard*10)))

                    if not hand.done and order:
                        color = (255,165,0)
                        order = False
                    elif not hand.done:
                        color = (0, 255, 0)
                    else:
                        color = (255, 0, 0)
                    draw_circle(self.screen, hand.get_value(), main_space, self.screenHeight-40,color)
                    if hand.doubled:
                        draw_circle(self.screen, "2x", main_space, self.screenHeight-15)


            rect_width = 100
            rect_height = 220
            rect_x = self.screenWidth - rect_width - 10
            rect_y = 10

            font = pygame.font.SysFont("Arial", 12)
            surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 128))  # Şeffaf dikdörtgen
            for i, probability in enumerate(self.deck.probability_of_cards()):
                text = f"{i + 2}: {100 * probability:.2f} %"
                text_surface = font.render(text, True, (255, 255, 255))
                surface.blit(text_surface, (10, 10 + i * 20))
            self.screen.blit(surface, (rect_x, rect_y))

            rect_width = 130
            rect_height = 220
            rect_x = 10
            rect_y = 10

            font = pygame.font.SysFont("Arial", 12)
            surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 128))  # Şeffaf dikdörtgen
            text = f"Games: {self.played_hands}"
            text_surface = font.render(text, True, (255, 255, 255))
            surface.blit(text_surface, (10, 10))

            text = f"Win: {self.win}"
            text_surface = font.render(text, True, (255, 255, 255))
            surface.blit(text_surface, (10, 10 + 20))

            text = f"Lose: {self.loss}"
            text_surface = font.render(text, True, (255, 255, 255))
            surface.blit(text_surface, (10, 10 + 40))

            text = f"Draw: {self.draw}"
            text_surface = font.render(text, True, (255, 255, 255))
            surface.blit(text_surface, (10, 10 + 60))

            text = "-"*20
            text_surface = font.render(text, True, (255, 255, 255))
            surface.blit(text_surface, (10, 10 + 80))

            text = f"Money: {self.money * 100}"
            text_surface = font.render(text, True, (255, 255, 255))
            surface.blit(text_surface, (10, 10 + 100))

            text = f"Earn Rate: {100 * self.earn_money_rate:.2f} %"
            text_surface = font.render(text, True, (255, 255, 255))
            surface.blit(text_surface, (10, 10 + 120))

            text = f"Loss Rate: {100 * self.loss_money_rate:.2f} %"
            text_surface = font.render(text, True, (255, 255, 255))
            surface.blit(text_surface, (10, 10 + 140))
            self.screen.blit(surface, (rect_x, rect_y))


            if self.done:
                rect_width = self.screenWidth / 2.5
                rect_height = self.screenHeight / 3
                rect_x = (self.screenWidth - rect_width) / 2
                rect_y = (self.screenHeight - rect_height) / 2

                if self.reward > 0:
                    color = (0, 255, 0)
                else:
                    color = (255, 0, 0)

                pygame.draw.rect(self.screen, (169,169,169), (rect_x, rect_y, rect_width, rect_height))
                font = pygame.font.Font(None, 36)
                text_surface = font.render("Reward: " + str(self.reward), True, color)
                text_rect = text_surface.get_rect(center=(self.screenWidth / 2, self.screenHeight / 2))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

        elif self.render_mode == 'cmd':
            print("Dealer's Hand: ", self.dealer_hand)
            print("Player's Hand: ", self.playingHand)
            print("0 - Stand")
            print("1 - Hit")
            print("2 - Double")
            print("3 - Split")

            if self.done:
                print("Dealer's Hand: ", self.dealer_hand)
                for indexSeat,seat in enumerate(self.table.seats):
                    for indexHand,hand in enumerate(seat.hands):
                        print(f"Players's {indexSeat+indexHand} Hand: ", hand)
                print("reward =", self.reward)
                print(100*"-")



    def close(self):
        """
        Close the environment.
        """
        if self.screen is not None:
            pygame.quit()


    def get_obs(self):

        if self.envV == 1:
            return {
                "player_sum": self.playingHand.get_value(),
                "dealer_card": self.dealer_hand.cards[0].value,
                "usable_ace": self.playingHand.usable_ace_count(),
                "can_split": 1 if self.playingHand.can_split() else 0,
                "can_double": 1 if self.playingHand.can_double() else 0,
            }
        elif self.envV ==2:
            prob = self.deck.probability_of_cards()
            return {
                "player_sum": self.playingHand.get_value(),
                "dealer_card": self.dealer_hand.cards[0].value,
                "usable_ace": self.playingHand.usable_ace_count(),
                "can_split": 1 if self.playingHand.can_split() else 0,
                "can_double": 1 if self.playingHand.can_double() else 0,

                "two": prob[0]*100,
                "three": prob[1]*100,
                "four":prob[2]*100,
                "five": prob[3]*100,
                "six": prob[4]*100,
                "seven": prob[5]*100,
                "eight": prob[6]*100,
                "nine": prob[7]*100,
                "ten": prob[8]*100,
                "ace": prob[9]*100,
                "last_card": self.deck.last_card.value,

            }
        elif self.envV == 3:

            prob = self.deck.probability_of_cards()
            return {
                "player_sum": self.playingHand.get_value(),
                "dealer_card": self.dealer_hand.cards[0].value,
                "usable_ace": self.playingHand.usable_ace_count(),
                "can_split": 1 if self.playingHand.can_split() else 0,
                "can_double": 1 if self.playingHand.can_double() else 0,

                "prob": np.array(prob,dtype=np.float16),
                "last_card": self.deck.last_card.value,
                "last_second_card": self.deck.last_second_card.value,
                "last_third_card": self.deck.last_third_card.value,
            }

    def distribute_cards(self):
        for k in range(2):
            for i in self.table.seats:
                i.hands[0].add_card(self.deck.hit())


            if k == 1:
                card = self.deck.hit(secret=True)
                card.hidden = True
            else:
                card = self.deck.hit()
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
        if self.at_least_one_hand_not_finalized():
            while self.dealer_hand.get_value() < 17:
                self.dealer_hand.add_card(self.deck.hit())


    def results(self):
        win_chip = 0
        loss_chip = 0
        for seat in self.table.seats:
            for hand in seat.hands:
                self.played_hands += 1
                outcome = hand.is_win(self.dealer_hand)
                if outcome == Outcome.WIN:
                    win_chip += hand.chip.value
                    hand.case = Outcome.WIN
                    self.win += 1
                elif outcome == Outcome.LOSS:
                    loss_chip += hand.chip.value
                    hand.case = Outcome.LOSS
                    self.loss += 1
                elif outcome == Outcome.DRAW:
                    hand.case = Outcome.DRAW
                    self.draw += 1
        return (win_chip - loss_chip) if (win_chip - loss_chip) == 0 else(win_chip - loss_chip)/100




    def get_next_hand(self):
        for seat in self.table.seats:
            for hand in seat.hands:
                if hand.done == False:
                    return hand , seat
        return None

    def at_least_one_hand_not_finalized(self):
        """
        Checks if at least one hand is not finalized.
        :return:
        """
        for seat in self.table.seats:
            for hand in seat.hands:
                if hand.case == Outcome.UNCLEAR:
                    return True
        return False

    def sum_all_chips(self):
        for seat in self.table.seats:
            for hand in seat.hands:
                self.all_money = self.all_money + hand.chip.value / 100

        if self.all_money == 0:
            self.earn_money_rate = 0
            self.loss_money_rate = 0
            return
        if self.money <=0:
            self.earn_money_rate = (((self.all_money - self.money) / 2 ) + self.money) / self.all_money
            self.loss_money_rate = 1 - abs(self.earn_money_rate)
        else:
            self.earn_money_rate = (((self.all_money - self.money) / 2) + self.money) / self.all_money
            self.loss_money_rate = 1 - abs(self.earn_money_rate)