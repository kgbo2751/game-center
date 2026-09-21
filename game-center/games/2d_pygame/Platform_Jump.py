import pygame
import random

# 초기화
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platform Jump")

# 색
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
GREEN = (0, 200, 0)

# 시계
clock = pygame.time.Clock()

# 폰트
font = pygame.font.SysFont("Arial", 30)

# 플레이어
player_y_vel = 0
gravity = 0.5
jump_strength = -15
on_ground = False

# 발판
first_platform = pygame.Rect(0, 550, 200, 20)
platforms = [first_platform]
player = pygame.Rect(first_platform.x + 50, first_platform.y - 40, 40, 40)  # 발판 위에 위치
platform_speed = 3

# 점수
score = 0

# 새 변수 추가
jump_pressed = False

# 이벤트 처리
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and on_ground:
            player_y_vel = jump_strength
            jump_pressed = True
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            jump_pressed = False
            # 점프 중에 스페이스 뗐으면 상승 줄이기
            if player_y_vel < -3:
                player_y_vel = -3

# 메인 루프
running = True
while running:
    screen.fill(WHITE)

    # 이벤트
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and on_ground:
        player_y_vel = jump_strength

    # 중력 적용
    player_y_vel += gravity
    player.y += player_y_vel

    # 발판 이동 (왼쪽으로 스크롤)
    for plat in platforms:
        plat.x -= platform_speed

    # 화면 밖 발판 제거 및 점수 증가
    platforms = [p for p in platforms if p.x + p.width > 0]
    while len(platforms) < 5:
        last_platform = platforms[-1]
        new_width = random.randint(100, 150)
        new_x = last_platform.x + random.randint(200, 300)
        new_y = random.randint(300, 550)
        platforms.append(pygame.Rect(new_x, new_y, new_width, 20))
        score += 1

    # 충돌 감지
    on_ground = False  # 여기서 초기화
    for plat in platforms:
        if player.colliderect(plat) and player_y_vel >= 0 and player.bottom <= plat.top + 10:
            player.bottom = plat.top
            player_y_vel = 0
            on_ground = True

    # 게임 오버
    if player.top > screen_height:
        running = False

    # 캐릭터 and 발판 그리기
    pygame.draw.rect(screen, BLUE, player)
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)

    # 점수 출력
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # 업데이트
    pygame.display.flip()
    clock.tick(60)

pygame.quit()