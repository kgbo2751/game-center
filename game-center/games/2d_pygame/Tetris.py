import pygame
import random

# 초기화
pygame.init()
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
cols, rows = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# 색상 정의
COLORS = [
    (0, 255, 255),  # I
    (255, 255, 0),  # O
    (128, 0, 128),  # T
    (0, 255, 0),    # S
    (255, 0, 0),    # Z
    (0, 0, 255),    # J
    (255, 165, 0),  # L
]

# 블록 정의
SHAPES = [
    [[1, 1, 1, 1]],                # I
    [[1, 1], [1, 1]],              # O
    [[0, 1, 0], [1, 1, 1]],        # T
    [[0, 1, 1], [1, 1, 0]],        # S
    [[1, 1, 0], [0, 1, 1]],        # Z
    [[1, 0, 0], [1, 1, 1]],        # J
    [[0, 0, 1], [1, 1, 1]],        # L
]

def create_grid():
    return [[(0, 0, 0)] * cols for _ in range(rows)]

def draw_grid(surface, grid):
    for y in range(rows):
        for x in range(cols):
            pygame.draw.rect(surface, grid[y][x], (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, (50, 50, 50), (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = cols // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_coords(self):
        coords = []
        for i, row in enumerate(self.shape):
            for j, val in enumerate(row):
                if val:
                    coords.append((self.x + j, self.y + i))
        return coords

def check_collision(grid, shape):
    for x, y in shape.get_coords():
        if x < 0 or x >= cols or y >= rows or (y >= 0 and grid[y][x] != (0, 0, 0)):
            return True
    return False

def merge_grid(grid, shape):
    for x, y in shape.get_coords():
        if 0 <= y < rows:
            grid[y][x] = shape.color

def clear_lines(grid):
    full_lines = [i for i in range(rows) if (0, 0, 0) not in grid[i]]
    for i in full_lines:
        del grid[i]
        grid.insert(0, [(0, 0, 0)] * cols)
    return len(full_lines)

# 게임 변수
grid = create_grid()
current = Tetromino()
fall_time = 0
score = 0

# 게임 루프
running = True
while running:
    fall_time += clock.get_rawtime()
    clock.tick(60)

    if fall_time > 500:
        current.y += 1
        if check_collision(grid, current):
            current.y -= 1
            merge_grid(grid, current)
            score += clear_lines(grid)
            current = Tetromino()
            if check_collision(grid, current):  # 게임 오버
                running = False
        fall_time = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current.x -= 1
                if check_collision(grid, current):
                    current.x += 1
            elif event.key == pygame.K_RIGHT:
                current.x += 1
                if check_collision(grid, current):
                    current.x -= 1
            elif event.key == pygame.K_DOWN:
                current.y += 1
                if check_collision(grid, current):
                    current.y -= 1
            elif event.key == pygame.K_UP:
                current.rotate()
                if check_collision(grid, current):
                    current.rotate()
                    current.rotate()
                    current.rotate()

    screen.fill((0, 0, 0))
    draw_grid(screen, grid)
    for x, y in current.get_coords():
        if y >= 0:
            pygame.draw.rect(screen, current.color, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.update()

pygame.quit()