import pygame
import random
import math

# 초기화
pygame.init()

# 화면 크기
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (50, 100, 255)
BLACK = (0, 0, 0)

# 플레이어 정Paper
player_radius = 20
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5

# 총알 정Paper
bullet_radius = 5
bullet_speed = 10
bullets = []

# 적 정Paper
enemy_radius = 20
enemy_speed = 2
enemies = []

# 점수 및 게임 상태
score = 0
game_over = False

# 플레이어 이동 함수
def move_player(keys):
    if keys[pygame.K_LEFT] and player_pos[0] - player_radius > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] + player_radius < WIDTH:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] - player_radius > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] + player_radius < HEIGHT:
        player_pos[1] += player_speed

# 총알 발사 함수
def shoot_bullet():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - player_pos[0]
    dy = mouse_y - player_pos[1]
    distance = math.hypot(dx, dy)
    direction = (dx / distance, dy / distance)
    bullet = {'pos': [player_pos[0], player_pos[1]], 'dir': direction}
    bullets.append(bullet)

# 적 생성 함수
def create_enemy():
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    return {'pos': [x, y]}

# 적과 총알 충돌 확인 함수
def check_collisions():
    global score, game_over
    for bullet in bullets:
        for enemy in enemies:
            dx = bullet['pos'][0] - enemy['pos'][0]
            dy = bullet['pos'][1] - enemy['pos'][1]
            if math.hypot(dx, dy) < enemy_radius + bullet_radius:
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break

    for enemy in enemies:
        dx = enemy['pos'][0] - player_pos[0]
        dy = enemy['pos'][1] - player_pos[1]
        if math.hypot(dx, dy) < player_radius + enemy_radius:
            game_over = True

# 적이 플레이어를 따라오는 함수
def move_enemies():
    for enemy in enemies:
        dx = player_pos[0] - enemy['pos'][0]
        dy = player_pos[1] - enemy['pos'][1]
        distance = math.hypot(dx, dy)
        if distance != 0:
            direction = (dx / distance, dy / distance)
            enemy['pos'][0] += direction[0] * enemy_speed
            enemy['pos'][1] += direction[1] * enemy_speed

# 게임 루프
while not game_over:
    screen.fill(WHITE)
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot_bullet()

    # 키 입력
    keys = pygame.key.get_pressed()
    move_player(keys)

    # 총알 이동
    for bullet in bullets:
        bullet['pos'][0] += bullet['dir'][0] * bullet_speed
        bullet['pos'][1] += bullet['dir'][1] * bullet_speed

    # 적 이동 (플레이어를 추적)
    move_enemies()

    # 적 추가 (주기적으로)
    if random.random() < 0.02:
        enemies.append(create_enemy())

    # 충돌 확인
    check_collisions()

    # 플레이어 그리기
    pygame.draw.circle(screen, BLUE, player_pos, player_radius)

    # 총알 그리기
    for bullet in bullets:
        pygame.draw.circle(screen, BLACK, (int(bullet['pos'][0]), int(bullet['pos'][1])), bullet_radius)

    # 적 그리기
    for enemy in enemies:
        pygame.draw.circle(screen, RED, (int(enemy['pos'][0]), int(enemy['pos'][1])), enemy_radius)

    # 점수 표시
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # 게임 오버 화면 표시
    if game_over:
        game_over_text = font.render("GAME OVER", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()