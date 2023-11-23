import pygame


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((900, 600))
x = 100
y = 100
pygame.draw.rect(screen, (255, 0, 0), (100, 100, 100, 100))

matrix_field = [[0 for i in range(9)] for j in range(6)]
matrix_field[4][4] = 1
matrix_field[4][5] = 1
matrix_field[2][2] = 1
matrix_field[2][8] = 1
matrix_field[3][8] = 1
matrix_field[1][5] = 1
obstacles = []

for i in range(9):
    for j in range(6):
        if matrix_field[j][i] == 1:
            obstacles.append((i * 100, j * 100, 100, 100))

print(obstacles)
right_left = 0
up_down = 0


while True:
    for event in pygame.event.get():
        if pygame.QUIT == event.type:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN and right_left == 0 and up_down == 0:
            if event.key == pygame.K_d and x < 900 - 100 and (x + 100, y) not in [(i[0], i[1]) for i in obstacles]:
                right_left = 10
            elif event.key == pygame.K_a and x > 0 and (x - 100, y) not in [(i[0], i[1]) for i in obstacles]:
                right_left = -10
            elif event.key == pygame.K_w and y > 0 and (x, y - 100) not in [(i[0], i[1]) for i in obstacles]:
                up_down = -10
            elif event.key == pygame.K_s and y < 600 - 100 and (x, y + 100) not in [(i[0], i[1]) for i in obstacles]:
                up_down = 10

    if up_down > 0:
        y += 10
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (x, y, 100, 100))
        up_down -= 1
    elif up_down < 0:
        y -= 10
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (x, y, 100, 100))
        up_down += 1

    if right_left > 0:
        x += 10
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (x, y, 100, 100))
        right_left -= 1
    elif right_left < 0:
        x -= 10
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (x, y, 100, 100))
        right_left += 1

    for i in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), i)
    pygame.display.update()
    clock.tick(10)
