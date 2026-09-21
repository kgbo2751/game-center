import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

# 색상 정의
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLOR = (205, 193, 180)
CELL_EMPTY_COLOR = (204, 192, 179)
TEXT_COLOR = (119, 110, 101)

# 폰트 설정
font = pygame.font.SysFont("Arial", 40)

# 게임 클래스
class Game2048:
    def __init__(self):
        self.size = 4
        self.grid = [[0] * self.size for _ in range(self.size)]  # 4x4 그리드
        self.score = 0
        self.add_new_tile()  # 첫 번째 타일 추가

    def reset(self):
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = random.choice([2, 4])

    def slide_right(self):
        for i in range(self.size):
            row = [x for x in self.grid[i] if x != 0]  # 0을 제외한 값만 모은다
            merged = []
            j = len(row) - 1
            while j > 0:
                if row[j] == row[j - 1]:  # 두 숫자가 같으면 합쳐준다
                    merged.append(row[j] * 2)
                    self.score += row[j] * 2
                    j -= 2
                else:
                    merged.append(row[j])
                    j -= 1
            merged += row[:j+1]  # 나머지 값을 그대로 추가
            self.grid[i] = [0] * (self.size - len(merged)) + merged  # 왼쪽 빈 공간은 0으로 채운다

    def rotate_grid(self):
        self.grid = [list(row) for row in zip(*self.grid)]  # 행과 열을 바꾼다

    def move(self, direction):
        if direction == "UP":
            self.rotate_grid()
            self.slide_right()
            self.rotate_grid()
            self.rotate_grid()
            self.rotate_grid()
        elif direction == "DOWN":
            self.rotate_grid()
            self.rotate_grid()
            self.rotate_grid()
            self.slide_right()
            self.rotate_grid()
        elif direction == "LEFT":
            self.rotate_grid()
            self.rotate_grid()
            self.slide_right()
            self.rotate_grid()
            self.rotate_grid()
        elif direction == "RIGHT":
            self.slide_right()
        self.add_new_tile()  # 새로운 타일 추가

    def is_game_over(self):
        # 게임 종료 조건: 더 이상 이동할 수 있는 칸이 없으면 종료
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return False
                if i < self.size - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
                if j < self.size - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
        return True

    def draw(self, screen):
        block_size = WIDTH // self.size
        for i in range(self.size):
            for j in range(self.size):
                value = self.grid[i][j]
                x = (self.size - 1 - j) * block_size
                y = (self.size - 1 - i) * block_size
                rect = pygame.Rect(x, y, block_size, block_size)

                # 배경 색
                pygame.draw.rect(screen, CELL_COLOR if value != 0 else CELL_EMPTY_COLOR, rect)

                # 테두리 추가 (검정, 두께 2)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)

                # 숫자 표시
                if value != 0:
                    text = font.render(str(value), True, TEXT_COLOR)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

        # 점수 표시
        score_text = font.render(f"Score: {self.score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

# 게임 루프
running = True
game = Game2048()

while running:
    screen.fill(BACKGROUND_COLOR)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.move("UP")
            elif event.key == pygame.K_DOWN:
                game.move("DOWN")
            elif event.key == pygame.K_LEFT:
                game.move("LEFT")
            elif event.key == pygame.K_RIGHT:
                game.move("RIGHT")

    # 게임 오버 처리
    if game.is_game_over():
        game_over_text = font.render("Game Over!", True, TEXT_COLOR)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))

    # 퍼즐 그리기
    game.draw(screen)

    # 화면 업데이트
    pygame.display.flip()

pygame.quit()