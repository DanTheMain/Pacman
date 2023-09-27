import random
import sys

import pygame
from pygame.sprite import Group, spritecollide

from src.objects import Player, Bot, Wall
from resources.helpers import get_screen_resolution


def get_walls_data(screen_width, screen_height, wall_width):
    h_offset = screen_width - wall_width * 2
    y_offset = screen_height - wall_width * 2
    return [
        (wall_width, 0, h_offset, wall_width),
        (wall_width, screen_height - wall_width, h_offset, wall_width),
        (0, wall_width, wall_width, y_offset),
        (screen_width - wall_width, wall_width, wall_width, y_offset),
    ]


def get_bots_data(screen_width, screen_height, bot_num):
    return [
        (
            random.choice(range(Wall.width * 2, screen_width - Wall.width * 2)),
            random.choice(range(Wall.width * 2, screen_height - Wall.width * 2)),
            30,
            30,
            i
        )
        for i in range(1, bot_num + 1)
    ]


def compose_context(screen):
    return {
        "player": Player(
            screen.get_width() // 2, screen.get_height() // 2, 40, 40, "player"
        ),
        "walls": Group(*
                       [
                           Wall(x, y, w, h, "wall")
                           for (x, y, w, h) in get_walls_data(screen.get_width(), screen.get_height(), Wall.width)
                       ]
                       ),
        "bots": Group(*
                      [
                          Bot(x, y, w, h, 'bot')
                          for (x, y, w, h, i) in get_bots_data(screen.get_width(), screen.get_height(), 4)
                      ]
                      ),
    }


def draw_screen(screen, context):
    screen.fill("blue")
    context["player"].draw(screen)
    context["walls"].draw(screen)
    context["bots"].draw(screen)


def handle_player_to_bots_collision(player_context, bots_context) -> None:
    if spritecollide(player_context, bots_context, dokill=False):
        sys.exit(0)


def handle_player_to_wall_collision(player, walls, old_player_position):
    if spritecollide(player, walls, dokill=False):
        player.rect.topleft = old_player_position


def handle_bots_to_walls_collision(bots, walls) -> None:
    for bot in bots:
        if spritecollide(bot, walls, dokill=False):
            bots.remove(bot)


def move_player_by_keys_at_speed(player, keys, speed):
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.rect = player.rect.move(0, -1 * speed)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.rect = player.rect.move(0, speed)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.rect = player.rect.move(-1 * speed, 0)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.rect = player.rect.move(speed, 0)


def move_bots_at_base_speed(bots, speed):
    for bot in bots:
        bot.rect = bot.rect.move(
            random.choice(range(-2, 3)) * speed,
            random.choice(range(-2, 3)) * speed
        )


def PacmanGame():
    pygame.init()
    screen = pygame.display.set_mode(get_screen_resolution(0.9))
    clock = pygame.time.Clock()
    player_speed = 5
    bot_speed = 2
    game_speed = 20

    context = compose_context(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_screen(screen, context)
        pygame.display.flip()

        move_bots_at_base_speed(context["bots"], bot_speed)

        keys = pygame.key.get_pressed()

        old_player_topleft = context["player"].rect.topleft

        move_player_by_keys_at_speed(context["player"], keys, player_speed)

        handle_player_to_wall_collision(context['player'], context['walls'], old_player_topleft)

        handle_bots_to_walls_collision(context['bots'], context['walls'])

        handle_player_to_bots_collision(context['player'], context['bots'])

        clock.tick(game_speed)

    pygame.quit()

