import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Penalty Kick Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 폰트 설정
font = pygame.font.SysFont("Arial", 30)

# 플레이어 and 골키퍼 설정
player_x = 100
player_y = HEIGHT // 2
player_width = 50
player_height = 20
player_speed = 10

ball_radius = 10
ball_x = player_x + player_width
ball_y = player_y + player_height // 2

goalkeeper_width = 50
goalkeeper_height = 100
goalkeeper_x = WIDTH - goalkeeper_width - 50
goalkeeper_y = random.randint(100, HEIGHT - 200)

# 게임 변수
score = 0
lives = 3
game_over = False

# 공의 방향 (상, 하, 좌, 우)
ball_dx = 0
ball_dy = 0

# 게임 루프
running = True
while running:
    screen.fill(GREEN)

    if not game_over:
        # 게임 오버가 아니면 페널티킥 진행
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 키Paper드 입력 처리
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball_dy = -5  # 공을 위로 찬다
                elif event.key == pygame.K_DOWN:
                    ball_dy = 5  # 공을 아래로 찬다
                elif event.key == pygame.K_LEFT:
                    ball_dx = -5  # 공을 왼쪽으로 찬다
                elif event.key == pygame.K_RIGHT:
                    ball_dx = 5  # 공을 오른쪽으로 찬다

        # 공의 이동
        ball_x += ball_dx
        ball_y += ball_dy

        # 공이 골대 안으로 들어가면 점수 증가
        if ball_x > WIDTH - 50 and goalkeeper_y < ball_y < goalkeeper_y + goalkeeper_height:
            if goalkeeper_x < ball_x < goalkeeper_x + goalkeeper_width:
                score -= 1  # 골키퍼가 막으면 점수 차감
                lives -= 1  # 골키퍼가 막을 경우 라이프 감소
                ball_dx = 0
                ball_dy = 0
                ball_x = player_x + player_width  # 공 초기화
                ball_y = player_y + player_height // 2

        # 공이 화면 밖으로 나가면 점수 증가
        if ball_x >= WIDTH:
            if goalkeeper_y < ball_y < goalkeeper_y + goalkeeper_height:
                score += 1  # 공이 골문을 통과하면 점수 추가
            ball_dx = 0
            ball_dy = 0
            ball_x = player_x + player_width  # 공 초기화
            ball_y = player_y + player_height // 2

        # 골키퍼 랜덤 움직임
        if random.random() < 0.02:  # 일정 확률로 골키퍼가 움직임
            goalkeeper_y = random.randint(100, HEIGHT - 200)

        # 공 그리기
        pygame.draw.circle(screen, YELLOW, (ball_x, ball_y), ball_radius)

        # 골키퍼 그리기
        pygame.draw.rect(screen, RED, (goalkeeper_x, goalkeeper_y, goalkeeper_width, goalkeeper_height))

        # 점수 출력
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # 라이프 출력
        lives_text = font.render(f"Lives: {lives}", True, BLACK)
        screen.blit(lives_text, (WIDTH - 150, 10))

        # 게임 오버 처리
        if lives <= 0:
            game_over_text = font.render("Game Over!", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
            game_over = True

    # 화면 업데이트
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()