import pygame
import random
import math
from pygame import mixer

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.display.set_caption("Christmas Chaos")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('snow.png')

# background music
mixer.music.load('414673__lena-orsa__a-christmas-tale.mp3')
mixer.music.play(-1)

# level
level = 1
level_up = False

# player
playerImg = pygame.image.load('santa-claus.png')


class Player(object):
    def __init__(self, x, y, x_change):
        self.x = x
        self.y = y
        self.x_change = x_change



class Enemy(object):
    def __init__(self, x, y, x_change, y_change):
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change


# enemy
enemyImg = pygame.image.load('grinch.png')
num_enemies = 12
enemies = []
for i in range(num_enemies):
    new_enemy = Enemy(random.randint(0, 735), 80, 1, 50)
    enemies.append(new_enemy)


class Boss(object):
    def __init__(self, x, y, hp, x_change):
        self.x = x
        self.y = y
        self.hp = hp
        self.x_change = x_change


class Bullet(object):
    def __init__(self, x, y, y_change, state):
        self.x = x
        self.y = y
        self.y_change = y_change
        self.state = state


rockImg = pygame.image.load('coal.png')
rock_launch = False


class Rock(object):
    def __init__(self, x, y, y_change):
        self.x = x
        self.y = y
        self.y_change = y_change

    def draw(self, screen):
        screen.blit(rockImg, (self.x, self.y))


santaImg = pygame.image.load('santaIcon.png')


class Santa(object):
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp

    def draw(self, screen):
        screen.blit(santaImg, (self.x, self.y))
        pygame.draw.rect(screen, (255, 0, 0), (self.x + 80, self.y + 30, 50, 10))
        pygame.draw.rect(screen, (0, 128, 0), (self.x + 80, self.y + 30, 50 * (self.hp / 5), 10))

# bullet
bulletImg = pygame.image.load('candy-cane.png')

# game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# missile
missileImg = []
missileX = []
missileY = []
missileY_change = []


