import pygame
import random

# 초기화
pygame.init()

# 화면 크기
WIDTH, HEIGHT = 300, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TicTacToe vs Computer")

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (28, 170, 156)
X_COLOR = (242, 85, 96)
O_COLOR = (28, 170, 156)

# 폰트 설정
font = pygame.font.Font(None, 30)

# 게임 Paper드 설정
board = [' ' for _ in range(9)]  # 3x3 Paper드 (빈칸으로 초기화)
player = 'X'  # 사용자
computer = 'O'  # 컴퓨터

# 게임 Paper드 그리기 함수
def draw_board():
    screen.fill(WHITE)
    # 그리드 그리기
    for row in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT / 3 * row), (WIDTH, HEIGHT / 3 * row), 5)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 * row, 0), (WIDTH / 3 * row, HEIGHT), 5)
    
    # 'X' and 'O' 그리기
    for i in range(9):
        row, col = divmod(i, 3)
        if board[i] == 'X':
            pygame.draw.line(screen, X_COLOR, (col * WIDTH / 3 + 10, row * HEIGHT / 3 + 10),
                             (col * WIDTH / 3 + WIDTH / 3 - 10, row * HEIGHT / 3 + HEIGHT / 3 - 10), 10)
            pygame.draw.line(screen, X_COLOR, (col * WIDTH / 3 + 10, row * HEIGHT / 3 + HEIGHT / 3 - 10),
                             (col * WIDTH / 3 + WIDTH / 3 - 10, row * HEIGHT / 3 + 10), 10)
        elif board[i] == 'O':
            pygame.draw.circle(screen, O_COLOR, (int(col * WIDTH / 3 + WIDTH / 6), int(row * HEIGHT / 3 + HEIGHT / 6)),
                               WIDTH // 6, 10)
    
    pygame.display.update()

# 승패 검사 함수
def check_winner():
    # 승리 조건
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # 가로
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 세로
                      (0, 4, 8), (2, 4, 6)]  # 대각선
    
    for condition in win_conditions:
        a, b, c = condition
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    
    if ' ' not in board:
        return 'D'  # Tie
    
    return None  # 게임이 끝나지 않음

# 컴퓨터 AI (랜덤으로 빈 칸에 'O'를 놓음)
def computer_move():
    empty_spaces = [i for i, spot in enumerate(board) if spot == ' ']
    move = random.choice(empty_spaces)
    board[move] = computer

# 게임 루프
running = True
game_over = False
while running:
    draw_board()
    
    # 게임 종료 후 메시지
    if game_over:
        winner = check_winner()
        if winner == 'X':
            message = "You Win!"
        elif winner == 'O':
            message = "Computer Wins!"
        else:
            message = "It's a Tie!"
        
        text = font.render(message, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 1.5))
        pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            row, col = int(y // (HEIGHT // 3)), int(x // (WIDTH // 3))
            index = row * 3 + col
            
            # 사용자 차례
            if board[index] == ' ':
                board[index] = player
                if check_winner() is None:
                    computer_move()
                if check_winner() is not None:
                    game_over = True
    
    pygame.display.flip()

pygame.quit()