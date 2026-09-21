import pygame
import random

# 초기화
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, platform_rect):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(midbottom=(platform_rect.centerx, platform_rect.top))
        self.vel_y = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        self.vel_y += 0.5  # 중력
        self.rect.y += self.vel_y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# 발판 클래스
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 10))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

# 스프라이트 그룹
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# 초기 발판 생성
# 초기 발판 생성
for i in range(6):
    x = random.randint(0, WIDTH - 60)
    y = i * 100
    p = Platform(x, y)
    all_sprites.add(p)
    platforms.add(p)

# 플레이어를 가장 아래 발판 위에 생성
bottom_platform = max(platforms, key=lambda p: p.rect.y)
player = Player(bottom_platform.rect)
all_sprites.add(player)

score = 0
font = pygame.font.SysFont(None, 36)
running = True

while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 플레이어 발판 충돌 체크
    if player.vel_y > 0:
        hits = pygame.sprite.spritecollide(player, platforms, False)
        if hits and player.rect.bottom <= hits[0].rect.bottom + 10:
            player.vel_y = -12  # 점프

    player.update()

    # 화면 스크롤
    if player.rect.top <= HEIGHT // 3:
        offset = HEIGHT // 3 - player.rect.top
        player.rect.top = HEIGHT // 3
        score += offset
        for p in platforms:
            p.rect.y += offset
        # 새 발판 추가
        while len(platforms) < 6:
            x = random.randint(0, WIDTH - 60)
            y = random.randint(-50, 0)
            new_p = Platform(x, y)
            all_sprites.add(new_p)
            platforms.add(new_p)

    # 바닥 아래 발판 제거
    for p in list(platforms):
        if p.rect.top > HEIGHT:
            p.kill()

    all_sprites.draw(screen)

    # 점수 출력
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()

    # 게임 오버
    if player.rect.top > HEIGHT:
        running = False

pygame.quit()