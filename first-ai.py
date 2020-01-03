# pylint: disable=no-member
# imports
import pygame
import pygame.transform as transform
import pygame.image as image
import neat
import time
import os
import random

# local imports
import bird as bird_c
import pipe as pipe_c
import base as base_c

# inits
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BG_IMG = transform.scale2x(image.load(os.path.join("imgs", "bg.png")))
STAT_FOMT = pygame.font.SysFont("consolas", 25)


def draw_window(win, bird, pipes, base, score):
    # background
    win.blit(BG_IMG, (0, 0))

    # pipes
    for pipe in pipes:
        pipe.draw(win)

    # base
    base.draw(win)

    # bird
    bird.draw(win)

    # score
    score_text = STAT_FOMT.render("SCORE: " + str(score), 1, (255, 255, 255))
    win.blit(score_text, (WIN_WIDTH - 10 - score_text.get_width(), 10))

    # update
    pygame.display.update()


def main():
    # inits
    score = 0
    bird = bird_c.Bird(230, 350)
    base = base_c.Base(730)
    pipes = [pipe_c.Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # clock
    clock = pygame.time.Clock()

    # game loop
    run = True
    while run:
        # FPS
        clock.tick(30)

        # quit logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # pipe logic
        rem = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(pipe_c.Pipe(600))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730:
            pass

        # bird move
        # bird.move()

        # base move
        base.move()

        draw_window(win, bird, pipes, base, score)

    pygame.quit()
    quit()


main()
