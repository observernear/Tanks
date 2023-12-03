import pygame
import os
from random import randint

pygame.init()
#
HEIGHT, WIDTH = 1024, 1024
TILE_SIZE = 64
BONUS_SIZE = TILE_SIZE // 2
FPS = 60
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
BONUSCD = 54

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fontUI = pygame.font.Font(None, 30)
fontBig = pygame.font.Font(None, 70)
cursor_image = pygame.image.load(os.path.join("data", "cursor.png"))
cursor_image = pygame.transform.scale(cursor_image, (30, 30))
cursor_rect = cursor_image.get_rect()

pygame.mouse.set_visible(False)
pygame.display.set_caption("Tanks")

imgObstacle = pygame.image.load("data/obstacle.png")
imgTanks = [
    pygame.image.load('data/tank1.png'),
    pygame.image.load('data/tank2.png'),
    pygame.image.load('data/tank3.png'),
    pygame.image.load('data/tank4.png'),
    pygame.image.load('data/tank5.png'),
    pygame.image.load('data/tank6.png'),
    pygame.image.load('data/tank7.png'),
    pygame.image.load('data/tank8.png')]
imgBangs = [
    pygame.image.load('data/bang1.png'),
    pygame.image.load('data/bang2.png'),
    pygame.image.load('data/bang3.png'),
    pygame.image.load('data/bang2.png'),
    pygame.image.load('data/bang1.png')]
imgBonuses = [
    pygame.image.load('data/bonus_helmet.png'),
    pygame.image.load('data/bonus_tank.png')]
imgNone = pygame.image.load('data/block_none.png')
imgMain = pygame.image.load('main_img.png')

soundStart = pygame.mixer.Sound('sounds/level_start.mp3')
soundShot = pygame.mixer.Sound('sounds/shot.wav')
soundDestroy = pygame.mixer.Sound('sounds/destroy.wav')
soundDead = pygame.mixer.Sound('sounds/dead.wav')
soundFinish = pygame.mixer.Sound('sounds/level_finish.mp3')

objects = []
bullets = []
bonuses = []


class main_menu:
    def __init__(self):
        self.image = imgMain
        self.rect = self.image.get_rect()
        self.screen = pygame.display.set_mode(self.rect.size)

    def draw(self):
        self.screen.blit(self.image, (0, 0))


class Tank:
    def __init__(self, px, py, direct, color, keyList):
        objects.append(self)
        self.type = "tank"

        self.rect = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
        self.color = color
        self.direct = direct
        self.moveSpeed = 2
        self.HP = 5

        self.shotTimer = 0
        self.shotDelay = 60
        self.bulletDamage = 1
        self.bulletSpeed = 7

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keyFIRE = keyList[4]

        self.rank = randint(0, 7)
        self.image = pygame.transform.rotate(
            imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, keys):
        self.image = pygame.transform.rotate(
            imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() + 10, self.image.get_height() + 10))
        self.rect = self.image.get_rect(center=self.rect.center)

        oldx, oldy = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2

        if keys[self.keyFIRE] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery,
                   dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0:
            self.shotTimer -= 1

        for object in objects:
            if object != self and object.type != 'explosion':
                if self.rect.colliderect(object) or self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 64 or self.rect.y > HEIGHT:
                    self.rect.topleft = oldx, oldy

    def draw(self):
        screen.blit(self.image, self.rect)

    def damage(self, value):
        self.HP -= value
        if self.HP <= 0:
            objects.remove(self)
            soundDead.play()


class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for object in objects:
            if object.type == 'tank':
                pygame.draw.rect(screen, object.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(object.bulletDamage), 1, 'black')
                rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                screen.blit(text, rect)

                text = fontUI.render(str(object.HP), 1, object.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                screen.blit(text, rect)
                i += 1


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.type = "bullet"
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage
        soundShot.play()

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for object in objects:
                if object != self.parent and object.type != 'explosion' and object.rect.collidepoint(self.px, self.py):
                    bullets.remove(self)
                    soundDestroy.play()
                    object.damage(self.damage)
                    Explosion(self.px, self.py)
                    break

    def draw(self):
        pygame.draw.circle(screen, "yellow", (self.px, self.py), 2)


class Explosion:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'explosion'

        self.px, self.py = px, py
        self.frame = 0

    def update(self, keys):
        self.frame += 0.2
        if self.frame >= 5:
            objects.remove(self)

    def draw(self):
        img = imgBangs[int(self.frame)]
        rect = img.get_rect(center=(self.px, self.py))
        screen.blit(img, rect)


class Obstacle:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = "obstacle"

        self.rect = pygame.Rect(px, py, size, size)
        self.HP = 1

    def update(self, keys):
        pass

    def draw(self):
        screen.blit(imgObstacle, self.rect)

    def damage(self, value):
        self.HP -= value
        if self.HP <= 0:
            objects.remove(self)


class Bonus:
    def __init__(self, px, py, bonusNum):
        bonuses.append(self)

        self.rect = pygame.Rect(px, py, BONUS_SIZE, BONUS_SIZE)
        self.bonusNum = bonusNum
        self.image = pygame.transform.scale(
            imgBonuses[self.bonusNum], (BONUS_SIZE, BONUS_SIZE))
        self.frame = 0

    def update(self):
        self.frame += 0.1
        for object in objects:
            if object.type == 'tank' and object.rect.colliderect(self.rect):
                bonuses.remove(self)
                if self.bonusNum == 0:
                    object.HP += 1
                elif self.bonusNum == 1:
                    if object.moveSpeed < 5:
                        object.moveSpeed += 1
                    if object.bulletDamage < 3:
                        object.bulletDamage += 1

        if self.frame >= 54:
            bonuses.remove(self)

    def draw(self):
        if self.frame <= 24:
            screen.blit(self.image, self.rect)
        elif 3 >= int(self.frame) % 6 >= 0:
            screen.blit(self.image, self.rect)
