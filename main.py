import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()
FPS = pygame.time.Clock()

HEIGHT = 700
WIDTH = 1200
FONT = pygame.font.SysFont('Verdana', 45)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0,0,255)
COLOR_PURPLE = (255,0,255)
main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3


IMAGE_PATH = "goose"
PLAYER_IMAGER = os.listdir(IMAGE_PATH)
PLAYER_SIZE = (20,20)
player = pygame.image.load('1-1.png').convert_alpha()
PLAYER_RECT = pygame.Rect(100,300, *PLAYER_SIZE)

player_move_down = [0,4]
player_move_right = [4,0]
player_move_left = [-4,0]
player_move_top = [0,-4]

def create_enemy():
    enemy_size = (30,30)
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (150,50))
    enemy_rect = pygame.Rect(WIDTH, random.randint(200, 500), *enemy_size)
    enemy_move = [random.randint(-8,-4),0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (20,20)
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (100,150))
    bonus_rect = pygame.Rect(random.randint(200, 800), 1, *bonus_size)
    bonus_move = [0, random.randint(4,6)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = CREATE_ENEMY + 1
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE,200)

enemies = []
bonuses = []
score = 0

image_index = 0

playing = True

while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGER[image_index]))
            image_index +=1
            if image_index >= len(PLAYER_IMAGER):
                image_index = 0


    bg_X1 -= bg_move
    bg_X2 -= bg_move



    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()  



    main_display.blit(bg, (bg_X1,0))
    main_display.blit(bg, (bg_X2,0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and PLAYER_RECT.bottom < HEIGHT:
        PLAYER_RECT = PLAYER_RECT.move(player_move_down)
    if keys[K_RIGHT] and PLAYER_RECT.right < WIDTH:
        PLAYER_RECT = PLAYER_RECT.move(player_move_right)
    if keys[K_UP] and PLAYER_RECT.top > 0:
        PLAYER_RECT = PLAYER_RECT.move(player_move_top)
    if keys[K_LEFT] and PLAYER_RECT.left > 0:
        PLAYER_RECT = PLAYER_RECT.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0],enemy[1])
        
        if PLAYER_RECT.colliderect(enemy[1]):
            playing = False


    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0],bonus[1])
        
        if PLAYER_RECT.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-60, 20))
    main_display.blit(FONT.render(str("score:"), True, COLOR_BLACK), (WIDTH-200, 20))
    
    main_display.blit(player, PLAYER_RECT)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))