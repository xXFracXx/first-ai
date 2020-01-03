# imports
import pygame
import pygame.transform as transform
import pygame.image as image
import pygame.mask as mask
import os

# local imports


BASE_IMG = transform.scale2x(image.load(os.path.join("imgs", "base.png")))


class Base:
    VEL = 5
    IMG = BASE_IMG
    WIDTH = BASE_IMG.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
