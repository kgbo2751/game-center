import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dodge the Obstacles")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)

# 차선 설정 (5개 차선)
lane_width = screen_width // 5  # 차선 너비를 5개로 나눔
lane_x = [lane_width * i + lane_width // 2 for i in range(5)]  # 5개 차선의 x 좌표

# 자동차 설정
car_width = 50
car_height = 80
car_x = lane_x[2] - car_width // 2  # 처음에 중앙 차선에 위치 (세 번째 차선)
car_y = screen_height - car_height - 10
car_speed = 30  # 좌우 이동 속도 설정

# 장애물 설정
obstacle_width = 50
obstacle_height = 80
obstacle_speed = 5

# 폰트 설정
font = pygame.font.SysFont('Arial', 30)

# 장애물 클래스 정의
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((obstacle_width, obstacle_height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -obstacle_height

    def update(self):
        self.rect.y += obstacle_speed
        if self.rect.y > screen_height:
            self.kill()  # 화면을 벗어난 장애물은 제거

# 자동차 클래스 정의
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((car_width, car_height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = car_x
        self.rect.y = car_y

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > lane_x[0]:
            self.rect.x -= car_speed  # 왼쪽 차선으로 이동
        if keys[pygame.K_RIGHT] and self.rect.x < lane_x[4] - car_width:
            self.rect.x += car_speed  # 오른쪽 차선으로 이동

# 그룹 설정
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# 플레이어 자동차 생성
car = Car()
all_sprites.add(car)

# 게임 루프
running = True
score = 0
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # 프레임 속도 60fps로 설정
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 장애물 생성 (무작위로 차선에 생성)
    if random.randint(1, 30) == 1:  # 30번에 1번 확률로 장애물 생성
        lane_choice = random.choice(lane_x)
        obstacle = Obstacle(lane_choice)
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

    # 모든 스프라이트 업데이트
    all_sprites.update()

    # 충돌 처리
    if pygame.sprite.spritecollideany(car, obstacles):
        running = False  # 충돌하면 게임 종료

    # 화면 그리기
    screen.fill(BLACK)

    # 차선 그리기
    for x in lane_x:
        pygame.draw.line(screen, WHITE, (x, 0), (x, screen_height), 5)

    # 모든 스프라이트 그리기
    all_sprites.draw(screen)

    # 점수 표시
    score += 1  # 시간에 따라 점수 증가
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # 화면 업데이트
    pygame.display.flip()

# 게임 종료 후 처리
pygame.quit()