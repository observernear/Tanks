from settings import *


class main_class:
    
    def draw():
        for object in objects:
            object.draw()
        for bonus in bonuses:
            bonus.draw()
        for bullet in bullets:
            bullet.draw()

    def update(keys):
        for object in objects:
            object.update(keys)
        for bullet in bullets:
            bullet.update()
        for bonus in bonuses:
            bonus.update()

    def spawn_tanks():
        Tank(100, 100, 0, "Blue", (pygame.K_a, pygame.K_d,
                                   pygame.K_w, pygame.K_s, pygame.K_SPACE))
        Tank(700, 100, 1, "Red", (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,
                                  pygame.K_DOWN, pygame.K_x))

    def spawn_bonuses():
        global BONUSCD
        if BONUSCD >= 54:
            BONUSCD = 0
            for _ in range(3):
                bonusNum = randint(0, 1)
                x = randint(0, WIDTH // TILE_SIZE - 1) * TILE_SIZE
                y = randint(1, HEIGHT // TILE_SIZE - 1) * TILE_SIZE
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                Bonus(x, y, bonusNum)
        BONUSCD += 0.1

    def spawn_obstacles():
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

    def check_winner():
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
    def click(pos):
        pass
    def restart():
        main_class.spawn_tanks()
        main_class.spawn_obstacles()
        bullets.clear()
        bonuses.clear()
        