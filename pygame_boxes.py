import pygame
import random
from play import Play


colours = (None, '#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#888888')


def draw_box(x, y, col, screen, modul=30, edge=3, ox=10, oy=10):

    if col is not None:
        c = pygame.Color(col)
        cl = c//pygame.Color(2, 2, 2)
        pygame.draw.rect(screen, c, (ox + x * modul, oy + y * modul, modul, modul), 0)
        pygame.draw.rect(screen, cl, (ox + x * modul, oy + y * modul, modul, modul), edge)


def main():

    random.seed()

    width = 8
    heigth = 20

    play = Play(width, heigth)

    pygame.init()
    screen = pygame.display.set_mode(((width * 30) + 20, (heigth * 30) + 20))
    clock = pygame.time.Clock()

    pygame.time.set_timer(pygame.USEREVENT, 500)

    while True:

        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            # determin if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.USEREVENT:
                play.piece_fall()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_UP:
                    play.piece_rotate('R')
                if event.key == pygame.K_LEFT:
                    play.piece_move('L')
                if event.key == pygame.K_RIGHT:
                    play.piece_move('R')
                if event.key == pygame.K_DOWN:
                    play.piece_fall()

            screen.fill((0, 0, 0))
            for y in range(heigth):
                for x in range(width):
                    draw_box(x, y, colours[play.field[y][x]], screen)

            pygame.display.flip()

        clock.tick(50)


if __name__ == "__main__":

    main()
