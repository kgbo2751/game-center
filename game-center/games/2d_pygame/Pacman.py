import pygame
import random

# 초기화
pygame.init()
WIDTH, HEIGHT = 560, 400
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 100, 100)
GREEN = (0, 255, 0)

# 맵: 0 - 길, 1 - 벽, 2 - 동전
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,0,2,2,2,0,2,2,2,2,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,0,1],
    [1,2,2,0,2,2,2,2,2,2,2,0,2,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,0,1],
    [1,2,2,2,0,2,2,2,0,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# 플레이어, 적 위치
player_pos = [1, 1]
ghosts = [[5, 5], [1, 11], [4, 7]]

# 점수
score = 0
total_coins = sum(row.count(2) for row in MAP)

def draw_map():
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 1:
                pygame.draw.rect(screen, BLUE, rect)
            elif tile == 2:
                pygame.draw.circle(screen, YELLOW, rect.center, 5)

def draw_entities():
    # 플레이어
    pygame.draw.circle(screen, GREEN, (player_pos[1]*TILE_SIZE+TILE_SIZE//2, player_pos[0]*TILE_SIZE+TILE_SIZE//2), 12)
    # 적
    for g in ghosts:
        pygame.draw.circle(screen, RED, (g[1]*TILE_SIZE+TILE_SIZE//2, g[0]*TILE_SIZE+TILE_SIZE//2), 12)

def move_entity(pos, direction):
    dx, dy = direction
    nx, ny = pos[0] + dy, pos[1] + dx
    if 0 <= nx < ROWS and 0 <= ny < COLS and MAP[nx][ny] != 1:
        return [nx, ny]
    return pos

def move_ghosts():
    for i, g in enumerate(ghosts):
        dirs = [(0,1), (1,0), (0,-1), (-1,0)]
        random.shuffle(dirs)
        for d in dirs:
            new_pos = move_entity(g, d)
            if new_pos != g:
                ghosts[i] = new_pos
                break

def check_game_state():
    if player_pos in ghosts:
        return "lose"
    if score >= total_coins:
        return "win"
    return "playing"

# 메인 루프
running = True
game_state = "playing"

while running:
    clock.tick(5)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if game_state == "playing":
        if keys[pygame.K_LEFT]:
            player_pos = move_entity(player_pos, (-1, 0))
        elif keys[pygame.K_RIGHT]:
            player_pos = move_entity(player_pos, (1, 0))
        elif keys[pygame.K_UP]:
            player_pos = move_entity(player_pos, (0, -1))
        elif keys[pygame.K_DOWN]:
            player_pos = move_entity(player_pos, (0, 1))

        # 동전 먹기
        if MAP[player_pos[0]][player_pos[1]] == 2:
            MAP[player_pos[0]][player_pos[1]] = 0
            score += 1

        move_ghosts()
        game_state = check_game_state()

    draw_map()
    draw_entities()
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    if game_state == "win":
        msg = font.render("YOU WIN!", True, YELLOW)
        screen.blit(msg, (WIDTH // 2 - 80, HEIGHT // 2))
    elif game_state == "lose":
        msg = font.render("GAME OVER", True, RED)
        screen.blit(msg, (WIDTH // 2 - 100, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()