import pygame
import random
from play import Play
from solver import solve

colours = (None, '#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#888888')


def draw_box(x, y, col, screen, modul=30, edge=3, ox=10, oy=10):

    if col is not None:
        c = pygame.Color(col)
        cl = c // pygame.Color(2, 2, 2)
        pygame.draw.rect(screen, c, (ox + x * modul, oy + y * modul, modul, modul), 0)
        pygame.draw.rect(screen, cl, (ox + x * modul, oy + y * modul, modul, modul), edge)


class Boxes:

    def __init__(self):
        self.width = 8
        self.heigth = 20

        random.seed()
        pygame.init()

        self.play = Play(self.width, self.heigth)

        self.screen = pygame.display.set_mode(((self.width * 30) + 20, (self.heigth * 30) + 20))
        self.clock = pygame.time.Clock()

        self.pause = True

        pygame.time.set_timer(pygame.USEREVENT, 500)

    def show(self, field=None, wait=None):
        if field is None:
            field = self.play.field
        self.screen.fill((0, 0, 0))
        for y in range(self.heigth):
            for x in range(self.width):
                draw_box(x, y, colours[field[y][x]], self.screen)

        pygame.display.flip()
        if wait:
            pygame.time.wait(wait)

    def run(self):

        while True:

            pressed = pygame.key.get_pressed()

            alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
            ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

            for event in pygame.event.get():

                # determin if X was clicked, or Ctrl+W or Alt+F4 was used
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.USEREVENT:
                    if not self.pause:
                        self.play.piece_fall()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and ctrl_held:
                        return
                    if event.key == pygame.K_F4 and alt_held:
                        return
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_UP:
                        self.play.piece_rotate('R')
                    if event.key == pygame.K_LEFT:
                        self.play.piece_move('L')
                    if event.key == pygame.K_RIGHT:
                        self.play.piece_move('R')
                    if event.key == pygame.K_DOWN:
                        self.play.piece_fall()
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_s:
                        p = self.pause
                        self.pause = True
                        solve(self.play.ground, self.play.piece, self.play.px, self.play.py, self.show)
                        self.pause = p

                self.show()

            self.clock.tick(50)


if __name__ == "__main__":

    app = Boxes()
    app.run()
