import os
from typing import Tuple, Any
from dataclasses import dataclass

from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite
from pygame.transform import scale

DEFAULT_IMG_EXT = 'png'


class GameObject(Sprite):
    sprite_filename: str
    topleft_x: int
    topleft_y: int
    width: int
    height: int
    color_key: tuple[int, int, int] = (245, 245, 245)

    def __init__(self, topleft_x: int, topleft_y: int, width: int, height: int, sprite_fname: str):
        super().__init__()
        self.width = width
        self.height = height
        self.sprite_filename = f"{sprite_fname}.{DEFAULT_IMG_EXT if '.' not in sprite_fname else ''}"
        sprite_image_full_path = os.path.join("..", "resources", self.sprite_filename)
        self.image = scale(load(sprite_image_full_path), (self.width, self.height))
        self.image.set_colorkey(self.color_key)
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft_x, topleft_y

    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_collided_with(self, another_object: "GameObject") -> bool:
        return self.rect.colliderect(another_object.rect)


class Player(GameObject):
    pass


class Wall(GameObject):
    pass


class Bot(GameObject):
    pass


@dataclass
class GameContext:
    player: Player
    walls: Any
    bots: Any