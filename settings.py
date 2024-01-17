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
# os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
fontUI = pygame.font.Font(None, 30)
fontBig = pygame.font.Font(None, 70)
fontMegaBig = pygame.font.Font(None, 170)
cursor_image = pygame.image.load(os.path.join("data", "cursor.png"))
cursor_image = pygame.transform.scale(cursor_image, (30, 30))
cursor_rect = cursor_image.get_rect()

pygame.mouse.set_visible(False)
pygame.display.set_caption("Tanks")

imgObstacle = pygame.image.load("data/obstacle.png")
imgArmor = pygame.image.load("data/block_armor.png")
imgBrick = pygame.image.load("data/block_brick.png")
imgIce = pygame.image.load("data/block_ice.png")
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
imgMain = pygame.image.load('main_img.jpg')
imgMute = pygame.image.load('images/mute.png')
imgUnmute = pygame.image.load('images/unmute.png')
soundStart = pygame.mixer.Sound('sounds/level_start.mp3')
soundShot = pygame.mixer.Sound('sounds/shot.wav')
soundDestroy = pygame.mixer.Sound('sounds/destroy.wav')
soundDead = pygame.mixer.Sound('sounds/dead.wav')
soundFinish = pygame.mixer.Sound('sounds/level_finish.mp3')
soundClick = pygame.mixer.Sound('sounds/click.wav')

objects = []
bullets = []
bonuses = []
isMuted = False


