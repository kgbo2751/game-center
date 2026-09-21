import pygame
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bulls and Cows")

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# 폰트 설정
font = pygame.font.SysFont("Arial", 30)

# 게임 변수 설정
target_number = str(random.randint(1000, 9999))  # 컴퓨터가 랜덤으로 생성한 4자리 숫자
attempts = 0
max_attempts = 10  # 최대 시도 횟수

# 결과 메시지 설정
input_box = pygame.Rect(200, 100, 200, 40)
input_text = ""
game_over = False
result_message = ""

# 게임 루프
running = True
while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                continue  # 게임 오버 후 입력 불가
            if event.key == pygame.K_RETURN:  # Enter 키로 숫자 제출
                if len(input_text) == 4 and input_text.isdigit():  # 입력이 4자리 숫자인지 확인
                    attempts += 1
                    strikes = sum([input_text[i] == target_number[i] for i in range(4)])
                    balls = sum([input_text[i] in target_number and input_text[i] != target_number[i] for i in range(4)])
                    outs = 4 - strikes - balls

                    if strikes == 4:  # 사용자가 숫자를 맞췄을 경우
                        result_message = f"Correct answer! Attempt: {attempts}"
                        game_over = True
                    else:
                        result_message = f"{strikes} Strike, {balls} Ball, {outs} Out"
                    
                    input_text = ""  # 입력란 초기화
                else:
                    result_message = "Enter 4 digits!"
            elif event.key == pygame.K_BACKSPACE:  # 백스페이스 처리
                input_text = input_text[:-1]
            else:
                if len(input_text) < 4:  # 4자리 숫자만 입력 가능
                    input_text += event.unicode

    # 입력란 그리기
    pygame.draw.rect(screen, BLACK, input_box, 2)
    input_surface = font.render(input_text, True, BLACK)
    screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

    # 결과 메시지 출력
    result_surface = font.render(result_message, True, BLACK)
    screen.blit(result_surface, (150, 200))

    # 최대 시도 횟수까지 게임 진행
    if attempts >= max_attempts and not game_over:
        result_message = f"Max attempts exceeded! Answer was {target_number}."
        game_over = True

    # 화면 업데이트
    pygame.display.flip()

pygame.quit()