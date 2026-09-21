import pygame
import random

# 초기화
pygame.init()

# 화면 크기
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scissors Rock Paper")

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 폰트 설정 (한글을 지원하는 폰트 파일을 사용)
font = pygame.font.Font(None, 30)  # None으로 기본 폰트 사용
large_font = pygame.font.Font(None, 50)

# 버튼 설정
button_width, button_height = 200, 50
button_gap = 20

# Scissors Rock Paper 선택
choices = ['Scissors', 'Rock', 'Paper']

# 결과 처리 함수
def get_result(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "Tie"
    elif (user_choice == 'Scissors' and computer_choice == 'Paper') or \
         (user_choice == 'Rock' and computer_choice == 'Scissors') or \
         (user_choice == 'Paper' and computer_choice == 'Rock'):
        return "Win"
    else:
        return "Lose"

# 게임 루프
running = True
user_choice = None
computer_choice = random.choice(choices)
result = ""

while running:
    screen.fill(WHITE)
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if 50 <= mx <= 50 + button_width and 250 <= my <= 250 + button_height:
                user_choice = 'Scissors'
            elif 250 <= mx <= 250 + button_width and 250 <= my <= 250 + button_height:
                user_choice = 'Rock'
            elif 450 <= mx <= 450 + button_width and 250 <= my <= 250 + button_height:
                user_choice = 'Paper'

            if user_choice:
                computer_choice = random.choice(choices)
                result = get_result(user_choice, computer_choice)
    
    # 사용자 선택 버튼
    pygame.draw.rect(screen, BLUE, (50, 250, button_width, button_height))
    pygame.draw.rect(screen, BLUE, (250, 250, button_width, button_height))
    pygame.draw.rect(screen, BLUE, (450, 250, button_width, button_height))
    
    # 텍스트 표시
    screen.blit(font.render("Scissors", True, WHITE), (100, 260))
    screen.blit(font.render("Rock", True, WHITE), (300, 260))
    screen.blit(font.render("Paper", True, WHITE), (500, 260))
    
    # 결과 출력
    if user_choice:
        screen.blit(large_font.render(f"My Choice: {user_choice}", True, BLACK), (WIDTH // 2 - 150, 100))
        screen.blit(large_font.render(f"Computer Choice: {computer_choice}", True, BLACK), (WIDTH // 2 - 200, 150))
        screen.blit(large_font.render(f"Result: {result}", True, GREEN if result == "Win" else RED), (WIDTH // 2 - 150, 200))
    
    pygame.display.flip()

pygame.quit()