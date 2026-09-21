import pygame
import random

# 카드 덱 및 각 카드의 특성 정의
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deck = [(value, suit) for suit in suits for value in values]

# 카드 값 계산 (높은 카드 우선)
card_values = {value: index for index, value in enumerate(values, 2)}  # 2-10, J=10, Q=10, K=10, A=1 or 11

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)

# 폰트 설정
font = pygame.font.SysFont("NotoSansKR-Regular.ttf", 30)

# 카드 배분 함수
def deal_cards():
    random.shuffle(deck)
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    return player_hand, dealer_hand

# 카드 값을 계산
def calculate_hand(hand):
    total = 0
    aces = 0
    for card in hand:
        value = card[0]
        if value in ['J', 'Q', 'K']:
            total += 10
        elif value == 'A':
            total += 11
            aces += 1
        else:
            total += int(value)

    # A가 11일 때 21을 넘으면 1로 취급
    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total

# 게임 루프
running = True
player_hand, dealer_hand = deal_cards()  # 카드를 나눠줌
player_score = calculate_hand(player_hand)
dealer_score = calculate_hand(dealer_hand)

# 게임 진행 상태
game_over = False
player_stands = False
dealer_stands = False

while running:
    screen.fill(GREEN)

    # 플레이어 카드 출력
    for i, card in enumerate(player_hand):
        card_text = f"{card[0]} of {card[1]}"
        text_surface = font.render(card_text, True, WHITE)
        screen.blit(text_surface, (50 + i * 150, HEIGHT - 200))

    # 딜러 카드 출력
    for i, card in enumerate(dealer_hand):
        card_text = f"{card[0]} of {card[1]}"
        text_surface = font.render(card_text, True, WHITE)
        if i == 0 and not game_over:  # 딜러의 첫 번째 카드는 숨깁니다.
            card_text = "Hidden Card"
        screen.blit(text_surface, (50 + i * 150, 100))

    # 점수 출력
    player_score_text = font.render(f"Your Score: {player_score}", True, WHITE)
    screen.blit(player_score_text, (10, HEIGHT - 250))

    dealer_score_text = font.render(f"Dealer Score: {dealer_score}" if game_over else "Dealer Score: ?", True, WHITE)
    screen.blit(dealer_score_text, (10, 50))

    # 플레이어가 Hit을 선택할 수 있도록 안내
    if not game_over:
        hit_text = font.render("Press H for Hit, S for Stand", True, WHITE)
        screen.blit(hit_text, (WIDTH // 2 - hit_text.get_width() // 2, HEIGHT - 50))

    # 게임 종료 후 승패 출력
    if game_over:
        if player_score > 21:
            result_text = font.render("You Bust! Dealer Wins!", True, WHITE)
        elif dealer_score > 21:
            result_text = font.render("Dealer Busts! You Win!", True, WHITE)
        elif player_score > dealer_score:
            result_text = font.render("You Win!", True, WHITE)
        elif player_score < dealer_score:
            result_text = font.render("Dealer Wins!", True, WHITE)
        else:
            result_text = font.render("It's a Tie!", True, WHITE)

        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2))

    # 게임 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 키 입력 처리
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h and not game_over:
                # 플레이어가 카드를 받음
                player_hand.append(deck.pop())
                player_score = calculate_hand(player_hand)

                if player_score > 21:
                    game_over = True

            if event.key == pygame.K_s and not game_over:
                # 플레이어가 Stand
                player_stands = True
                game_over = True  # 게임 종료 후 딜러 진행

    # 딜러가 카드를 받음 (게임 오버 후)
    if game_over and dealer_score < 17:
        dealer_hand.append(deck.pop())
        dealer_score = calculate_hand(dealer_hand)

    # 화면 업데이트
    pygame.display.flip()

pygame.quit()