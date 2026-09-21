import pygame
import random

# 초기화
pygame.init()
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# 색상
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# 스네이크 초기 상태
snake = [(5, 5)]
direction = (1, 0)  # 오른쪽 시작
apple = (random.randint(0, WIDTH // CELL_SIZE - 1),
         random.randint(0, HEIGHT // CELL_SIZE - 1))
score = 0

def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_apple():
    pygame.draw.rect(screen, RED, (apple[0]*CELL_SIZE, apple[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

running = True
while running:
    screen.fill(WHITE)

    # 이벤트
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, 1):
        direction = (0, -1)
    elif keys[pygame.K_DOWN] and direction != (0, -1):
        direction = (0, 1)
    elif keys[pygame.K_LEFT] and direction != (1, 0):
        direction = (-1, 0)
    elif keys[pygame.K_RIGHT] and direction != (-1, 0):
        direction = (1, 0)

    # 이동
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)

    # 충돌 처리
    if head == apple:
        score += 1
        apple = (random.randint(0, WIDTH // CELL_SIZE - 1),
                 random.randint(0, HEIGHT // CELL_SIZE - 1))
    else:
        snake.pop()  # 꼬리 제거 (이동 효과)

    # 벽이나 자기 몸에 닿았는지 확인
    if (head[0] < 0 or head[0] >= WIDTH // CELL_SIZE or
        head[1] < 0 or head[1] >= HEIGHT // CELL_SIZE or
        head in snake[1:]):
        running = False

    # 그리기
    draw_snake()
    draw_apple()
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()