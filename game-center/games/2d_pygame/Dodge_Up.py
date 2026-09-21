import pygame
import random

# Pygame 초기화
pygame.init()

# 게임 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dodge Game")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 게임 속도 설정
clock = pygame.time.Clock()

# 캐릭터 설정
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# 떨어지는 물체 설정
falling_object_width = 50
falling_object_height = 50
falling_speed = 5

# 점수
score = 0
font = pygame.font.SysFont("Arial", 30)

# 게임 루프
running = True
falling_objects = []

def create_falling_object():
    x = random.randint(0, screen_width - falling_object_width)
    y = -falling_object_height
    falling_objects.append(pygame.Rect(x, y, falling_object_width, falling_object_height))

while running:
    screen.fill(BLACK)
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # 떨어지는 물체 업데이트
    if random.random() < 0.02:  # 확률로 새로운 물체를 생성
        create_falling_object()
    
    for obj in falling_objects[:]:
        obj.y += falling_speed
        if obj.y > screen_height:
            falling_objects.remove(obj)
            score += 1  # 물체가 화면을 지나가면 점수 증가
    
    # 충돌 처리
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for obj in falling_objects:
        if player_rect.colliderect(obj):
            running = False  # 충돌하면 게임 오버

    # 화면에 물체 그리기
    pygame.draw.rect(screen, WHITE, player_rect)
    for obj in falling_objects:
        pygame.draw.rect(screen, RED, obj)
    
    # 점수 출력
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # 화면 업데이트
    pygame.display.flip()

    # 게임 속도 조절
    clock.tick(60)

pygame.quit()