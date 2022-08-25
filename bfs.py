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
FBS = 60
shape = 20
# barrier = np.random.randint(0, shape, size=(shape, 1, 2))
grid = np.zeros((shape, shape))
screen = pygame.display.set_mode((high, width))
path = []
goal = np.random.randint(0, shape, (1, 2))[0]

def bfs(grid, start):
    # if grid[start] == 1:
    #     return []
    m, n = len(grid), len(grid[0])
    queue, visited, steps = deque(), set(), 1
    visited.add(start)
    queue.append(start)
    while queue:
        # print(queue)
        path = queue.popleft()
        if (len(path) == 2):
            x, y = path
        else:
            x, y = path[-1]
        neighbours = [(x-1, y), (x, y+1),
                      (x, y-1), (x+1, y)]
        if (x, y) == (goal[0], goal[1]):
            try:
                path = path[1:]
                path[0] = start
            except:
                print(path)
            return path
        for nx, ny in neighbours:
            if nx >= 0 and nx < m and ny >= 0 and ny < n and (nx, ny) not in visited and grid[nx][ny] == 0:
                new_path = list(path)
                new_path.append((nx, ny))
                queue.append(new_path)
                visited.add((nx, ny))
    return []



def drawLine(screen, color, shape):
    for i in range(0, high, high//shape):
        pygame.draw.line(screen, color, (0, i), (width, i))
        pygame.draw.line(screen, color, (i, 0), (i, high))


def new_goal(goal, snake):
    goal_ = goal
    check = False
    while (list(goal) == list(goal_)) and (list(goal) in snake):
        goal_ = np.random.randint(0, shape, (1, 2))[0]
        # print(goal_)
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
    if path:
        try:
            x, y = path.pop(0)
        except:
            x, y = path
            # print(path)
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
        pygame.draw.rect(screen, (255, 255, 255),
                         (x*high/shape, y*high/shape, high/shape, high/shape))
        snake.pop(0)

    else:
        goal = new_goal(goal, snake)
        snake.append([x_old, y_old])
        start = (int(x_old), int(y_old))
        grid = np.zeros((shape, shape))
        for i in snake:
            grid[i[0], i[1]] = 1
            # print(i[0], i[1])
        # barrier = np.random.randint(0, shape, size=(shape//2, 1, 2))
        # grid = np.zeros((shape, shape))
        # for i in barrier:
        #     grid[i[0][0], i[0][1]] = 1
        start_time = time.time()
        path = bfs(grid, start)
        if not path:
            goal = snake[0]
            path = bfs(grid, start)

        end_time = time.time()
        print(end_time-start_time)

    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            game_play = False
    pygame.display.flip()
    clock.tick(FBS)
pygame.quit()
