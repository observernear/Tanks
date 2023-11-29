import pygame
from random import randint

pygame.init()

HEIGHT, WIDTH = 1000, 1000
TILE_SIZE = 50
FPS = 60
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Tanks")


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

    def update(self):
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

            Bullet(parent=self, px=self.rect.centerx, py=self.rect.centery,
                   dx=dx, dy=dy, damage=self.bulletDamage)

            self.shotTimer = self.shotDelay

        if self.shotTimer > 0:
            self.shotTimer -= 1

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

        x = self.rect.centerx + DIRECTS[self.direct][0] * 60
        y = self.rect.centery + DIRECTS[self.direct][1] * 60

        pygame.draw.line(screen, "white", (self.rect.centerx, self.rect.centery),
                         (x, y), 6)

    def damage(self, value):
        self.HP -= value
        if self.HP <= 0:
            objects.remove(self)
            print(f"{self.color} dead!")


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
                if object != self.parent and object.rect.collidepoint(self.px, self.py):
                    bullets.remove(self)
                    object.damage(self.damage)
                    break

    def draw(self):
        pygame.draw.circle(screen, "yellow", (self.px, self.py), 2)


class Obstacle:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = "obstacle"

        self.rect = pygame.Rect(px, py, size, size)
        self.HP = 1

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(screen, "orange", self.rect)
        pygame.draw.rect(screen, "grey", self.rect, 2)

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


for _ in range(50):
    while True:
        x = randint(0, WIDTH // TILE_SIZE - 1) * TILE_SIZE
        y = randint(0, HEIGHT // TILE_SIZE - 1) * TILE_SIZE
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        fined = False
        for object in objects:
            if rect.colliderect(object.rect):
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

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
