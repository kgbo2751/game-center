import pygame
import random

# 카드 덱 및 각 카드의 특성 정의
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deck = [(value, suit) for suit in suits for value in values]

# 카드 값 계산 (높은 카드 우선)
card_values = {value: index for index, value in enumerate(values, 2)}  # 2-10, J=11, Q=12, K=13, A=14

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1v1 Poker (Cards Exchangeable)")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)

# 폰트 설정
font = pygame.font.SysFont("NotoSansKR-Regular.ttf", 30)

# 카드 배분
def deal_cards():
    random.shuffle(deck)
    player_hand = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()]
    ai_hand = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()]
    return player_hand, ai_hand

# 카드 값을 평가 (단순히 가장 높은 카드로 승자 결정)
def evaluate_hand(hand):
    hand_values = [card_values[card[0]] for card in hand]
    return max(hand_values)

# 카드 교환
def exchange_cards(hand, indices_to_exchange):
    for index in indices_to_exchange:
        new_card = deck.pop()
        hand[index] = new_card

# 게임 루프
running = True
player_hand, ai_hand = deal_cards()  # 카드를 나눠줌
player_score = evaluate_hand(player_hand)
ai_score = evaluate_hand(ai_hand)

# 교환할 카드 인덱스 (플레이어가 선택할 수 있음)
exchange_indices = []  # 교환할 카드 인덱스 저장

while running:
    screen.fill(GREEN)

    # 카드 출력
    for i, card in enumerate(player_hand):
        card_text = f"{card[0]} of {card[1]}"
        text_surface = font.render(card_text, True, WHITE)
        screen.blit(text_surface, (50 + i * 150, HEIGHT - 200))

    for i, card in enumerate(ai_hand):
        card_text = f"{card[0]} of {card[1]}"
        text_surface = font.render(card_text, True, WHITE)
        screen.blit(text_surface, (50 + i * 150, 100))

    # 교환할 카드 선택 (플레이어가 카드 클릭 시)
    if exchange_indices:
        for index in exchange_indices:
            pygame.draw.rect(screen, (255, 0, 0), (50 + index * 150, HEIGHT - 200, 100, 50), 3)

    # 승자 판단
    player_score = evaluate_hand(player_hand)
    ai_score = evaluate_hand(ai_hand)
    if player_score > ai_score:
        winner_text = font.render("You Win!", True, WHITE)
    elif player_score < ai_score:
        winner_text = font.render("AI Wins!", True, WHITE)
    else:
        winner_text = font.render("It's a Tie!", True, WHITE)

    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))

    # 교환 버튼
    exchange_text = font.render("Click a card to exchange", True, WHITE)
    screen.blit(exchange_text, (WIDTH // 2 - exchange_text.get_width() // 2, HEIGHT - 50))

    # 게임 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 플레이어가 카드 클릭 시 교환 카드 선택
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y >= HEIGHT - 200:
                card_index = (x - 50) // 150
                if card_index < len(player_hand):
                    if card_index in exchange_indices:
                        exchange_indices.remove(card_index)  # 카드 선택 해제
                    else:
                        exchange_indices.append(card_index)  # 카드 선택

        # 엔터키로 교환 후 게임 진행
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if exchange_indices:
                exchange_cards(player_hand, exchange_indices)
                exchange_indices.clear()  # 교환 후 초기화

    # 화면 업데이트
    pygame.display.flip()

pygame.quit()