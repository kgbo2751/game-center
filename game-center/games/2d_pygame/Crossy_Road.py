import pygame
import random

# 초기 설정
pygame.init()
WIDTH, HEIGHT = 600, 800
TILE_SIZE = 50
ROWS = HEIGHT // TILE_SIZE
CARS_LANES = 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
GRAY = (100, 100, 100)
BLUE = (50, 50, 255)

# 플레이어
player = pygame.Rect(WIDTH//2 - TILE_SIZE//2, HEIGHT - TILE_SIZE, TILE_SIZE, TILE_SIZE)

# 자동차 클래스
class Car:
    def __init__(self, lane, direction):
        self.lane = lane
        self.y = TILE_SIZE * lane
        self.direction = direction
        self.width = 60
        self.height = 40
        if direction == "left":
            self.rect = pygame.Rect(WIDTH, self.y + 5, self.width, self.height)
            self.speed = random.randint(4, 7)
        else:
            self.rect = pygame.Rect(-self.width, self.y + 5, self.width, self.height)
            self.speed = random.randint(4, 7)

    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# 자동차 관리
cars = []
car_timer = 0

# 게임 상태
running = True
game_state = "playing"

def draw_lanes():
    for i in range(ROWS):
        y = i * TILE_SIZE
        if 0 < i <= CARS_LANES:
            pygame.draw.rect(screen, GRAY, (0, y, WIDTH, TILE_SIZE))
        else:
            pygame.draw.rect(screen, GREEN, (0, y, WIDTH, TILE_SIZE))

while running:
    clock.tick(60)
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if game_state == "playing":
        # 플레이어 이동 (타일 단위)
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= TILE_SIZE
            pygame.time.wait(100)
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += TILE_SIZE
            pygame.time.wait(100)
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= TILE_SIZE
            pygame.time.wait(100)
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += TILE_SIZE
            pygame.time.wait(100)

        # 자동차 스폰
        car_timer += 1
        if car_timer > 30:
            lane = random.randint(1, CARS_LANES)
            direction = random.choice(["left", "right"])
            cars.append(Car(lane, direction))
            car_timer = 0

        # 자동차 업데이트
        for car in cars:
            car.update()

        # 충돌 검사
        for car in cars:
            if player.colliderect(car.rect):
                game_state = "lose"

        # 승리 조건
        if player.top <= 0:
            game_state = "win"

    # 배경 및 도로
    draw_lanes()

    # 자동차 그리기
    for car in cars:
        car.draw()

    # 플레이어 그리기
    pygame.draw.rect(screen, BLUE, player)

    # 메시지 출력
    if game_state == "win":
        msg = font.render("YOU WIN!", True, WHITE)
        screen.blit(msg, (WIDTH//2 - 100, HEIGHT//2))
    elif game_state == "lose":
        msg = font.render("GAME OVER", True, RED)
        screen.blit(msg, (WIDTH//2 - 120, HEIGHT//2))

    pygame.display.flip()

pygame.quit()