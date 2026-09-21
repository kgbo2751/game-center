import pygame
import random

# 초기화
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# 색상
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
GREEN = (0, 200, 0)

# 플레이어 설정
player = pygame.Rect(100, 300, 30, 30)
gravity = 0.5
jump_strength = -10
velocity = 0

# 파이프 설정
pipe_width = 60
pipe_gap = 150
pipe_speed = 3
pipes = []
score = 0

def create_pipe():
    top_height = random.randint(100, 400)
    bottom_y = top_height + pipe_gap
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, top_height)
    bottom_pipe = pygame.Rect(WIDTH, bottom_y, pipe_width, HEIGHT - bottom_y)
    return top_pipe, bottom_pipe

# 첫 파이프
pipes.extend(create_pipe())

running = True
while running:
    screen.fill(WHITE)

    # 이벤트
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        velocity = jump_strength

    # 중력 적용
    velocity += gravity
    player.y += velocity

    # 파이프 이동 및 충돌
    for pipe in pipes:
        pipe.x -= pipe_speed
    if pipes[0].x + pipe_width < 0:
        pipes = pipes[2:]  # 앞 파이프 제거
        pipes.extend(create_pipe())
        score += 1

    # 충돌 체크
    for pipe in pipes:
        if player.colliderect(pipe):
            running = False
    if player.top < 0 or player.bottom > HEIGHT:
        running = False

    # 그리기
    pygame.draw.rect(screen, BLUE, player)
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

    # 점수 표시
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # 업데이트
    pygame.display.flip()
    clock.tick(60)

pygame.quit()