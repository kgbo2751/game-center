import pygame
import random

# 초기화
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Laser")

# 색상
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 플레이어 설정
player_size = 50
player = pygame.Rect(WIDTH//2, HEIGHT//2, player_size, player_size)
player_speed = 5

# 레이저 설정
laser_speed = 7
lasers = []
laser_timer = 0
laser_interval = 1000  # ms

# 점수
score = 0
font = pygame.font.SysFont(None, 40)

# 방향 정의
DIRECTIONS = ['left', 'right', 'top', 'bottom']

def spawn_laser():
    direction = random.choice(DIRECTIONS)
    if direction == 'left':
        rect = pygame.Rect(0, random.randint(0, HEIGHT-10), WIDTH, 10)
        velocity = (laser_speed, 0)
    elif direction == 'right':
        rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT-10), WIDTH, 10)
        velocity = (-laser_speed, 0)
    elif direction == 'top':
        rect = pygame.Rect(random.randint(0, WIDTH-10), 0, 10, HEIGHT)
        velocity = (0, laser_speed)
    else:  # bottom
        rect = pygame.Rect(random.randint(0, WIDTH-10), HEIGHT, 10, HEIGHT)
        velocity = (0, -laser_speed)
    return {'rect': rect, 'vel': velocity}

# 게임 루프
clock = pygame.time.Clock()
running = True
last_time = pygame.time.get_ticks()

while running:
    dt = clock.tick(60)
    win.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.x -= player_speed
    if keys[pygame.K_RIGHT]: player.x += player_speed
    if keys[pygame.K_UP]: player.y -= player_speed
    if keys[pygame.K_DOWN]: player.y += player_speed

    # 레이저 생성
    now = pygame.time.get_ticks()
    if now - last_time > laser_interval:
        lasers.append(spawn_laser())
        last_time = now
        score += 1

    # 레이저 이동 및 충돌
    for laser in lasers:
        laser['rect'].x += laser['vel'][0]
        laser['rect'].y += laser['vel'][1]
        if laser['rect'].colliderect(player):
            running = False

    # 그리기
    pygame.draw.rect(win, BLUE, player)
    for laser in lasers:
        pygame.draw.rect(win, RED, laser['rect'])

    # 점수 출력
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    win.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()