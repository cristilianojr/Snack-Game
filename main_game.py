"""
PROGRAM: Snake Game
AUTHOR: Cristiliano Júnior
START_CODE: 2202-05-21 22:26
FINISH_CODE:
"""
# Standart Importations
from random import randint
import sys
import time


# Pygame Importations
import pygame
import pygame.event as EVENT
from pygame import Surface

# Game Imports
from configs import CONFIGS
from models import Food, Snake

# This part of code will start the funcitons of pygame.
pygame.init()

# Setting Surface
screen: Surface = pygame.display.set_mode((CONFIGS['screen']['width'], CONFIGS['screen']['height']))


# Generator Food
def create_new_food(screen: Surface, limite_x: int, limite_y: int, snake: Snake, color: tuple = (255, 0, 0)) -> Food:

    while True:
        x: int = randint(0, limite_x)
        y: int = randint(0, limite_y)

        if (x, y) in snake._positions:
            continue
        else: 
            return Food(color, x, y, snake.width, snake.height)

def is_collide(snake: Snake, food: Food) -> bool:
    for vertex in snake.area():
        if (food.x <= vertex[0] <= food.x + food.width) and (food.y <= vertex[1] <= food.y + food.height):
            return True
    
    return False
        

# Globals Vars
objects_queue: list[Snake, Food] = [
    Snake((255, 255, 255), 30, 30, 10, 10),
    None,
]
"""
The Objects Queue are all objects then will draw in the canvas
"""
current_key: int = pygame.K_d
delta: float = 0.1
counter_food: int = 0


# MAIN LOOP
while True:
    # Clear Canvas to next frame
    screen.fill(CONFIGS['screen']['background_color'])

    if objects_queue[1] == None:
        objects_queue[1] = create_new_food(screen, CONFIGS['screen']['width'], CONFIGS['screen']['height'], objects_queue[0])
    elif is_collide(objects_queue[0], objects_queue[1]) == True:
        counter_food += 1
        delta /= 1.05
        objects_queue[0].add_shape()
        objects_queue[1] = create_new_food(screen, CONFIGS['screen']['width'], CONFIGS['screen']['height'], objects_queue[0])
        print(counter_food)


    for event in EVENT.get():
        match event.type:
            case pygame.QUIT:
                sys.exit()

            case pygame.KEYDOWN:
                snake: Snake = objects_queue[0]

                if event.key == pygame.K_d and not current_key in (pygame.K_a, pygame.K_d):
                    snake.direction = [1, 0]

                if event.key == pygame.K_a and not current_key in (pygame.K_d, pygame.K_a):
                    snake.direction = [-1, 0]

                if event.key == pygame.K_w and not current_key in (pygame.K_s, pygame.K_w):
                    snake.direction = [0, -1]

                if event.key == pygame.K_s and not current_key in (pygame.K_w, pygame.K_s):
                    snake.direction = [0, 1]

                current_key = event.key

    # Snake Movement apply
    objects_queue[0].move()

    for game_object in objects_queue:
        game_object.draw(screen)

    pygame.display.flip()

    time.sleep(delta)