def game_over_test():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def game_won():
    won_text = over_font.render('YOU WIN', True, (255, 255, 0))
    screen.blit(won_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def show_boss(x, y, hp):
    bossImg = pygame.image.load('grinchboss.png')
    if 64 >= hp > 32:
        bossImg = pygame.image.load('grinch3.png')
    elif hp <= 32:
        bossImg = pygame.image.load('grinchlast.png')
    screen.blit(bossImg, (x, y))
    pygame.draw.rect(screen, (255, 0, 0), (x + 20, y - 5, 50, 10))
    pygame.draw.rect(screen, (0, 128, 0), (x + 20, y - 5, 50 * (hp / 100), 10))


def show_santa(x, y, hp):
    santaImg = pygame.image.load('santaIcon.png')
    screen.blit(santaImg, (x, y))
    pygame.draw.rect(screen, (255, 0, 0), (x + 100, y - 50, 50, 10))
    pygame.draw.rect(screen, (0, 128, 0), (x + 100, y - 50, 50 * (hp / 100), 10))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    bullet.state = 'fire'
    screen.blit(bulletImg, (x + 15, y - 50))


def isCollision(object1_x, object1_y, object2_x, object2_y, hitbox):
    dist = math.sqrt(math.pow(object1_x - object2_x, 2) + math.pow(object1_y - object2_y, 2))
    if object1_x > object2_x:
        if dist < hitbox:
            return True
        else:
            return False
    else:
        if dist < 2 * hitbox:
            return True
        else:
            return False


def missile(x, y, i):
    screen.blit(missileImg[i], (x, y))


player1 = Player(370, 480, 0)
boss = Boss(690, 10, 100, 0)
bullet = Bullet(0, 480, 4, 'ready')
rocks = []
numRocks = math.floor(width / 100)
santa = Santa(0, 530, 5)
take_dmg = mixer.Sound('dmg.wav')
game_over = False
waitImg = pygame.image.load('wait_page.png')
# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.x_change = -2.5
            if event.key == pygame.K_RIGHT:
                player1.x_change = 2.5
            if event.key == pygame.K_SPACE:
                if bullet.state == 'ready':
                    bullet_sound = mixer.Sound('427595__michorvath__20-gauge-shotgun-gunshot.wav')
                    bullet_sound.play()
                    bullet.x = player1.x
                    fire_bullet(player1.x, bullet.y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player1.x_change = 0

    player1.x += player1.x_change
    if player1.x <= 0:
        player1.x = 0
    elif player1.x >= 736:
        player1.x = 736

    # Level 1
    if game_over == False:
        if boss.hp > 64:
            for i in range(num_enemies):
                # game over
                if enemies[i].y > 600:
                    santa.hp -= 1

                enemies[i].x += enemies[i].x_change
                if enemies[i].x <= 0:
                    enemies[i].x_change = 1
                    enemies[i].y += enemies[i].y_change
                elif enemies[i].x >= 736:
                    enemies[i].x_change = -1
                    enemies[i].y += enemies[i].y_change

                # collision
                collision = isCollision(bullet.x, bullet.y, enemies[i].x, enemies[i].y, 20)
                if collision:
                    explosion_sound = mixer.Sound('344276__nsstudios__laser3.wav')
                    explosion_sound.play()
                    bullet.y = 480
                    bullet.state = 'ready'
                    boss.hp -= 3
                    enemies[i].x = random.randint(0, 735)
                    enemies[i].y = -100
                    enemies[i].x_change = 0
                enemy(enemies[i].x, enemies[i].y)

        # level 2
        elif boss.hp > 32:
            if not level_up:
                laugh_sound = mixer.Sound('laugh.wav')
                laugh_sound.play()
                boss.x_change = 2
                level_up = True

            if boss.x <= 0:
                boss.x_change = 1.5
            elif boss.x >= 736:
                boss.x_change = -1.5

            rotate = random.randint(1, 2)
            if boss.x % 100 == 0 and rotate == 2:
                boss.x_change *= -1
                missileImg.append(pygame.image.load('giftbox.png'))
                missileX.append(boss.x)
                missileY.append(20)
                missileY_change.append(2.5)
            for i in range(len(missileImg)):
                missileY[i] += missileY_change[i]
                missile(missileX[i], missileY[i], i)
                collect = isCollision(player1.x, player1.y, missileX[i], missileY[i], 25)
                if collect:
                    success = mixer.Sound('collect.wav')
                    success.play()
                    missileX[i] = 2000
                    boss.hp -= 4
                if 735 >= missileX[i] >= 0 and missileY[i] == 600:
                    santa.hp -= 1
            boss.x += boss.x_change
            if boss.hp == 32:
                level_up = False

        # lv3
        else:
            boss.x_change = 0
            boss.x = 690
            boss.y = 10
            if not level_up:
                laugh_sound = mixer.Sound('donotmess.mp3')
                laugh_sound.play()
                boss.x_change = 2
                level_up = True
            if not rock_launch:
                opening = random.randint(1, 7)
                for i in range(1, numRocks):
                    if i != opening:
                        rock = Rock(i * 100 - 50, boss.y + 50, 1.5)
                        rocks.append(rock)
                rock_launch = True
            for j in range(len(rocks)):
                rocks[j].y += rocks[j].y_change
                Rock.draw(rocks[j], screen)
                hit = isCollision(rocks[j].x, rocks[j].y, player1.x, player1.y, 50)
                if hit:
                    santa.hp -= 1
                    take_dmg.play()
                    rocks[0].y = 600

            if rock_launch is True and rocks[0].y == 600:
                boss.hp -= 4
                rocks.clear()
                rock_launch = False

        if bullet.y <= 0:
            bullet.y = 480
            bullet.state = 'ready'

        if bullet.state == 'fire':
            fire_bullet(bullet.x, bullet.y)
            bullet.y -= bullet.y_change

    if game_over == False:
        player(player1.x, player1.y)
        show_boss(boss.x, boss.y, boss.hp)
        Santa.draw(santa, screen)
    if boss.hp <= 0:
        game_over = True
        game_won()
        if boss.hp == 0:
            win_sound = mixer.Sound('wingame.mp3')
            win_sound.play()
            boss.hp -= 1
    if santa.hp <= 0:
        game_over = True
        game_over_test()
        if santa.hp == 0:
            lose_sound = mixer.Sound('lose.wav')
            lose_sound.play()
            santa.hp -= 1
    pygame.display.update()
