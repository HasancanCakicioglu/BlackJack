import time
from typing import SupportsFloat, Any, Optional, Union
import gymnasium as gym
import pygame
from gymnasium.core import ActType, ObsType, RenderFrame
from gymnasium.vector.utils import spaces
from pygame import QUIT

from deck import Deck
from table import Table
from seat import Seat
from hand import Hand, Outcome
from chip import Chip


class BlackJackEnv(gym.Env):
    def __init__(self):
        self.screen = None
        self.clock = None

        self.deck = Deck()
        self.deck.shuffle()
        self.table = Table()
        self.table = self.create_objects(self.table, 7, [100,100,100,100,100,100,100])
        self.dealer_hand = Hand(chip=Chip(0))
        self.playingHand = None
        self.done = False
        self.distribute_cards()
        self.reward = 0
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
            if not hand.double_down(self.deck):
                print("You need exactly 2 cards to double down.")
        elif action == 3:
            if not seat.split_hand():
                print("You need 1 hands to split.")
            else:
                seat.hands[0].add_card(self.deck.hit())
                seat.hands[1].add_card(self.deck.hit())

        self.playingHand = hand
        hand = self.get_next_hand()

        if hand is None:
            self.dealer_play()
            self.reward = self.results()
            self.done = True
            return self.get_obs(), self.reward, True, True, {}

        return self.get_obs(), 0, False, False, {}


    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict[str, Any]] = None,
        full_reset: bool = True,
    ) -> tuple[ObsType, dict[str, Any]]:

        if full_reset:
            self.deck = Deck()
            self.deck.shuffle()
        else:
            if self.deck.needs_shuffle():
                self.deck = Deck()
                self.deck.shuffle()

        self.table = Table()

        self.table = self.create_objects(self.table, 7, [100,100,100,100,100,100,100])
        self.done = False
        self.dealer_hand = Hand(chip=Chip(0))
        self.playingHand = self.get_next_hand()[0]
        self.distribute_cards()
        return self.get_obs(), {}

    def render(self, mode="human"):
        def draw_circle(window, value, x, y,color=(0, 0, 0)):
            circle_radius = 12
            circle_color = color
            font = pygame.font.SysFont(None, 24)
            text_color = (255, 255, 255)  # Beyaz renk

            pygame.draw.circle(window, circle_color, (int(x), int(y)), circle_radius)

            text_surface = font.render(str(value), True, text_color)
            text_rect = text_surface.get_rect()
            text_rect.center = (int(x), int(y))

            window.blit(text_surface, text_rect)

        if mode == 'human':
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
            self.clock.tick(60)


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

            rect_width = 100
            rect_height = 220
            rect_x = self.screenWidth - rect_width - 10
            rect_y = 10

            font = pygame.font.SysFont("Arial", 12)
            surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 128))  # Şeffaf dikdörtgen
            for i, probability in enumerate(self.deck.probability_of_cards()):
                text = f"{i + 2}: {probability:.2f} %"
                text_surface = font.render(text, True, (255, 255, 255))
                surface.blit(text_surface, (10, 10 + i * 20))
            self.screen.blit(surface, (rect_x, rect_y))

            if self.done:
                rect_width = self.screenWidth / 2.5
                rect_height = self.screenHeight / 3
                rect_x = (self.screenWidth - rect_width) / 2
                rect_y = (self.screenHeight - rect_height) / 2

                if self.reward > 0:
                    color = (0, 255, 0)  # Yeşil
                else:
                    color = (255, 0, 0)  # Kırmızı

                pygame.draw.rect(self.screen, (169,169,169), (rect_x, rect_y, rect_width, rect_height))
                font = pygame.font.Font(None, 36)  # Varsayılan font ve boyut
                text_surface = font.render("Reward: " + str(self.reward), True, color)  # Beyaz renkli metin
                text_rect = text_surface.get_rect(center=(self.screenWidth / 2, self.screenHeight / 2))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()


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
        if self.at_least_one_hand_not_finalized():
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

    def at_least_one_hand_not_finalized(self):
        for seat in self.table.seats:
            for hand in seat.hands:
                if hand.case == Outcome.UNCLEAR:
                    return True
        return False


