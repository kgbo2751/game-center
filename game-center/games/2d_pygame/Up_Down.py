import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Up Down Game")

# 한글 폰트 설정 (같은 폴더에 있어야 함)
try:
    font = pygame.font.Font("NotoSansKR-Regular.ttf", 40)
except:
    print("Font not found")
    pygame.quit()
    sys.exit()

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 게임 변수
target = random.randint(1, 100)
attempts = 0
input_number = ""
message = "Enter a number between 1 and 100"

# 텍스트 출력 함수
def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# 게임 루프
running = True
while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_number.isdigit():
                    guess = int(input_number)
                    attempts += 1
                    if guess < target:
                        message = "Up!"
                    elif guess > target:
                        message = "Down!"
                    else:
                        message = f"Correct! Success in {attempts} tries!"
                input_number = ""

            elif event.key == pygame.K_BACKSPACE:
                input_number = input_number[:-1]

            elif event.unicode.isdigit():
                if len(input_number) < 3:
                    input_number += event.unicode

    # 텍스트 출력
    draw_text(f"Input: {input_number}", 50, 100)
    draw_text(message, 50, 160)
    draw_text(f"Attempts: {attempts}", 50, 220)

    pygame.display.flip()

pygame.quit()
sys.exit()