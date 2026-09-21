import pygame
import random
import time

# 초기화
pygame.init()

# 화면 크기
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Game")
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# 게임 설정
font = pygame.font.SysFont("Arial", 30)
score = 0

# 리듬 버튼 설정 (방향키)
buttons = {
    pygame.K_UP: (100, HEIGHT - 100),      # 위
    pygame.K_LEFT: (200, HEIGHT - 100),    # 왼쪽
    pygame.K_DOWN: (300, HEIGHT - 100),    # 아래
    pygame.K_RIGHT: (400, HEIGHT - 100)    # 오른쪽
}

button_radius = 40
button_colors = {
    pygame.K_UP: BLUE,
    pygame.K_LEFT: GREEN,
    pygame.K_DOWN: RED,
    pygame.K_RIGHT: YELLOW
}

# 리듬 이벤트 설정
note_speed = 4
notes = []

# 점수 표시 함수
def display_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# 리듬 노트 생성 함수
def generate_notes():
    key = random.choice([pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT])
    x, y = buttons[key]
    notes.append({'key': key, 'pos': [x, 0]})

# 노트 이동 함수
def move_notes():
    global score
    for note in notes:
        note['pos'][1] += note_speed
        if note['pos'][1] > HEIGHT:  # 화면 밖으로 나가면 제거
            notes.remove(note)
            score -= 5  # 화면 밖으로 나간 노트에 대해 점수 감소

# 노트 충돌 처리
def check_notes():
    global score
    for note in notes:
        note_x, note_y = note['pos']
        if note_y > 550 and note_y < 600:  # 타이밍이 맞는 구간
            if pygame.key.get_pressed()[note['key']]:  # 맞는 키가 눌렸을 때
                score += 10
                notes.remove(note)
            elif not pygame.key.get_pressed()[note['key']]:  # 키가 눌리지 않으면
                score -= 5
                notes.remove(note)

# 버튼 효과 (누를 때 색상 변경)
def button_effect(key):
    if pygame.key.get_pressed()[key]:
        return (255, 255, 255)  # 흰색 효과
    else:
        return button_colors[key]  # 기본 색

# 키 이름 표시 함수
def draw_key_names():
    key_names = {
        pygame.K_UP: "Up",
        pygame.K_LEFT: "Left",
        pygame.K_DOWN: "Down",
        pygame.K_RIGHT: "Right"
    }
    for key, (x, y) in buttons.items():
        text = font.render(key_names[key], True, BLACK)
        screen.blit(text, (x - text.get_width() // 2, y + button_radius + 10))

# 게임 루프
while True:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # 리듬 노트 생성 주기
    if random.random() < 0.02:
        generate_notes()

    # 리듬 노트 이동
    move_notes()

    # 리듬 노트 충돌 확인
    check_notes()

    # 리듬 노트 그리기
    for note in notes:
        key = note['key']
        x, y = note['pos']
        pygame.draw.circle(screen, button_colors[key], (x, y), button_radius)

    # 버튼(키) 위치 표시 및 효과
    for key, (x, y) in buttons.items():
        button_color = button_effect(key)
        pygame.draw.circle(screen, button_color, (x, y), button_radius, 2)

    # 키 이름 표시
    draw_key_names()

    # 점수 표시
    display_score()

    pygame.display.flip()
    clock.tick(60)