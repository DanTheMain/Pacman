import random
import sys

import pygame
from pygame.sprite import Group, spritecollide

from pacman.objects import Player, Bot, Wall, GameContext


class Game:
    scale: float = 0.9
    player_speed: int = 5
    player_move_range: int = 2
    player_size: int = 40
    bot_count: int = 4
    bot_size: int = 30
    bot_speed: int = 2
    bot_move_range: int = 3
    wall_width: int = 40
    game_speed: int = 30
    background_color = "white"
    
    def __init__(self) -> None:
        self._game = None
        self._init_game()
        self._screen: pygame.Surface = self._init_display_surface()
        self._context: GameContext = self._compose_context()
        self._clock: pygame.time.Clock = pygame.time.Clock()

    def _init_game(self) -> None:
        if not pygame.get_init():
            pygame.init()
        self._game = pygame

    def _init_display_surface(self) -> pygame.Surface:
        display_info = self._game.display.Info()
        pygame.display.set_mode((display_info.current_w * Game.scale, display_info.current_h * Game.scale))
        return pygame.display.get_surface()

    def _generate_bots(self) -> list[Bot]:
        wall_offset = Game.wall_width * 2
        return [
            Bot(
                topleft_x=random.choice(range(wall_offset, self._screen.get_width() - wall_offset)),
                topleft_y=random.choice(range(wall_offset, self._screen.get_height() - wall_offset)),
                width=Game.bot_size,
                height=Game.bot_size,
                sprite_fname="bot",
            )
            for _ in range(Game.bot_count)
        ]

    def _generate_walls(self) -> list[Wall]:
        h_offset = self._screen.get_width() - Game.wall_width * 2
        y_offset = self._screen.get_height() - Game.wall_width * 2
        return [
            Wall(
                Game.wall_width,
                0,
                h_offset,
                Game.wall_width,
                "wall"),
            Wall(
                Game.wall_width,
                self._screen.get_height() - Game.wall_width,
                h_offset,
                Game.wall_width,
                "wall",
            ),
            Wall(
                0,
                Game.wall_width,
                Game.wall_width,
                y_offset,
                "wall"),
            Wall(
                self._screen.get_width() - Game.wall_width,
                Game.wall_width,
                Game.wall_width,
                y_offset,
                "wall",
            ),
    ]

    def _compose_context(self) -> GameContext:
        return GameContext(
            player=Player(
                topleft_x=self._screen.get_width() // 2,
                topleft_y=self._screen.get_height() // 2,
                width=Game.player_size,
                height=Game.player_size,
                sprite_fname="player",
            ),
            walls=Group(*self._generate_walls()),
            bots=Group(*self._generate_bots()),
        )

    def quit_game(self) -> None:
        if self._game.get_init():
            self._game.quit()
            sys.exit(0)

    def redraw_game(self) -> None:
        self._screen.fill(Game.background_color)
        self._context.walls.draw(self._screen)
        self._context.player.draw(self._screen)
        self._context.bots.draw(self._screen)
        self._game.display.flip()

    def move_bots(self) -> None:
        for bot in self._context.bots:
            old_topleft = bot.rect.topleft
            bot.rect = bot.rect.move(
                random.choice(range(-Game.bot_move_range, Game.bot_move_range + 1)) * Game.bot_speed,
                random.choice(range(-Game.bot_move_range, Game.bot_move_range + 1)) * Game.bot_speed,
            )
            if spritecollide(sprite=bot, group=self._context.walls, dokill=False):
                bot.rect.topleft = old_topleft

    def move_player(self) -> None:
        player = self._context.player
        keys = self._game.key.get_pressed()
        speed = Game.player_speed

        old_topleft = player.rect.topleft
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.rect = player.rect.move(0, -Game.player_move_range * speed)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.rect = player.rect.move(0, Game.player_move_range * speed)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.rect = player.rect.move(-Game.player_move_range * speed, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.rect = player.rect.move(Game.player_move_range * speed, 0)

        if spritecollide(player, self._context.walls, dokill=False):
            player.rect.topleft = old_topleft

        if spritecollide(player, self._context.bots, dokill=True):
            self.quit_game()

    def update_game_clock(self) -> None:
        self._clock.tick(Game.game_speed)

    def run(self) -> None:
        running = True
        while running:
            for event in self._game.event.get():
                if event.type == self._game.QUIT:
                    running = False

            self.redraw_game()
            self.move_bots()
            self.move_player()
            self.update_game_clock()

        self.quit_game()
