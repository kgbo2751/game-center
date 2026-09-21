import pygame
import random
import math

# 초기 설정
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the Lasers")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# 색상
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (50, 100, 255)
BLACK = (0, 0, 0)

# 플레이어 설정
player_radius = 15
player_pos = [WIDTH // 2, HEIGHT // 2]  # 리스트로 변경해서 이동 가능
player_speed = 5

# 레이저 설정
lasers = []
laser_speed = 4
spawn_delay = 30
frame_count = 0
score = 0

# 레이저 클래스
class Laser:
    def __init__(self):
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            self.pos = [random.randint(0, WIDTH), 0]
        elif edge == "bottom":
            self.pos = [random.randint(0, WIDTH), HEIGHT]
        elif edge == "left":
            self.pos = [0, random.randint(0, HEIGHT)]
        else:
            self.pos = [WIDTH, random.randint(0, HEIGHT)]

        # 방향 벡터 계산 (플레이어 위치 향해)
        dx = player_pos[0] - self.pos[0]
        dy = player_pos[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        self.dir = [dx / dist, dy / dist]

    def move(self):
        self.pos[0] += self.dir[0] * laser_speed
        self.pos[1] += self.dir[1] * laser_speed

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.pos[0]), int(self.pos[1])), 6)

    def hit_player(self):
        dx = self.pos[0] - player_pos[0]
        dy = self.pos[1] - player_pos[1]
        return math.hypot(dx, dy) < player_radius + 6


# 메인 루프
running = True
while running:
    screen.fill(WHITE)
    frame_count += 1

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 (플레이어 이동)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] - player_radius > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] + player_radius < WIDTH:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] - player_radius > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] + player_radius < HEIGHT:
        player_pos[1] += player_speed

    # 레이저 생성
    if frame_count % spawn_delay == 0:
        lasers.append(Laser())
        score += 1

    # 레이저 이동 및 충돌 체크
    for laser in lasers:
        laser.move()
        laser.draw()
        if laser.hit_player():
            running = False

    # 플레이어 그리기
    pygame.draw.circle(screen, BLUE, player_pos, player_radius)

    # 점수 표시
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()