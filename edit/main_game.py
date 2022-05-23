"""
PROGRAM: Snake Game
AUTHOR: Cristiliano Júnior
START_CODE: 2202-05-21 22:26
FINISH_CODE: 2202-05-23 12:37
"""
# Standart Importations
from random import randint
import sys
import time
from turtle import width


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
def create_new_food(limite_x: int, limite_y: int, snake: Snake, color: tuple = (255, 0, 0)) -> Food:

    food = Food(color, 0, 0, snake.width, snake.height)

    while True:
        x: int = randint(0, limite_x - food.width)
        y: int = randint(0, limite_y - food.height)

        if (x, y) in snake._positions:
            continue
        else: 
            food.x = x
            food.y = y
            return food

def is_collide(snake: Snake, food: Food) -> bool:
    for vertex in snake.area():
        if (food.x <= vertex[0] <= food.x + food.width) and (food.y <= vertex[1] <= food.y + food.height):
            return True
    return False

def is_collide_with_wall(snake: Snake, width: int, height: int) -> bool:
    for vertex in snake.area():
        if (0 < vertex[0] < width) and (0 < vertex[1] < height):
            return False
    return True

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
status: str = 'ALIVE'


# SYSTEM AND UI
score: int = 0
font = pygame.font.Font('Consola.ttf', 25)


# MAIN LOOP
while True:
    # Clear Canvas to next frame
    screen.fill(CONFIGS['screen']['background_color'])
    
    font_text = font.render(f'SCORE: {score}', True, (255, 255, 255))
    score_rect = font_text.get_rect()
    
    if is_collide_with_wall(objects_queue[0], CONFIGS['screen']['width'], CONFIGS['screen']['height']) == True:
        status = 'GAMEOVER'
        screen.fill(CONFIGS['screen']['background_color'])
        font_text_gameover = font.render(f'GAMEOVER - SCORE: {score}', True, (255, 255, 255))
        gameover_rect = font_text.get_rect()
        gameover_rect.center = ((CONFIGS['screen']['width'] - gameover_rect.width)/2, (CONFIGS['screen']['height']  - gameover_rect.height)/2)
        screen.blit(font_text_gameover, gameover_rect)

    if objects_queue[1] == None:
        objects_queue[1] = create_new_food(CONFIGS['screen']['width'], CONFIGS['screen']['height'], objects_queue[0])
    elif is_collide(objects_queue[0], objects_queue[1]) == True:
        score += 1
        delta /= 1.05
        objects_queue[0].add_shape()
        objects_queue[1] = create_new_food(CONFIGS['screen']['width'], CONFIGS['screen']['height'], objects_queue[0])


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

    if status != 'GAMEOVER':
        # Snake Movement apply
        objects_queue[0].move()

        for game_object in objects_queue:
            game_object.draw(screen)

        # DRAW UI
        
        screen.blit(font_text, score_rect)

    pygame.display.flip()

    time.sleep(delta)

