import pygame
import random
import time

# 초기화
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Mole")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# 색상
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

# 두더지 정Paper
mole_radius = 30
mole_time = 1000  # 두더지가 나타나는 시간 (밀리초)
mole_hide_time = 1000  # 두더지가 사라지는 시간
mole_pos = (random.randint(0, WIDTH - mole_radius * 2), random.randint(0, HEIGHT - mole_radius * 2))

# 게임 변수
score = 0
missed = 0
mole_show_time = random.randint(1000, 3000)
last_mole_time = time.time()
mole_active = False
mole_rect = pygame.Rect(mole_pos[0], mole_pos[1], mole_radius * 2, mole_radius * 2)

# 두더지 생성 함수
def generate_mole():
    return pygame.Rect(random.randint(0, WIDTH - mole_radius * 2), random.randint(0, HEIGHT - mole_radius * 2), mole_radius * 2, mole_radius * 2)

# 게임 루프
running = True
while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and mole_active:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mole_rect.collidepoint(mouse_x, mouse_y):
                score += 1
                mole_active = False

    # 두더지 활성화
    if time.time() - last_mole_time > mole_show_time / 1000:
        mole_active = True
        mole_rect = generate_mole()
        last_mole_time = time.time()

    # 두더지 그리기
    if mole_active:
        pygame.draw.circle(screen, BROWN, mole_rect.center, mole_radius)
    
    # 점수 and 놓친 두더지 표시
    score_text = font.render(f"Score: {score}", True, BLACK)
    missed_text = font.render(f"Missed: {missed}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(missed_text, (10, 40))

    # 게임 오버 조건
    if missed >= 5:
        game_over_text = font.render("Game Over!", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        time.sleep(2)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()