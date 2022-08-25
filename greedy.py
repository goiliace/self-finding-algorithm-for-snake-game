import numpy as np
from pygame.locals import *
import pygame
from collections import deque
import time

pygame.init()
width = 800
high = 800
screen_color = (49, 150, 100)
line_color = (255, 255, 255)
FBS =   120
shape = 300
# barrier = np.random.randint(0, shape, size=(shape, 1, 2))
grid = np.zeros((shape, shape))
screen = pygame.display.set_mode((high, width))
path = []
goal = np.random.randint(0, shape, (1, 2))[0]
def greedy_search(start):

    x, y = start
    # print(x, y)
    neighbours = [(x-1, y), (x+1, y),
                    (x, y-1), (x, y+1)]
    min_ = np.inf
    next_max = tuple()
    dist = None
    for nx, ny in neighbours:
        if (nx >= 0 and nx < shape and ny >= 0 and ny < shape) and grid[nx][ny] == 0:
            dist = abs(nx-goal[0])+abs(ny-goal[1])
            if dist < min_:
                min_ = dist
                next_max = (nx, ny)
    return next_max



def drawLine(screen, color, shape):
    for i in range(0, high, high//shape):
        pygame.draw.line(screen, color, (0, i), (width, i))
        pygame.draw.line(screen, color, (i, 0), (i, high))


def new_goal(goal, snake):
    goal_ = goal
    check = False
    while (list(goal) == list(goal_)) or (list(goal_) in snake):
        goal_ = np.random.randint(0, shape, (1, 2))[0]
        # print(goal_)
    # print(goal_, snake)
    return goal_


def draw_snake(x, y):
    pygame.draw.rect(screen, (0, 0, 255),
                     (x*high/shape, y*high/shape, high/shape, high/shape))


def draw_(snake):
    for x, y in snake:
        draw_snake(x, y)


# x, y = 0, 0
game_play = True
clock = pygame.time.Clock()
x_old, y_old = 0, 0

snake = [(0, 0)]
while game_play:
    if (x_old, y_old) != (goal[0], goal[1]):
        x,y = greedy_search((x_old, y_old))
        snake.append([x, y])
        screen.fill((0, 0, 0))
        # draw_snake(x_, y_)
        # for i in snake:
        #     pygame.draw.circle(screen, (255, 0, 0),
        #                        (i[0][0]*high/shape+high/(shape*2),  i[0][1]*high/shape+high/(shape*2)), high/(shape*3))
        # drawLine(screen, line_color, shape)
        pygame.draw.circle(screen, (0, 255, 0), goal*high /
                           shape+high/(shape*2), high/(shape*2))
        x_old, y_old = x, y
        draw_(snake)
        grid = np.zeros((shape, shape))
        snake.pop(0)
        for i in snake:
            grid[i[0], i[1]] = 1
        pygame.draw.rect(screen, (255, 255, 255),
                         (x*high/shape, y*high/shape, high/shape, high/shape))

    else:
        snake.append([x_old, y_old])
        goal = new_goal(goal, snake)
        # start_time = time.time()
        # end_time = time.time()
        # print(end_time-start_time)

    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            game_play = False
    pygame.display.flip()
    clock.tick(FBS)
pygame.quit()
