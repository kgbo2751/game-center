import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Card Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# 폰트 설정
font = pygame.font.SysFont("Arial", 30)

# 카드 클래스
class Card:
    def __init__(self, color, x, y):
        self.color = color
        self.rect = pygame.Rect(x, y, 100, 100)
        self.flipped = False
        self.matched = False

    def flip(self):
        self.flipped = not self.flipped

    def draw(self, screen):
        if self.flipped or self.matched:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            pygame.draw.rect(screen, BLACK, self.rect)
            pygame.draw.line(screen, WHITE, self.rect.topleft, self.rect.bottomright, 3)
            pygame.draw.line(screen, WHITE, self.rect.bottomleft, self.rect.topright, 3)

# 게임 변수
cards = []
flipped_cards = []
score = 0
matched_pairs = 0
total_pairs = 8  # 4x4에서 8쌍의 카드
game_over = False

# 카드 색 리스트 (색상만 사용)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
          (0, 255, 255), (255, 0, 255), (128, 0, 128), (255, 165, 0)]

# 게임 초기화
def create_cards():
    global cards
    card_deck = colors * 2  # 카드 색을 2번 반복하여 한 덱을 만듦
    random.shuffle(card_deck)  # 랜덤하게 섞음
    x, y = 50, 50
    for color in card_deck:
        cards.append(Card(color, x, y))
        x += 120  # 가로로 배치
        if x > WIDTH - 100:
            x = 50
            y += 120  # 세로로 배치

# 카드 매칭 처리
def check_match():
    global matched_pairs, score
    if len(flipped_cards) == 2:
        card1, card2 = flipped_cards
        if card1.color == card2.color:  # 카드 두 장이 같으면 매칭
            card1.matched = True
            card2.matched = True
            matched_pairs += 1
            score += 1
        # 두 장을 다시 뒤집기 전에 잠시 대기
        pygame.time.delay(500)
        flipped_cards.clear()

# 게임 루프
running = True
create_cards()

while running:
    screen.fill(GREEN)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            # 카드 클릭 처리
            if len(flipped_cards) < 2:  # 두 개의 카드만 뒤집을 수 있음
                for card in cards:
                    if card.rect.collidepoint(event.pos) and not card.flipped and not card.matched:
                        card.flip()
                        flipped_cards.append(card)
                        check_match()

    # 카드 그리기
    for card in cards:
        card.draw(screen)

    # 점수 출력
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # 게임 종료 확인
    if matched_pairs == total_pairs:  # 모든 카드가 맞춰졌을 때 게임 종료
        game_over_text = font.render("Game Over! You matched all cards.", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))

    # 화면 업데이트
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()