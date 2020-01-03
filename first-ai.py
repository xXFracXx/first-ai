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

GEN = 0

BG_IMG = transform.scale2x(image.load(os.path.join("imgs", "bg.png")))
STAT_FOMT = pygame.font.SysFont("consolas", 25)


def draw_window(win, birds, pipes, base, score, gen):
    # background
    win.blit(BG_IMG, (0, 0))

    # pipes
    for pipe in pipes:
        pipe.draw(win)

    # base
    base.draw(win)

    # bird
    for bird in birds:
        bird.draw(win)

    # score
    score_text = STAT_FOMT.render("SCORE: " + str(score), 1, (255, 255, 255))
    win.blit(score_text, (WIN_WIDTH - 10 - score_text.get_width(), 10))

    # score
    gen_text = STAT_FOMT.render("GEN: " + str(gen), 1, (255, 255, 255))
    win.blit(gen_text, (10, 10))

    # update
    pygame.display.update()


def main(genomes, config):
    global GEN
    GEN += 1

    # inits
    score = 0
    birds = []
    base = base_c.Base(730)
    pipes = [pipe_c.Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(bird_c.Bird(230, 350))
        g.fitness = 0
        ge.append(g)

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
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(
                bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        # pipe logic
        rem = []
        add_pipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(pipe_c.Pipe(600))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)

        # bird move
        # bird.move()

        # base move
        base.move()

        draw_window(win, birds, pipes, base, score, GEN)

        # if score > 50:
        #     break


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    winner = p.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")
    run(config_path)
