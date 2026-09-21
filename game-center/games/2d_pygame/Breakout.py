import pygame

# 게임 초기화
pygame.init()

# 화면 크기
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# FPS 설정
clock = pygame.time.Clock()

# 폰트 설정
font = pygame.font.SysFont("Arial", 20)  # Arial 폰트 사용, 폰트 크기 20

# 패들 클래스
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.x = (WIDTH - self.width) // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 6
    
    def move(self, dx):
        self.x += dx * self.speed
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
    
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

# 공 클래스
class Ball:
    def __init__(self):
        self.radius = 10
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.x_vel = 3
        self.y_vel = -3
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
        if self.x <= 0 or self.x >= WIDTH:
            self.x_vel = -self.x_vel
        if self.y <= 0:
            self.y_vel = -self.y_vel
    
    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.radius)

# 벽돌 클래스
class Brick:
    def __init__(self, x, y):
        self.width = 60
        self.height = 20
        self.x = x
        self.y = y
        self.color = GREEN
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# 벽돌 생성
bricks = []
for row in range(3):
    for col in range(10):
        brick = Brick(col * 60 + 5, row * 25 + 5)
        bricks.append(brick)

# 게임 변수
paddle = Paddle()
ball = Ball()
score = 0
game_over = False

# 메인 게임 루프
running = True
while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 게임 종료 조건
    if ball.y > HEIGHT:
        game_over = True
        running = False

    # 키 입력에 따른 패들 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move(-1)
    if keys[pygame.K_RIGHT]:
        paddle.move(1)

    # 공 이동
    ball.move()

    # 공과 패들 충돌 처리
    if paddle.y <= ball.y + ball.radius <= paddle.y + paddle.height and paddle.x <= ball.x <= paddle.x + paddle.width:
        ball.y_vel = -ball.y_vel
    
    # 공과 벽돌 충돌 처리
    for brick in bricks[:]:
        if brick.x <= ball.x <= brick.x + brick.width and brick.y <= ball.y <= brick.y + brick.height:
            bricks.remove(brick)
            ball.y_vel = -ball.y_vel
            score += 10  # 벽돌을 깨면 점수 증가

    # 벽돌 그리기
    for brick in bricks:
        brick.draw()

    # 패들 그리기
    paddle.draw()

    # 공 그리기
    ball.draw()

    # 점수 출력
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # 게임 오버 메시지
    if game_over:
        font = pygame.font.SysFont("Arial", 40)
        game_over_text = font.render("Game Over!", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

pygame.quit()