import pygame
import random
import time

# 초기화
pygame.init()

# 화면 크기
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("5-Lane Horse Racing")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HORSE_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]  # 빨강, 초록, 파랑, 노랑, 주황

# 폰트
font = pygame.font.SysFont("Arial", 30)

# 레이스 설정
lane_width = 120  # 각 레인의 너비
num_horses = 5  # 말의 개수
horse_positions = [pygame.Rect(100 + i * lane_width, 100 + j * 80, 100, 50) for j, i in enumerate(range(num_horses))]  # 5개의 레인에 말 배치
race_length = 600  # 경주 거리
speed = [random.randint(1, 3) for _ in range(num_horses)]  # 각 말의 속도를 천천히 설정
race_time = 5  # 10초 동안 경주
start_time = None
race_started = False
winner = None

# 메인 루프
running = True

# 말 선택 화면
def show_selection_screen():
    screen.fill(WHITE)
    title_text = font.render("Select your horse", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
    
    for i in range(num_horses):
        horse_rect = pygame.Rect(100 + i * lane_width, 200, 100, 50)
        pygame.draw.rect(screen, HORSE_COLORS[i], horse_rect)  # 각 말에 색을 적용
        pygame.draw.rect(screen, BLACK, horse_rect, 2)  # 테두리

        # 선택된 말에 빨간 테두리
        if horse_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 0, 0), horse_rect, 5)  # 선택된 말에 빨간 테두리

    pygame.display.flip()

def start_race():
    global race_started, start_time
    race_started = True
    start_time = time.time()  # 경주 시작 시간 기록

def update_race():
    global winner
    screen.fill(WHITE)

    # 경주 트랙 그리기 (5레인)
    for i in range(num_horses):
        pygame.draw.line(screen, BLACK, (100, 100 + i * 80), (WIDTH - 100, 100 + i * 80), 5)  # 각 레인의 트랙

    # 결승선 그리기
    pygame.draw.line(screen, BLACK, (WIDTH - 100, 50), (WIDTH - 100, HEIGHT - 50), 5)  # 결승선

    # 말 이동
    for i in range(num_horses):
        horse_positions[i].x += speed[i]  # 각 말의 속도로 이동
        pygame.draw.rect(screen, HORSE_COLORS[i], horse_positions[i])  # 말 색상

    # 경주 시간이 끝났는지 확인
    if time.time() - start_time >= race_time:
        if winner is None:
            # 10초 후 랜덤으로 우승자 결정
            winner = random.randint(0, num_horses - 1)

    # 우승한 말 표시
    if winner is not None:
        win_text = font.render(f"Winner: Horse {winner + 1}", True, BLACK)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

# 게임 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not race_started:  # 말 선택 화면에서 클릭
                for i in range(num_horses):
                    horse_rect = pygame.Rect(100 + i * lane_width, 200, 100, 50)
                    if horse_rect.collidepoint(pygame.mouse.get_pos()):
                        start_race()

    if not race_started:
        show_selection_screen()  # 말 선택 화면
    else:
        update_race()  # 경주 진행

    pygame.display.flip()

pygame.quit()