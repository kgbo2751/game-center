import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 크기 및 설정
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# 색상 설정
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 폰트 설정
font = pygame.font.SysFont("Arial", 20)

# Minesweeper 게임 클래스
class Minesweeper:
    def __init__(self, grid_size, num_mines):
        self.grid_size = grid_size
        self.num_mines = num_mines
        self.board = [[0] * grid_size for _ in range(grid_size)]  # 지뢰판
        self.revealed = [[False] * grid_size for _ in range(grid_size)]  # 셀 공개 여부
        self.game_over = False
        self.mines = set()  # 지뢰 위치

        # 지뢰 배치
        self._place_mines()

    def _place_mines(self):
        # 지뢰 배치 (랜덤)
        mines_placed = 0
        while mines_placed < self.num_mines:
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if self.board[y][x] != -1:  # 지뢰가 이미 있는 곳은 건너뛰기
                self.board[y][x] = -1
                self.mines.add((x, y))
                mines_placed += 1

        # 숫자 설정: 각 셀에 주변 지뢰의 수
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.board[y][x] == -1:
                    continue
                # 인접한 8개 셀의 지뢰 개수 세기
                self.board[y][x] = sum((nx, ny) in self.mines for nx in range(x-1, x+2) for ny in range(y-1, y+2) if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size)

    def reveal(self, x, y):
        # 게임 오버가 아니면 셀을 공개
        if self.game_over or self.revealed[y][x]:
            return
        self.revealed[y][x] = True

        # 지뢰를 클릭했다면 게임 오버
        if self.board[y][x] == -1:
            self.game_over = True
            return

        # 0인 경우 주변 셀을 재귀적으로 열기
        if self.board[y][x] == 0:
            for nx in range(x-1, x+2):
                for ny in range(y-1, y+2):
                    if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                        if not self.revealed[ny][nx]:
                            self.reveal(nx, ny)

    def draw(self, screen):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.revealed[y][x]:
                    pygame.draw.rect(screen, WHITE, rect)
                    pygame.draw.rect(screen, BLACK, rect, 2)
                    if self.board[y][x] == -1:
                        pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
                    elif self.board[y][x] > 0:
                        text = font.render(str(self.board[y][x]), True, BLUE)
                        screen.blit(text, (x * CELL_SIZE + (CELL_SIZE - text.get_width()) // 2, y * CELL_SIZE + (CELL_SIZE - text.get_height()) // 2))
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    pygame.draw.rect(screen, BLACK, rect, 2)
                if self.game_over and self.board[y][x] == -1 and not self.revealed[y][x]:
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)

# 게임 초기화
game = Minesweeper(grid_size=GRID_SIZE, num_mines=10)

# 게임 루프
running = True
while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 왼쪽 클릭
                mx, my = event.pos
                x, y = mx // CELL_SIZE, my // CELL_SIZE
                game.reveal(x, y)

    # 게임 Paper드 그리기
    game.draw(screen)

    # 게임 오버 메시지
    if game.game_over:
        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 20))

    # 화면 업데이트
    pygame.display.flip()

pygame.quit()
sys.exit()