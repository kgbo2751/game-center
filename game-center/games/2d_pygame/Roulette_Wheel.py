import pygame
import random
import math

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roulette Machine")

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 폰트 설정
font = pygame.font.SysFont("Arial", 30)

# 룰렛 바퀴 설정
num_slots = 37  # 0~36
angle_per_slot = 360 / num_slots
radius = 200
center = (WIDTH // 2, HEIGHT // 2)

# 숫자 and 색상 설정
numbers = list(range(num_slots))
colors = ['red', 'black'] * (num_slots // 2) + ['green']
colors[0] = 'green'  # 0번은 녹색

# 사용자 입력 상태
selected_number = None  # 사용자가 선택한 번호
spinning = False  # 바퀴가 회전 중인지 여부
rotation_angle = 0  # 회전 각도
spin_duration = 0  # 회전 지속 시간
game_result = ""  # 게임 결과

# 게임 루프
running = True
while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if selected_number is None:  # 아직 번호를 선택하지 않았으면
                # 클릭한 위치에서 숫자 선택 (0~36)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.degrees(math.atan2(mouse_y - center[1], mouse_x - center[0])) % 360
                selected_number = int(angle // angle_per_slot)  # 선택한 숫자
                game_result = f"Selected Number: {selected_number}"
            elif not spinning:  # 번호를 선택한 후 클릭하면 회전 시작
                spinning = True
                rotation_angle = random.randint(0, 360)  # 회전 각도 랜덤
                spin_duration = 60  # 60프레임 동안 회전

    # 룰렛 바퀴 그리기
    roulette_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    roulette_surface.fill((0, 0, 0, 0))  # 투명 배경

    for i in range(num_slots):
        angle = angle_per_slot * i
        start_x = center[0] + radius * math.cos(math.radians(angle))
        start_y = center[1] + radius * math.sin(math.radians(angle))
        end_x = center[0] + radius * math.cos(math.radians(angle + angle_per_slot))
        end_y = center[1] + radius * math.sin(math.radians(angle + angle_per_slot))

        # 색상 지정
        color = RED if colors[i] == 'red' else BLACK if colors[i] == 'black' else GREEN
        pygame.draw.line(roulette_surface, color, (start_x, start_y), (end_x, end_y), 3)

        # 숫자 배치
        number_text = font.render(str(numbers[i]), True, WHITE)
        text_rect = number_text.get_rect(center=(start_x + (end_x - start_x) / 2, start_y + (end_y - start_y) / 2))
        roulette_surface.blit(number_text, text_rect)

    # 회전 효과 적용
    if spinning:
        rotation_angle += 10  # 회전 속도
        spin_duration -= 1
        if spin_duration <= 0:
            spinning = False
            selected_number_on_wheel = int((rotation_angle % 360) / angle_per_slot)
            result_text = f"Result: {numbers[selected_number_on_wheel]}"
            if selected_number_on_wheel == selected_number:
                result_text += " - Your choice was correct!"
            else:
                result_text += " - Your choice was wrong."
            game_result = result_text

    # 룰렛 바퀴 회전
    rotated_surface = pygame.transform.rotate(roulette_surface, rotation_angle)
    rotated_rect = rotated_surface.get_rect(center=center)
    screen.blit(rotated_surface, rotated_rect.topleft)

    # 결과 출력
    if game_result:
        result_surface = font.render(game_result, True, BLUE)
        screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, HEIGHT - 100))

    # 화면 업데이트
    pygame.display.flip()

pygame.quit()