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
        Tank(700, 700, 1, "Red", (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,
                                  pygame.K_DOWN, pygame.K_m))

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
            # clock.tick(24)
            bullets.clear()
            pygame.draw.rect(screen, 'black', (0, HEIGHT // 2-100, 1024, 200))
            if tankWin.color == 'Blue':
                text = fontMegaBig.render('PLAYER 1 WINS', 1, 'white')
            else:
                text = fontMegaBig.render('PLAYER 2 WINS', 1, 'white')
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, rect)
            for i in range(32):
                e = Explosion(1024//32*i, HEIGHT // 2-120)
                e = Explosion(1024//32*i, HEIGHT // 2+120)
                e = Explosion(1024//32*i, HEIGHT // 2-220)
                e = Explosion(1024//32*i, HEIGHT // 2+220)
            

            # pygame.draw.rect(screen, tankWin.color,
            #                  (WIDTH // 2 - 100, HEIGHT // 2, 200, 200))
    def click(pos):
        pass
    def restart():
        bullets.clear()
        bonuses.clear()
        main_class.spawn_tanks()
        main_class.spawn_obstacles()
        main_class.spawn_bonuses()
        
