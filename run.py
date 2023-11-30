import pygame
from random import randint

pygame.init()

HEIGHT, WIDTH = 1024, 1024
TILE_SIZE = 64
FPS = 60
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fontUI = pygame.font.Font(None, 30)
fontBig = pygame.font.Font(None, 70)

pygame.display.set_caption("Tanks")

imgObstacle = pygame.image.load("obstacle.png")
imgTanks = [
    pygame.image.load('images/tank1.png'),
    pygame.image.load('images/tank2.png'),
    pygame.image.load('images/tank3.png'),
    pygame.image.load('images/tank4.png'),
    pygame.image.load('images/tank5.png'),
    pygame.image.load('images/tank6.png'),
    pygame.image.load('images/tank7.png'),
    pygame.image.load('images/tank8.png'),]
imgBangs = [
    pygame.image.load('images/bang1.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang3.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang1.png'),]


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

                text = fontUI.render(str(object.rank), 1, 'black')
                rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                screen.blit(text, rect)

                text = fontUI.render(str(object.HP), 1, object.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                screen.blit(text, rect)
                i += 1


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

    def update(self):
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


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.type = "bullet"
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for object in objects:
                if object != self.parent and object.type != 'explosion' and object.rect.collidepoint(self.px, self.py):
                    bullets.remove(self)
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

    def update(self):
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

    def update(self):
        pass

    def draw(self):
        screen.blit(imgObstacle, self.rect)

    def damage(self, value):
        self.HP -= value
        if self.HP <= 0:
            objects.remove(self)


objects = []
bullets = []

Tank(100, 100, 0, "Blue", (pygame.K_a, pygame.K_d,
     pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank(700, 100, 1, "Red", (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,
     pygame.K_DOWN, pygame.K_x))
ui = UI()

for _ in range(110):
    while True:
        x = randint(0, WIDTH // TILE_SIZE - 1) * TILE_SIZE
        y = randint(1, HEIGHT // TILE_SIZE - 1) * TILE_SIZE
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        fined = False
        for object in objects:
            if rect.colliderect(object):
                fined = True
        if not fined:
            break
    Obstacle(x, y, TILE_SIZE)

play = True
while play:
    for event in pygame.event.get():
        if pygame.QUIT == event.type:
            play = False

    keys = pygame.key.get_pressed()

    for object in objects:
        object.update()
    for bullet in bullets:
        bullet.update()
    screen.fill((0, 0, 0))
    for bullet in bullets:
        bullet.draw()
    for object in objects:
        object.draw()
    ui.draw()

    t = 0
    for obj in objects:
        if obj.type == 'tank':
            t += 1
            tankWin = obj

    if t == 1:
        bullets.clear()
        text = fontBig.render('ПОБЕДИЛ', 1, 'white')
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(text, rect)

        pygame.draw.rect(screen, tankWin.color,
                         (WIDTH // 2 - 100, HEIGHT // 2, 200, 200))

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
