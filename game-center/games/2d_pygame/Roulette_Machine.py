import pygame
import random
import time

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3-Slot Roulette Machine")

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 폰트 설정
font = pygame.font.SysFont("None", 50)
button_font = pygame.font.SysFont("None", 30)

# 가능한 심볼들
possible_values = ['★', '7', '♥', '○', 'X']  # 5가지 가능한 심볼

# 룰렛 설정
slot_width = 100
slot_height = 100
num_slots = 3  # 3자리 숫자
gap = 10  # 슬롯 간격
spinning = False  # 룰렛 회전 여부
spin_duration = 0  # 회전 지속 시간
result = ""
start_time = None  # 룰렛 시작 시간
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)  # 버튼 위치

# 게임 루프
running = True
while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and not spinning:
                # 버튼 클릭 시, 룰렛 시작
                spinning = True
                start_time = time.time()  # 현재 시간 저장
                result = ""  # 이전 결과 지우기

    # 슬롯 그리기
    for i in range(num_slots):
        x = WIDTH // 2 - (num_slots * (slot_width + gap) // 2) + i * (slot_width + gap)
        y = HEIGHT // 2 - slot_height // 2

        # 슬롯 배경
        pygame.draw.rect(screen, BLACK, (x, y, slot_width, slot_height))

        # 가능한 심볼 랜덤으로 표시
        value = random.choice(possible_values)
        value_text = font.render(str(value), True, WHITE)
        text_rect = value_text.get_rect(center=(x + slot_width // 2, y + slot_height // 2))
        screen.blit(value_text, text_rect)

    # 룰렛 회전 효과
    if spinning:
        if start_time and time.time() - start_time < 5:  # 5초 동안 회전
            # 회전 속도 설정
            spin_duration += 10  # 회전 속도
        else:
            spinning = False  # 5초 후 멈추기
            result = f"Result: {random.choice(possible_values)}"  # 랜덤으로 결과 결정

    # 5초 제한 후 멈춤
    if not spinning and result:
        result_surface = font.render(result, True, BLUE)
        screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, HEIGHT - 100))

    # 'Spin' 버튼 그리기
    pygame.draw.rect(screen, GREEN, button_rect)  # 버튼 색상
    button_text = button_font.render("Spin", True, WHITE)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)  # 버튼 텍스트

    # 화면 업데이트
    pygame.display.flip()

pygame.quit()