from pacman.src.game import Game
import pygame


def main() -> None:
    packman_game = Game()
    print(pygame.display.Info())
    packman_game.run()


if __name__ == "__main__":
    main()