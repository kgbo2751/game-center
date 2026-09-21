import pygame

pygame.init()
WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
CELL = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rush Hour")

# 색상
BG = (240, 240, 240)
MAIN_CAR_COLOR = (255, 0, 0)
CAR_COLOR = (0, 128, 255)
EXIT_COLOR = (0, 255, 0)
HIGHLIGHT_COLOR = (255, 255, 0)

# 차량 클래스
class Car:
    def __init__(self, x, y, length, is_horizontal, is_main=False):
        self.x = x
        self.y = y
        self.length = length
        self.is_horizontal = is_horizontal
        self.is_main = is_main
        self.color = MAIN_CAR_COLOR if is_main else CAR_COLOR

    def get_cells(self):
        return [(self.x + i if self.is_horizontal else self.x,
                 self.y if self.is_horizontal else self.y + i)
                for i in range(self.length)]

    def draw(self, selected=False):
        for cx, cy in self.get_cells():
            pygame.draw.rect(screen, self.color, (cx*CELL, cy*CELL, CELL, CELL))
            pygame.draw.rect(screen, (0, 0, 0), (cx*CELL, cy*CELL, CELL, CELL), 2)
        if selected:
            x1, y1 = self.get_cells()[0]
            x2, y2 = self.get_cells()[-1]
            x_min = min(x1, x2) * CELL
            y_min = min(y1, y2) * CELL
            w = (abs(x2 - x1) + 1) * CELL if self.is_horizontal else CELL
            h = CELL if self.is_horizontal else (abs(y2 - y1) + 1) * CELL
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (x_min, y_min, w, h), 4)

    def move(self, dx, dy, cars):
        if self.is_horizontal and dy != 0: return
        if not self.is_horizontal and dx != 0: return
        new_cells = [(x + dx, y + dy) for x, y in self.get_cells()]
        for x, y in new_cells:
            if x < 0 or x >= COLS or y < 0 or y >= ROWS:
                return
            for car in cars:
                if car is not self and (x, y) in car.get_cells():
                    return
        self.x += dx
        self.y += dy

# 차량 초기 설정
cars = [
    Car(0, 2, 3, True, is_main=True),  # 메인 차량
    Car(0, 0, 2, False),
    Car(3, 1, 2, True),
    Car(5, 0, 3, False),
    Car(6, 4, 2, True),
    Car(2, 5, 3, False),
]

selected_car = 0
font = pygame.font.SysFont(None, 36)
running = True

def get_clicked_car(mx, my):
    cx, cy = mx // CELL, my // CELL
    for i, car in enumerate(cars):
        if (cx, cy) in car.get_cells():
            return i
    return None

while running:
    screen.fill(BG)

    # 탈출구
    pygame.draw.rect(screen, EXIT_COLOR, (CELL*7, CELL*7, CELL, CELL))

    for i, car in enumerate(cars):
        car.draw(selected=(i == selected_car))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            clicked = get_clicked_car(mx, my)
            if clicked is not None:
                selected_car = clicked
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                cars[selected_car].move(1, 0, cars)
            elif event.key == pygame.K_LEFT:
                cars[selected_car].move(-1, 0, cars)
            elif event.key == pygame.K_UP:
                cars[selected_car].move(0, -1, cars)
            elif event.key == pygame.K_DOWN:
                cars[selected_car].move(0, 1, cars)

    # 승리 조건
    if (7, 7) in cars[0].get_cells():
        win_text = font.render("Clear!", True, (0, 0, 0))
        screen.blit(win_text, (WIDTH // 2 - 50, HEIGHT // 2))

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()