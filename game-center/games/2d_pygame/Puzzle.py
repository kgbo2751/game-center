import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4x4 Puzzle")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 폰트 설정
font = pygame.font.SysFont("Arial", 30)

# 퍼즐 클래스
class Puzzle:
    def __init__(self):
        self.size = 4  # 4x4 퍼즐
        self.pieces = [i for i in range(1, self.size * self.size)] + [None]  # 조각들 (빈 칸은 None)
        self.shuffle_pieces()
        self.blank_pos = self.pieces.index(None)

    def shuffle_pieces(self):
        random.shuffle(self.pieces)
        
    def move_piece(self, direction):
        x, y = self.blank_pos % self.size, self.blank_pos // self.size
        
        if direction == "UP" and y < self.size - 1:
            swap_pos = self.blank_pos + self.size
        elif direction == "DOWN" and y > 0:
            swap_pos = self.blank_pos - self.size
        elif direction == "LEFT" and x < self.size - 1:
            swap_pos = self.blank_pos + 1
        elif direction == "RIGHT" and x > 0:
            swap_pos = self.blank_pos - 1
        else:
            return
        
        # 조각 이동
        self.pieces[self.blank_pos], self.pieces[swap_pos] = self.pieces[swap_pos], self.pieces[self.blank_pos]
        self.blank_pos = swap_pos

    def is_solved(self):
        return self.pieces == [i for i in range(1, self.size * self.size)] + [None]

    def draw(self, screen):
        block_size = WIDTH // self.size
        for i, piece in enumerate(self.pieces):
            x, y = i % self.size, i // self.size
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            if piece is not None:
                pygame.draw.rect(screen, BLUE, rect)
                text = font.render(str(piece), True, WHITE)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 3)

# 게임 루프
running = True
game_over = False
puzzle = Puzzle()

while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP:
                    puzzle.move_piece("UP")
                elif event.key == pygame.K_DOWN:
                    puzzle.move_piece("DOWN")
                elif event.key == pygame.K_LEFT:
                    puzzle.move_piece("LEFT")
                elif event.key == pygame.K_RIGHT:
                    puzzle.move_piece("RIGHT")
    
    # 퍼즐 그리기
    puzzle.draw(screen)

    # 게임 종료 처리
    if puzzle.is_solved() and not game_over:
        game_over_text = font.render("Puzzle completed!", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2))

    # 화면 업데이트
    pygame.display.flip()

pygame.quit()