class main_menu:
    def draw_text(self, screen, text, font, color, x, y, opacity=255):

        text_surface = font.render(text, True, color)
        text_surface.set_alpha(opacity)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)

    def __init__(self, ch):
        self.image = imgMain
        self.rect = self.image.get_rect()
        self.screen = pygame.display.set_mode(self.rect.size)
        self.main_font = pygame.font.Font("fonts/TheDark-pr2Z.ttf", 290)
        self.main_font1 = pygame.font.Font("fonts/TheDark-pr2Z.ttf", 300)
        self.main_font2 = pygame.font.Font("fonts/TheDark-pr2Z.ttf", 270)
        self.sub_font = pygame.font.Font(
            "fonts/ZilapSleepGrunge-zLnX.ttf", 100)
        self.restart = ch

        self.buff = [0, 10, 20, 30, 40]

    def click(self, pos):
        if 1024-100 < pos[0] < 1024 and 10 < pos[1] < 140:
            soundClick.play()
            global isMuted
            isMuted = not isMuted
            if isMuted:
                soundDead.set_volume(0)
                soundFinish.set_volume(0)
                soundShot.set_volume(0)
                soundStart.set_volume(0)
                soundDestroy.set_volume(0)
                soundClick.set_volume(0)
            else:
                soundDead.set_volume(1)
                soundFinish.set_volume(1)
                soundShot.set_volume(1)
                soundStart.set_volume(1)
                soundDestroy.set_volume(1)
                soundClick.set_volume(1)
        elif 100 < pos[0] < 495 and 835 < pos[1] < 935:
            soundClick.play()
            self.restart("")

        if 540 < pos[0] < 940 and 835 < pos[1] < 935:
            soundClick.play()
            objects.clear()
            bullets.clear()
            bonuses.clear()
            self.restart("restart")

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        # Mute button
        pygame.draw.rect(self.screen, 'black', (1024-115, 5, 110, 110), 5, 13)
        if isMuted:
            self.screen.blit(imgMute, (1024-100, 10))
        else:
            self.screen.blit(imgUnmute, (1024-100, 10))
        # Text animation
        tick = pygame.time.get_ticks()
        clock.tick(FPS)
        for i in range(4):
            self.buff[i] = self.buff[i+1]
        self.buff[4] = self.buff[3] + \
            (randint(1, 10)/10 if self.buff[3] <
             randint(50, 150) else randint(-10, -1)/10)
        ###
        self.draw_text(self.screen, "T", self.main_font1,
                       (0, 0, 0), WIDTH // 2-290, HEIGHT // 2-20)
        self.draw_text(self.screen, "A", self.main_font1,
                       (0, 0, 0), WIDTH // 2-170, HEIGHT // 2-20)
        self.draw_text(self.screen, "N", self.main_font1,
                       (0, 0, 0), WIDTH // 2-10, HEIGHT // 2-20)
        self.draw_text(self.screen, "K", self.main_font1,
                       (0, 0, 0), WIDTH // 2+160, HEIGHT // 2-20)
        self.draw_text(self.screen, "S", self.main_font1,
                       (0, 0, 0), WIDTH // 2+325, HEIGHT // 2-20)

        self.draw_text(self.screen, "T", self.main_font2,
                       (0, 0, 0), WIDTH // 2-290, HEIGHT // 2-20)
        self.draw_text(self.screen, "A", self.main_font2,
                       (0, 0, 0), WIDTH // 2-170, HEIGHT // 2-20)
        self.draw_text(self.screen, "N", self.main_font2,
                       (0, 0, 0), WIDTH // 2-10, HEIGHT // 2-20)
        self.draw_text(self.screen, "K", self.main_font2,
                       (0, 0, 0), WIDTH // 2+160, HEIGHT // 2-20)
        self.draw_text(self.screen, "S", self.main_font2,
                       (0, 0, 0), WIDTH // 2+325, HEIGHT // 2-20)

        ###
        self.draw_text(self.screen, "T", self.main_font, (int(self.buff[0]), int(
            self.buff[0]), int(self.buff[0])), WIDTH // 2-290, HEIGHT // 2-20)
        self.draw_text(self.screen, "A", self.main_font, (int(self.buff[1]), int(
            self.buff[1]), int(self.buff[1])), WIDTH // 2-170, HEIGHT // 2-20)
        self.draw_text(self.screen, "N", self.main_font, (int(self.buff[2]), int(
            self.buff[2]), int(self.buff[2])), WIDTH // 2-10, HEIGHT // 2-20)
        self.draw_text(self.screen, "K", self.main_font, (int(self.buff[3]), int(
            self.buff[3]), int(self.buff[3])), WIDTH // 2+160, HEIGHT // 2-20)
        self.draw_text(self.screen, "S", self.main_font, (int(self.buff[4]), int(
            self.buff[4]), int(self.buff[4])), WIDTH // 2+325, HEIGHT // 2-20)
        # play button
        s = pygame.Surface((400, 110))
        s.set_alpha(120)
        s.fill((60, 60, 60))
        self.screen.blit(s, (512-420, 820, 400, 110))
        pygame.draw.rect(self.screen, (0, 0, 0), (512-420, 820, 400, 110), 5)
        self.draw_text(self.screen, "PLAY", self.sub_font,
                       'black', 512-220, 875)
        # reset button
        l = pygame.Surface((400, 110))
        l.set_alpha(120)
        l.fill((60, 60, 60))
        self.screen.blit(l, (512+20, 820, 400, 110))
        pygame.draw.rect(self.screen, (0, 0, 0), (512+20, 820, 400, 110), 5)
        self.draw_text(self.screen, "RESET", self.sub_font,
                       'black', 512+220, 875)


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
            newx = self.rect.x + self.moveSpeed
            if newx <= 1024-TILE_SIZE//4*3:
                self.rect.x = newx
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            newy = self.rect.y + self.moveSpeed
            if newy <= 1024-TILE_SIZE//4*3:
                self.rect.y = newy
            self.direct = 2

        if keys[self.keyFIRE] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery,
                   dx, dy, self.bulletDamage)
            if self.bulletDamage > 1:
                self.bulletDamage = 1
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0:
            self.shotTimer -= 1

        for object in objects:
            if object != self and object.type != 'explosion':
                if self.rect.colliderect(object) or self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 64 or self.rect.y > HEIGHT:
                    self.rect.topleft = oldx, oldy

    def draw(self):
        #
        if self.bulletDamage > 1:
            surf = pygame.Surface((self.image.get_size())).convert_alpha()
            surf.fill((150, 75, 50, 125))
            self.image.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def damage(self, value):
        self.HP -= value
        if self.HP <= 0:
            objects.remove(self)
            soundDead.play()


class UI:
    def __init__(self):
        self.main_font = pygame.font.Font(
            "fonts/ZilapSleepGrunge-zLnX.ttf", 40)

    def update(self):
        pass

    def draw(self):
        # i = 0
        border = pygame.Rect(0, 0, 1024, 64)
        big_border = pygame.Rect(0, 0, 1024, 1024)
        pygame.draw.rect(screen, 'gray', big_border, 2)
        pygame.draw.line(screen, 'white', (512, 0), (512, 60), 2)
        pygame.draw.rect(screen, 'white', border, 2)
        for object in objects:
            if object.type == 'tank':
                if object.color == 'Blue':
                    label = self.main_font.render('PLAYER 1', 1, 'white')
                    rect1 = label.get_rect(center=(80, 30))

                    pygame.draw.rect(screen, (220, 20, 20),
                                     (200, 15, 55*min(object.HP, 5), 30))
                    for d in range(5):
                        pygame.draw.rect(
                            screen, 'black', (200 + 55*d, 15, 55, 30), 2)
                    #     pygame.draw.rect(screen, "black", (200 + 50*i, 15, 50, 30))
                    if object.HP > 5:
                        for i in range(min(object.HP-5, 5)):
                            pygame.draw.rect(screen, 'yellow',
                                             (200 + 55*i, 15, 55, 30), 4)

                elif object.color == 'Red':
                    label = self.main_font.render('PLAYER 2', 1, 'white')
                    rect1 = label.get_rect(center=(940, 30))
                    pygame.draw.rect(screen, (220, 20, 20),
                                     (550, 15, 55*min(object.HP, 5), 30))
                    for d in range(5):
                        pygame.draw.rect(
                            screen, 'black', (550 + 55*d, 15, 55, 30), 2)
                    if object.HP > 5:
                        for i in range(min(object.HP-5, 5)):
                            pygame.draw.rect(screen, 'yellow',
                                             (550 + 55*i, 15, 55, 30), 4)

                screen.blit(label, rect1)
                # pygame.draw.rect(screen, object.color, (5 + i * 70, 5, 22, 22))

                # text = fontUI.render(str(object.bulletDamage), 1, 'black')
                # rect = text.get_rect(center=(100, 50))
                # screen.blit(text, rect)

                # text = fontUI.render(str(object.HP), 1, object.color)
                # rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                # screen.blit(text, rect)
                # i += 1


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
        tipe = randint(0, 20)
        self.t = 0
        if tipe == 20:
            self.t = 4
            self.HP = 15
        elif tipe > 18:
            self.t = 3
            self.HP = 8
        elif tipe > 13:
            self.t = 2
            self.HP = 2
        else:
            self.t = 1
            self.HP = 1

        objects.append(self)
        self.type = "obstacle"

        self.rect = pygame.Rect(px, py, size, size)

    def update(self, keys):
        pass

    def draw(self):
        # screen.blit(imgObstacle, self.rect)
        match self.t:
            case 4:
                screen.blit(imgIce, self.rect)
            case 3:
                screen.blit(imgArmor, self.rect)
            case 2:
                screen.blit(imgObstacle, self.rect)
            case 1:
                screen.blit(imgBrick, self.rect)

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
            try:
                bonuses.remove(self)
            except Exception as e:
                print("GAME OVER")

    def draw(self):
        if self.frame <= 24:
            screen.blit(self.image, self.rect)
        elif 3 >= int(self.frame) % 6 >= 0:
            screen.blit(self.image, self.rect)
